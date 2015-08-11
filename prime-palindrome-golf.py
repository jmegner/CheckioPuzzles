def golf(n):
 while 1:
  n+=1
  if `n`==`n`[::-1]and all(n%x for x in range(2,n)):
   return n