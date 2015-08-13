c=complex
def golf(h,p=(0,0)):
 if h:return min(abs(c(*p)-c(*x))+golf(h-{x,},x)for x in h)
 return 0