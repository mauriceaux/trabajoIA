#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:28:16 2019

@author: mauri
"""
import numpy as np

class CFLPProblem:
    def fitness(self, y):
        
        transporCost = y * self.TC
        
        x = np.zeros((self.nFacilites))
        for i in range(self.ncli):
            x[i] = np.count_nonzero(y[i]) > 0 ? 1 : 0
        openingCost = np.sum(x*self.FC)
        
        obj = openingCost + clientCost
        
        
#        y = np.zeros((len(self.facilities), len(self.cli)))
##        for i in range(len(facilities)):
##            for j in range(len(self.cli)):
#                
#        
#        
##        COSTO DE ABRIR UN FACILITY
#        
#        clientCost = 0
#        for j in self.facilities:
#            openingCost += x[j] * self.FC[j]
#        for j in range(self.facilities):
#            for i in range(self.cli):
#                clientCost += y[i,j] * self.TC[i,j]
#        
#        ce1 = -1
#        for i in range(self.cli):
#            for j in range(self.facilities):
#                ce1 += y[i,j]
#        ci1 = 0
#        for i in range(self.cli):
#            for j in range(self.facilities):
#                ci1 += y[i,j] - x[j]
                
        return [obj, ce1, ci1]
                
            
    def get_nobj(self):
        return 2
        
    
    def get_bounds(self):
        return ([0]*3, [1]*3)
        
import pygmo as pg
prob = pg.problem(CFLPProblem())
print(prob)