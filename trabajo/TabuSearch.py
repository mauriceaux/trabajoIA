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
        self.distance = 3
        self.tabuList = deque([], maxTabuSize)
        self.tabuCostList = deque([], maxTabuSize)
        
    def optimize(self):
        
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        self.startTime = datetime.now()
        currState = self.problem.getValidRandomState()
        self.bestState = currState
        bestCandidate = currState
        self.bestCost = self.problem.evalObj(currState)
        self.bestCost *= 1 if self.problem.getMaximize() else -1
        self.tabuList.append(currState)
        bestCandidateCost = self.problem.evalObj(bestCandidate)
        bestCandidateCost *= 1 if self.problem.getMaximize() else -1
        self.tabuCostList.append(bestCandidateCost)
        maxRetry = 20
        tries = 0
        distance = 1
        while maxRetry > tries:
#            print(tries)
            self.iterations += 1
            print("Tabu search -- iteracion {}       cost {}          distance {}      ".format(self.iterations, self.getBestCost(), distance), end='\r')
            
            dropout = 0.0
                
            neighborhood = self.obtainValidNeighbors(currState, distance, dropout)
            candidates = []
            candidatesCosts = []
            for neighbor in neighborhood:
                neighbor = np.array(neighbor)
                neighborCost = self.problem.evalObj(neighbor)
                neighborCost *= 1 if self.problem.getMaximize() else -1

                found = False
                for tabu in self.tabuList:
                    if(np.all(tabu == neighbor)):
                        found = True
                        break
                    
                if (not found):
                    self.tabuList.append(neighbor)
                    self.tabuCostList.append(neighborCost)
                    candidates.append(neighbor)
                    candidatesCosts.append(neighborCost)
                    

            if len(candidatesCosts) < 1:
                tries+=1
                distance+= 1 if distance +1 < (self.problem.getMaxValue()/2)  else 0
                idx = np.argmax(np.array(self.tabuCostList))
                candidates.append(self.tabuList[idx])
                candidatesCosts.append(self.tabuCostList[idx])
            bestCanIdx = np.argmax(np.array(candidatesCosts))
            bestCandidate = candidates[bestCanIdx]
            bestCandidateCost = candidatesCosts[bestCanIdx]
#            self.tabuList.append(bestCandidate)
            currState = bestCandidate
            if bestCandidateCost > self.bestCost:
                
                self.costHistory.append(bestCandidateCost)
                self.bestState = bestCandidate
                self.bestCost = bestCandidateCost
                tries = 0
                distance -= 1 if distance -1 >0 else 0
            else:
                distance+= 1 if distance +1 < (self.problem.getMaxValue()/2)  else 0
            
#                distance = 5
            
#                distance += 1
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds / 1000
        print('\n')
        return
        
    
        
    def obtainValidNeighbors(self, currState, distance, dropout=0.0):
        neighbors = []
        encCurrentState = self.problem.encodeState(currState)
#        print(encCurrentState)
        #VENTANA DEL 5% DE LOS REGISTROS
        total = len(encCurrentState)
        for pos in range(total):
            st = encCurrentState
            for i in [-1,1]:
                st[pos] += distance*i
                if st[pos] > self.problem.getMaxValue():
                    continue
#                    st[pos] = self.problem.getMaxValue()
                if st[pos] < self.problem.getMinValue():
#                    continue
                    st[pos] = self.problem.getMinValue()
                dec = self.problem.decodeSt(st)
                valid = self.problem.getFactibility(dec)
                if valid:
                    neighbors.append(dec)
        
        return neighbors
    
    
    
    def getBestCost(self):
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        