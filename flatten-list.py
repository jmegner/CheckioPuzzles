def flat_list(a): return [a] if isinstance(a,int) else [] if not a else flat_list(a[0])+flat_list(a[1:])

