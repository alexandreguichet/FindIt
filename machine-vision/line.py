# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:41:08 2021

@author: Alexandre
"""

import math
import sys
 
sweepline = True            # use sweep line algorithm?
delta = 5.0                 # collision radius
 
class Point:
    """ A point P(x, y) in 2D space
    """
 
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
 
    def __repr__(self):
        return "P(%g, %g)" % (self.x, self.y)
 
    def __getitem__(self, index):
        return [int(self.x), int(self.y)][index]
    
class Vector:
    """ A vector v(x, y) in 2D space
    """
 
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    def mag(self):
        """ magnitude of the vector
        """
 
        return math.hypot(self.x, self.y)
 
    def norm(self):
        """ return the normalized vector or (0, 0)
        """
 
        a = self.mag()
 
        if a*a < 1.0e-16:
            return Vector(1, 0)
 
        return Vector(self.x / a, self.y / a)
 
    def __repr__(self):
        return "P(%g, %g)" % (self.x, self.y)
 
 
 
def diff(p, q):
    """ difference vector (q - p)
    """
 
    return Vector(q.x - p.x, q.y - p.y)
 
 
 
class Line:
    """ A line segment between two points
    """
 
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.parent = self
        
    def __repl__(self):
        return "Line(%r, %r)" % (self.p, self.q)
        
    def __getitem__(self, index):
        return (self.p, self.q)[index]
        
    def join(self, other):
        sp = self.root()
        op = other.root()
 
        op.parent = sp
 
    def root(self):
        if self.parent == self:
            return self
 
        self.parent = self.parent.root()
        
        return self.parent
 
    def __lt__(self, other):
        repr(self) < repr(other)
    
def within(p, dx, r):
    """ Is p within r of point (dx, 0)?
    """
 
    x = p.x - dx
    y = p.y
    
    return x*x + y*y <= r*r
 
def rot(p, u):
    """ Rotate point p to a coordinate system aligned with u.
    """
 
    return Point(p.x * u.x + p.y * u.y,
                -p.x * u.y + p.y * u.x)
 
def intersects(s, t, r):
    """ Do the line segments s and t collide with a radius r
    """
 
    ds = diff(s[0], s[1])
    ss = ds.mag()    
    u = ds.norm()
    
    a0 = rot(diff(s[0], t[0]), u)
    a1 = rot(diff(s[0], t[1]), u)
 
    if a0.y * a1.y < -0.9 * r * r:
        a = -a0.y * (a1.x - a0.x) / (a1.y - a0.y) + a0.x
        
        if 0 <= a <= ss: return True
    
    if -r <= a0.y <= r and -r <= a0.x <= ss + r:
        if 0 <= a0.x <= ss: return True    
        if a0.x < 0 and within(a0, 0, r): return True
        if a0.x > ss and within(a0, ss, r): return True
    
    if -r <= a1.y <= r and -r <= a1.x <= ss + r:
        if 0 <= a1.x <= ss: return True    
        if a1.x < 0 and within(a1, 0, r): return True
        if a1.x > ss and within(a1, ss, r): return True
    
    dt = diff(t[0], t[1])
    tt = dt.mag()    
    v = dt.norm()
    
    b0 = rot(diff(t[0], s[0]), v)
    b1 = rot(diff(t[0], s[1]), v)
 
    if 0 <= b0.x <= tt and -r <= b0.y <= r: return True
    if 0 <= b1.x <= tt and -r <= b1.y <= r: return True
       
    return False
