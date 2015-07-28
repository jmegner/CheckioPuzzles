a,b,m=[0,1,1],[1,1,0],[0,1,2]
d={'ib':a+b,'ri':a+[1]*3,'uc':[2,1,3]+b,'ac':a+[1,2,0],'el':m+[2,1,0],'er':[3,0,2]+a,'ad':a+a}
def f(x,c,k):
 if x not in c:c[x]=sum(k[i+3]*f(x-i-1,c,k)for i in m)
 return c[x]
def fibgolf(s,x):return f(x,dict(enumerate(d[s[1:3]][:3])),d[s[1:3]])
