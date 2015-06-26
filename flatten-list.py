def flat_list(a):
    if len(a)==1: return[a[0]]+flat_list(a[1:])
    return a
