import itertools
def golf(h):return min(sum(((c[0]-p[0])**2+(c[1]-p[1])**2)**.5 for c,p in zip(r,((0,0),)+r)) for r in itertools.permutations(h))
