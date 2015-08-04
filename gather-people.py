def golf(g,t,r=0,v=[]):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        if(c not in v)*d*(t-d+1)>0:
            e+=golf(g,t-d,c,v+[c])
    return e
