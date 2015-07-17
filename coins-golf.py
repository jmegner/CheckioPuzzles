from itertools import *
def golf(c):
 for v in count(1):
  f = 0
  for n in range(len(c)):
   for u in combinations(c,n+1):
    if sum(u)==v:
     f=1
  if not f:
   return v
