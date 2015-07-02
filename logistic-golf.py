def golf(m):d=[1e9]*len(m);d[0]=0;r(m,d,0);return 0 if d[-1]==1e9 else d[-1]
def r(m,d,i):
 for j,c in enumerate(m[i]):
  b=d[i]+c
  if c and b<d[j]:
   d[j]=b;r(m,d,j)
