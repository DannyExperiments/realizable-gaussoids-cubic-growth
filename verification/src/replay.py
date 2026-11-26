"""Exhaustive six-variable rational diagnostic; no external dependencies."""
from fractions import Fraction as Q
from itertools import product

def det(M):
    M=[list(map(Q,r)) for r in M]
    out=Q(1)
    for j in range(len(M)):
        i=next((i for i in range(j,len(M)) if M[i][j]),None)
        if i is None:
            return Q(0)
        if j!=i:
            M[j],M[i]=M[i],M[j]
            out=-out
        p=M[j][j]
        out*=p
        for i in range(j+1,len(M)):
            f=M[i][j]/p
            for k in range(j+1,len(M)):
                M[i][k]-=f*M[j][k]
    return out

def subs(items):
    return [tuple(k for i,k in enumerate(items) if mask>>i&1)
            for mask in range(2**len(items))]

K=(4,5)
u={4:1,5:2}
AB=list(product(range(2),range(2,4)))
groups=subs(K)
patterns=set()
t=Q(1,16)
for R in product(groups,repeat=len(AB)):
    M=[[int(i==j) for j in range(6)] for i in range(6)]
    for i in range(4):
        for k in K:
            M[i][k]=M[k][i]=t*(u[k] if i<2 else 1)
    for (i,j),S in zip(AB,R):
        M[i][j]=M[j][i]=t*t*sum(u[k] for k in S)
    for S in subs(range(6)):
        assert det([[M[i][j] for j in S] for i in S])>0
    got=[]
    for (i,j),want in zip(AB,R):
        zs=[S for S in groups
            if det([[M[r][c] for c in (j,)+S] for r in (i,)+S])==0]
        assert zs==[want]
        got.append(zs[0])
    patterns.add(tuple(got))
assert len(patterns)==256
print("256 distinct restricted CI patterns; all 16,384 principal determinants positive.")
