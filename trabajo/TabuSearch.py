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
        
    def optimize(self):
        
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        self.startTime = datetime.now()
        currState = self.problem.getValidRandomState()
        self.bestState = currState
        bestCandidate = currState
        self.bestCost = self.problem.evalObj(currState)
#        highTabu = currState
        self.bestCost *= 1 if self.problem.getMaximize() else -1
        self.tabuList.append(currState)
        bestCandidateCost = self.problem.evalObj(bestCandidate)
        bestCandidateCost *= 1 if self.problem.getMaximize() else -1
        maxRetry = self.problem.getDim()[0]
        tries = 0
#        print("tabu search optimize")
#        while self.iterations < self.numIter and maxRetry > tries:
        distance = 20
        while maxRetry > tries:
#            print(tries)
            self.iterations += 1
            print("Tabu search -- iteracion {}       cost {}          distance {}      ".format(self.iterations, self.getBestCost(), distance), end='\r')
            
            dropout = 0.0
                
            neighborhood = self.obtainValidNeighbors(currState, distance, dropout)
#            print(len(neighborhood))
#            exit()
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
#                        print("ya visitado")
                        break
#                print(found)
                
#                if (not found or len(candidatesCosts) == 0 or neighborCost > candidatesCosts[np.argmax(candidatesCosts)]):
                if (not found):
#                if neighborCost > bestCandidateCost:
                    candidates.append(neighbor)
                    candidatesCosts.append(neighborCost)
                    self.tabuList.append(neighbor)
#                    assigned = True
                    
#                exit()
#            print(len(self.tabuList))
            
            if len(candidatesCosts) < 1:
                tries+=1
#                print("2 no se encuentran movimientos para el punto en curso, generando uno nuevo")
                distance += 1
#                while True:
#                    _currState = self.problem.getValidRandomState()
#                    f = False
#                    for tabu in self.tabuList:
#                        if(np.all(tabu == _currState)):
#                            f = True
#                            break
#                    if not f: 
##                        print(_currState)
#                        currState = _currState
#                        break
                continue
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
                tries += 1
                distance += 1
#                while True:
#                    _currState = self.problem.getValidRandomState()
#                    f = False
#                    for tabu in self.tabuList:
#                        if(np.all(tabu == _currState)):
#                            f = True
#                            break
#                    if not f: 
##                        print(_currState)
#                        currState = _currState
#                        break
#                continue
            
            
#            else: 
#                tries += 1
##                dif = maxRetry - tries
#                while True:
#                    _currState = self.problem.getValidRandomState()
#                    f = False
#                    for tabu in self.tabuList:
#                        if(np.all(tabu == _currState)):
#                            f = True
#                            break
#                    if not f: 
##                        print(_currState)
#                        currState = _currState
#                        break
#                if dif < 1:
#                    print("morire")
#                    print(currState)
                
            
#            print("elementos tabu {}".format(len(self.tabuList)))
                
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds / 1000
        print('\n')
       
        
        return
        
    
        
    def obtainValidNeighbors(self, currState, distance, dropout=0.0):
#        distance = self.distance
#        dropout=0.0
        neighbors = self.problem.getValidNeighborhood(currState, distance, dropout)
#        movs = np.zeros()
        return neighbors
    
    
    
    def getBestCost(self):
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        