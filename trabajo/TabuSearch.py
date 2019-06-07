# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:30:52 2019

@author: mauri
"""
import numpy as np
from datetime import datetime
from collections import deque

import sys
np.set_printoptions(threshold=sys.maxsize)

class TabuSearch:
    
    def __init__(self, problem, maximize=True, numIter = 100, maxTabuSize=100):
        
        self.numIter = numIter
        self.maximize = maximize
        self.problem = problem
        self.bestCost = None
        self.bestState = None
        self.bestCandidate = None
        self.currState = None
        self.iterations = 0
        self.startTime = None
        self.endTime = None
        self.execTime = None
        self.x = None
        self.costHistory = []
        
        self.tabuList = deque([], maxTabuSize)
        
    def optimize(self):
        
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        self.startTime = datetime.now()
        currState = self.problem.getValidRandomState()
        self.bestState = currState
        bestCandidate = currState
        self.bestCost = self.problem.evalObj(currState)
        self.bestCost *= 1 if self.maximize else -1
        self.tabuList.append(currState)
        bestCandidateCost = self.problem.evalObj(bestCandidate)
        bestCandidateCost *= 1 if self.maximize else -1
        while self.iterations < self.numIter:
            self.iterations += 1
            print("iteracion {} cost {}".format(self.iterations, bestCandidateCost), end='\r')
            neighborhood = self.obtainValidNeighbors(currState)
            for neighbor in neighborhood:
                
                neighborCost = self.problem.evalObj(neighbor)
                neighborCost *= 1 if self.maximize else -1
#                print("self.tabuList \n{} \nneighbor \n{} \nnp.any(self.tabuList == neighbor) {}".format(self.tabuList,neighbor,np.any(self.tabuList == neighbor)))
                found = False
                for tabu in self.tabuList:
                    if(np.all(tabu == neighbor)):
                        found = True
                        break
#                print(found)
                if (not found) and neighborCost > bestCandidateCost:
#                if neighborCost > bestCandidateCost:
                    bestCandidate = neighbor
#                exit()
                    
            bestCandidateCost = self.problem.evalObj(bestCandidate)
            bestCandidateCost *= 1 if self.maximize else -1
            if bestCandidateCost > self.bestCost:
#                print("costo {}".format(bestCandidateCost))
                self.costHistory.append(bestCandidateCost)
                self.bestState = bestCandidate
                self.x = self.problem.getX(bestCandidate)
                self.bestCost = bestCandidateCost
                
            self.tabuList.append(bestCandidate)
                
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds / 1000
        
       
        
        return
        
    
        
    def obtainValidNeighbors(self, currState):
        distance = 5
        neighbors = self.problem.getValidNeighborhood(currState, distance, dropProb=0.0)        
        return neighbors
    
    
    
    def getBestCost(self):
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        