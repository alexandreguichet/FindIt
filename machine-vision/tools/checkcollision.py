# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:16:18 2021

@author: Alexandre
"""
import math

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def mag(self):
        return math.hypot(self.x, self.y)
    
    def norm(self):
        a = self.mag()
        if (a*a < 1.0e-16):
            a = 1.0;
        return Vector(self.x/a, self.y/a)

class Segment():
    def __init__(self, p, q):
        self.p = p
        self.q = q
        
        
def diff(p, q):
    return Vector(q.x - p.x, q.y - p.y)

def dot(u, v):
    return u.x*v.x - u.y*v.y

def cross(u, v):
    return u.x * v.y - u.y * v.x

def coll(s, t, r):
    ds = diff(s.p, s.q)
    ss = ds.mag()
    
    ds = ds.norm()
    
    a0 = dot(ds, diff(s.p, t.p))
    a1 = dot(ds, diff(s.p, t.q))
    
    if ((a0 < 0) & (a1 < 0)): return False
    if ((a0 > ss) & (a1 > ss)): return False
    
    Q0 = Point(s.p.x + a0 * ds.x, s.p.y + a0 * ds.y)
    d0 = cross(ds, diff(Q0, t.p))
    
    Q1 = Point(s.p.x + a1 * ds.x, s.p.y + a1 * ds.y)
    d1 = cross(ds, diff(Q1, t.q))
    
    if d0 == d1:
        if (abs(d0) < r) & (((a0 > 0) & (a0 <= ss)) | ((a1 > 0) & (a1 <= ss))): 
            return True
        else: 
            return False
    
    if ((d0 < -r) & (d1 < -r)): return False;
    if ((d0 >  r) & (d1 >  r)): return False;
    
    apos = (r - d0) * (a1 - a0) / (d1 - d0) + a0
    aneg = (-r - d0) * (a1 - a0) / (d1 - d0) + a0

        
    if ((apos >= 0) & (apos <= ss)): return True
    if ((aneg >= 0) & (aneg <= ss)): return True   
    
    return False

def collision(s, t, r):
    return coll(s, t, r) | coll(t, s, r)

def check_collision(S, T, r):
    s0 = Point(S[0], S[1])
    s1 = Point(S[2], S[3])

    t0 = Point(T[0], T[1])
    t1 = Point(T[2], T[3])
    
    s = Segment(s0, s1)
    t = Segment(t0, t1)
    
    return collision(s, t, r)