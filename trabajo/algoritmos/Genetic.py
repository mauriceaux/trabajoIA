# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 15:53:26 2019

@author: mauri
"""

import numpy as np
import random
from datetime import datetime
from collections import deque

class Genetic:
    def __init__(self, problem, maximize=True, n=20):
        self.problem = problem
        self.n = n
        self.poblacion = []
        self.bestCost = None
        self.bestState = None
        self.numGenerations = 100
        random.seed(1)
        
    def genInitialPobl(self):
        for _ in range(self.n):
            rnd = self.problem.getValidRandomState()
            cost = self.problem.evalObj(rnd)
            cost *= -1 if not self.problem.getMaximize() else 1
            self.poblacion.append([cost,self.problem.encodeState(rnd)])
        
        self.poblacion.sort(key=self.sortCost, reverse=True)
            
    def optimize(self):
        self.startTime = datetime.now()
        self.genInitialPobl()
        self.iterations = 0
        for i in range(self.numGenerations):
            self.iterations += 1
            print("iteracion {} \t cost {}\t ".format(i, round(self.poblacion[0][0])), end='\r')
            selected = np.array(self.poblacion)[0:10,1:]
#            print (selected)
            newGeneration = self.createNewGeneration(selected)
#            print(len(newGeneration))
#            exit()
            self.poblacion += newGeneration
            self.poblacion.sort(key=self.sortCost, reverse=True)
            while len(self.poblacion) > self.n:
                self.poblacion.pop(-1)
        print("\n")
        
        self.besState = self.poblacion[0][1]
        self.bestCost = self.poblacion[0][0]
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds
        
    def createNewGeneration(self, selected):
        hijos = []
        for i in range(selected.shape[0]-1):
            for j in range(selected.shape[0]-1):
                if i == j: continue
                corte = round(random.random() * (self.problem.getDim()[0] - 1))            
                h1 = np.concatenate([selected[i,0][0:corte], selected[j,0][corte:]])
                h2 = np.concatenate([selected[j,0][0:corte], selected[i,0][corte:]])
                swap1 = round(random.random() * (self.problem.getDim()[0] - 1))
                swap2 = round(random.random() * (self.problem.getDim()[0] - 1))
                val = h1[swap1]
                h1[swap1] = h1[swap2]
                h1[val]
                val2 = h2[swap1]
                h2[swap1] = h2[swap2]
                h2[val2]
                for hijo in [h1,h2]:
                    dec = self.problem.decodeSt(hijo)
                    if(self.problem.getFactibility(dec)):
                        cost = self.problem.evalObj(dec)
                        cost *= -1 if not self.problem.getMaximize() else 1
                        hijos.append([cost,hijo])
        return hijos
                    
            
        
        
    def sortCost(self,val):
        return val[0]
        
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.problem.getMaximize() else -1)
        
        
        