"""Render the labelled six-variable subset-encoding diagram."""

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product
from math import cos, pi, sin
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


SIZE = (944, 560)
BG = "#0b1324"
PANEL = "#13223a"
RULE = "#293c58"
TEXT = "#f5f8ff"
SOFT = "#b8c8df"
CYAN = "#67def5"
GREEN = "#8de4a5"
ORANGE = "#ffd185"
SUBSETS = ("∅", "{k₁}", "{k₂}", "{k₁, k₂}")
PAIR_NAMES = ("a₁, b₁", "a₁, b₂", "a₂, b₁", "a₂, b₂")
CHOICES = (1, 2, 0, 3)
PAIRS = tuple(product(range(2), range(2, 4)))


def minor_det(matrix, rows, cols):
    result = Fraction(0)
    for order in permutations(range(len(rows))):
        inversions = sum(i > j for a, i in enumerate(order) for j in order[a + 1:])
        term = Fraction((-1) ** inversions)
        for r, c in zip(rows, order):
            term *= matrix[r][cols[c]]
        result += term
    return result


def rational_example():
    """Build the displayed matrix and verify the explicit determinant table."""
    t = Fraction(1, 16)
    matrix = [[Fraction(i == j) for j in range(6)] for i in range(6)]
    for i in range(4):
        for k, weight in ((4, 1), (5, 2)):
            matrix[i][k] = matrix[k][i] = t * (weight if i < 2 else 1)
    for (i, j), choice in zip(PAIRS, CHOICES):
        matrix[i][j] = matrix[j][i] = t * t * choice
    for mask in range(64):
        s = tuple(i for i in range(6) if mask & (1 << i))
        assert minor_det(matrix, s, s) > 0
    table = []
    for (i, j), choice in zip(PAIRS, CHOICES):
        row = []
        for mask in range(4):
            s = tuple(k for index, k in enumerate((4, 5)) if mask & (1 << index))
            scaled = 256 * minor_det(matrix, (i,) + s, (j,) + s)
            assert scaled == choice - mask
            row.append(int(scaled))
        assert row.count(0) == 1
        table.append(tuple(row))
    return tuple(table)


