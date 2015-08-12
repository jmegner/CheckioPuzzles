from itertools import*
def golf(c):
 for v in count(1):
  if 1-any(sum(u)==v for u in combinations(c+[0]*len(c),len(c))):return v