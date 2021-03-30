# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:41:08 2021

@author: Alexandre
"""

class Line:
    def __init__(self, points):
        self.points = points
        self.parent = self
        
    def __getitem__(self, index):
        return self.points
        
    def join(self, other):
        sp = self.root()
        op = other.root()

        op.parent = sp

    def root(self):
        if self.parent == self:
            return self

        self.parent = self.parent.root()
        
        return self.parent