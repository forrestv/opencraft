import math
import operator

class v(list):
    def __init__(self,*args):
        if len(args) != 1:
            list.__init__(self,args)
        else:
            list.__init__(self,*args)
            
    def __add__(self, other): return v([operator.add(*x) for x in zip(self,other)])
    __radd__ = __add__
    def __sub__(self, other): return v([operator.sub(*x) for x in zip(self,other)])
    def __rsub__(self, other): return v([operator.sub(*x) for x in zip(other,self)])
    def __neg__(self): return v([operator.neg(x) for x in self])
    def __mul__(self, other):
        try:
            return v([operator.mul(*x) for x in zip(self,other)])
        except TypeError:
            return v([operator.mul(x,other) for x in self])
    __rmul__ = __mul__
    def __div__(self, other):
        try:
            return v([operator.div(*x) for x in zip(self,other)])
        except TypeError:
            return v([operator.div(x,other) for x in self])
    def __rdiv__(self, other):
        try:
            return v([operator.div(*x) for x in zip(other,self)])
        except TypeError:
            return v([operator.div(other,x) for x in self])
    def __mod__(self, other):
        try:
            return v([operator.mod(*x) for x in zip(self, other)])
        except TypeError:
            return v([operator.mod(x,other) for x in self])
            
    def copy(self): return v(self)
    
def zeros(n):
    return v([0. for x in range(n)])
    
def ones(n):
    return v([1. for x in range(n)])
    
from random import random as myrandom

def random(n=None, lmin=0.0, lmax=1.0):
    if n == None:
        return myrandom()
    dl = lmax-lmin
    return v([dl*myrandom()+lmin for x in range(n)])
    
def dot(a, b): return reduce(lambda x, y: x+y, a*b, 0.)
def norm(a): return math.sqrt(abs(dot(a,a)))
def sum(a):
    total = a[0]
    for x in a[1:]:
        total = total + x
    return total
    
sqrt=math.sqrt
arctan2=math.atan2
def sign(x):
    return x/abs(x)
cos=math.cos
sin=math.sin
tan=math.tan