def make_renderer(regular, bold, det_table):
    @lru_cache
    def font(size, heavy=False):
        return ImageFont.truetype(str(bold if heavy else regular), size)

    def frame(angle, selected, test):
        image = Image.new("RGB", SIZE, BG)
        draw = ImageDraw.Draw(image)

        def label(x, y, value, size, color=TEXT, heavy=False, anchor="lt"):
            face = font(size, heavy)
            left, top, right, bottom = draw.textbbox((x, y), value, font=face, anchor=anchor)
            assert 0 <= left <= right <= SIZE[0] and 0 <= top <= bottom <= SIZE[1], value
            draw.text((x, y), value, fill=color, font=face, anchor=anchor)

        def project(x, y, z):
            view_x = x * cos(angle) - y * sin(angle)
            depth = x * sin(angle) + y * cos(angle)
            return (256 + 142 * view_x, 376 + 65 * depth - 48 * z)

        label(39, 35, "Recover a subset from one zero", 36, heavy=True)
        label(41, 84, "Six labelled variables  /  two selectors, weights 1 and 2", 19, SOFT)
        draw.line((40, 119, 906, 119), fill=RULE, width=2)
        label(40, 149, "Each column is one pair across A and B", 18, SOFT)

        floor = [(x, y, 0) for x, y in [(-.96, -.96), (.96, -.96), (.96, .96), (-.96, .96)]]
        draw.polygon([project(*v) for v in floor], fill=PANEL, outline=RULE, width=2)
        for x in (-.58, .58):
            draw.line([project(x, y, 0) for y in (-.96, .96)], fill=RULE, width=2)
        for y in (-.58, .58):
            draw.line([project(x, y, 0) for x in (-.96, .96)], fill=RULE, width=2)
        for index, v in enumerate((-.58, .58)):
            label(*project(v, 1.13, 0), ("a₁", "a₂")[index], 18, CYAN, True, "mm")
            label(*project(1.16, v, 0), ("b₁", "b₂")[index], 18, ORANGE, True, "mm")

        positions = tuple(product((-.58, .58), repeat=2))
        order = sorted(range(4), key=lambda idx: positions[idx][0] * sin(angle) + positions[idx][1] * cos(angle))
        order.remove(selected)
        order.append(selected)
        for index in order:
            x, y = positions[index]
            color = CYAN if index == selected else "#859ab8"
            draw.line([project(x, y, 0), project(x, y, 3)], fill=color, width=3 if index == selected else 2)
            for value in range(4):
                X, Y = project(x, y, value)
                radius = 4
                if CHOICES[index] == value:
                    radius = 10
                    draw.ellipse((X-radius, Y-radius, X+radius, Y+radius), fill=color, outline=BG, width=2)
                    label(X + 14, Y, str(value), 19, color, True, "lm")
                else:
                    draw.ellipse((X-radius, Y-radius, X+radius, Y+radius), fill=BG, outline=color, width=2)
                if index == selected and value == test:
                    ring = radius + 6
                    draw.ellipse(
                        (X-ring, Y-ring, X+ring, Y+ring), outline=GREEN if value == CHOICES[index] else ORANGE, width=3,
                    )

        draw.rounded_rectangle((491, 144, 905, 448), radius=17, fill=PANEL)
        label(512, 167, f"Inspect pair ({PAIR_NAMES[selected]})", 23, heavy=True)
        label(512, 203, f"Stored subset R = {SUBSETS[CHOICES[selected]]}", 20, CYAN, True)
        label(512, 245, "Test subset S", 16, SOFT, True)
        label(879, 245, "256 × determinant", 16, SOFT, True, "rt")
        for index, subset in enumerate(SUBSETS):
            y = 276 + 37 * index
            value = det_table[selected][index]
            color = TEXT
            if test == index:
                color = GREEN if value == 0 else ORANGE
                draw.rounded_rectangle((505, y-6, 891, y+23), radius=7, fill=RULE)
            label(518, y, f"{subset}    sum {index}", 18, color, test == index)
            number = str(value).replace("-", "−")
            label(879, y, number if value else "0  ←  match", 18, GREEN if value == 0 else color, True, "rt")

        label(512, 421, "Height = stored sum   ·   t = 1/16", 15, SOFT)
        draw.line((40, 478, 905, 478), fill=RULE, width=2)
        label(41, 495, "4 pairs × 2 bits = 8 independent bits", 19, heavy=True)
        label(904, 495, "2⁸ = 256 constructed patterns", 19, CYAN, True, "rt")
        label(41, 527, "In general, |A| × |B| × |K| bits give cubic growth for balanced blocks.", 17, SOFT)
        return image

    return frame


def render(output, regular_font, bold_font):
    frame = make_renderer(regular_font, bold_font, rational_example())
    phases = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 2))
    frames, durations = [], []
    for i, (pair, test) in enumerate(phases):
        # Shallow changing view keeps the same labels readable as the cube turns.
        for j in range(5):
            angle = 0.39 + 0.21 * (1 - cos(2 * pi * (i * 5 + j) / 30)) / 2
            frames.append(frame(angle, pair, test).quantize(colors=96, dither=Image.Dither.NONE))
            durations.append(100 if j < 4 else (1450 if test == CHOICES[pair] else 740))
    frames[0].save(
        output, save_all=True, append_images=frames[1:], duration=durations,
        loop=0, disposal=1, optimize=True,
    )
    with Image.open(output) as animation:
        assert animation.size == SIZE and animation.n_frames == len(frames)
        actual_duration = 0
        for i in range(animation.n_frames):
            animation.seek(i)
            actual_duration += animation.info["duration"]
        assert actual_duration == sum(durations)
    print(f"{output.name}: {len(frames)} frames, {sum(durations)/1000:.2f}s, {output.stat().st_size:,} bytes")
    print("Checked all 16 almost-principal determinants and all 64 principal minors with exact rationals.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular-font", type=Path, required=True)
    parser.add_argument("--bold-font", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("subset-encoding.gif"))
    args = parser.parse_args()
    render(args.output, args.regular_font, args.bold_font)
    archive_path = args.output.with_name("subset-encoding-explorer.zip")
    with ZipFile(archive_path, "w") as archive:
        info = ZipInfo("index.html", (2026, 11, 26, 0, 0, 0))
        info.external_attr = 0o644 << 16
        archive.writestr(info, Path(__file__).with_name("index.html").read_bytes(), compress_type=ZIP_DEFLATED)
