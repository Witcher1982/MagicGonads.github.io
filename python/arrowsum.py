def sigma(n,m=1,f=lambda x:x):
    return [j for j in [0] for x in range(m,n+1) for j in [j+f(x)]] if n>m else 0
def integral(f,m=-1,n=1,d=1):
    return sigma(n*d,m*d,lambda i: f(i/d)/d)
def contsum(f,m=0,n=1,d=1):
    return [j for j in [0] for x in list(range(int(min(m,n)*d+0.5),int(max(m,n)*d+1.5)))[::(1,-1)[m>n]] for j in [j+f(x/d)]]
def invsum(f,m=0,n=1,d=1):
    return [j for j in [0] for x in list(range(int(min(m,n)/d+0.5),int(max(m,n)*d+1.5)))[::(1,-1)[m>n]] for j in [j+f(x*d)]]
class arrow:
    def _sum(m,n,d,f):
        return [j for j in [0] for x in list(range(int(min(m,n)/d+0.5),int(max(m,n)*d+1.5)))[::(1,-1)[m>n]] for j in [j+f(x*d)]][-1]
    def crop(self,l=0):
        it = arrow(self.it)
        if l:
            while len(it)>l:
                del it[-1]
        else:
            while it[-1]==0 and len(it)>1:
                del it[-1]
        return it
    def sum(self):
        it = self.crop()
        l = len(it)
        s = ''
        b = 0
        for i in list(range(1,l)):
            if i == 1:
                s+= str(it[i])
            elif i == l-1:
                s+= '+'+str(it[i])+'*x'+')'*b
            else:
                s+= '+arrow._sum(0,x-'+str(i)+','+str(self.s)+',lambda x:'+str(it[i])
                b+=1
        print(s)
        print('lambda x'+': '+str(it[0])+'+arrow._sum(0,x-1,'+str(self.s)+',lambda x:'+s+'-0'+')')
        return lambda x: it[0]+arrow._sum(0,x-1,self.s,eval('lambda x:'+s+'-0'))
    @classmethod
    def func(cls,f,s=1,l=10):
        d = [f]
        it = [f(0)]
        for i in range(l):
            if i:
                d += [lambda x,j: d[j-1](x+s,j-1)-d[j-1](x,j-1)]
            else:
                d += [lambda x,j: d[0](x+s)-d[0](x)]
            it+=[d[i+1](0,len(d)-1)]
        return cls(it,s)
    def __init__(self,it,s=1):
        self.s = s
        try:
            it.__iter__
            self.it = list(it)
        except AttributeError:
            self.it = [it]
    def __iter__(self):
        return self.it.__iter__()
    def __str__(self):
        return 'arrow('+str(self.it)+(','+str(self.s))*(self.s!=1)+')'
    __repr__ = __str__
    def __len__(self):
        return len(self.it)
    def __getitem__(self,key):
        try:
            return self.it[key]
        except IndexError:
            return 0
    def __setitem__(self,key,value):
        if key>=len(self):
            self.it+=[0]*(key-len(self)-1)
            self.it+=[value]
        else:
            self.it[key]=value
    def __delitem__(self,key):
        del self.it[key]
    def __missing__(key):
        return 0
    def __neg__(self):
        return -1*self
    def __add__(self,other):
        it = arrow(other)
        for i in range(max(len(it),len(self))):
            it[i]+= self[i]
        return arrow(it)
    __radd__ = __add__
    def __sub__(self,other):
        it = (-arrow(other)).it
        for i in range(max(len(it),len(self))):
            it[i]+= self[i]
        return arrow(it)
    def __rsub__(self,other):
        it = (arrow(other)).it
        se = -arrow(self)
        for i in range(max(len(it),len(self))):
            it[i]+= self[i]
        return arrow(it)
    def __mul__(self,other):
        ot = arrow(other)
        if len(self)+len(ot) != max(len(ot),len(self))+1:
            raise TypeError('Extra growth not supported')
        s = len(self)>len(ot)
        it = arrow((ot,self)[s])
        for i in range(len((ot,self)[s])):
            it[i]*= (self,ot)[s][0]
        return arrow(it)
    __rmul__ = __mul__
    def __truediv__(self,other):
        ot = arrow(other)
        if len(self)+len(ot) != max(len(ot),len(self))+1:
            raise TypeError('Extra growth not supported')
        s = len(self)>len(ot)
        it = arrow(0)
        for i in range(len((ot,self)[s])):
            it[i] = self[(i,0)[s]]/ot[(i,0)[s]]
        return arrow(it)
    def __rtruediv(self,other):
        ot = arrow(other)
        if len(self)+len(ot) != max(len(ot),len(self))+1:
            raise TypeError('Extra growth not supported')
        s = len(self)>len(ot)
        it = arrow(0)
        for i in range(len((ot,self)[s])):
            it[i] = ot[(i,0)[s]]/self[(i,0)[s]]
        return arrow(it)