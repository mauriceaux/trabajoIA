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
    
    def __init__(self, problem, maximize=True, numIter = 100, maxTabuSize=10):
        
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
        highTabu = currState
        self.bestCost *= 1 if self.maximize else -1
        self.tabuList.append(currState)
        bestCandidateCost = self.problem.evalObj(bestCandidate)
        bestCandidateCost *= 1 if self.maximize else -1
        maxRetry = self.problem.getDim()[0]
        tries = 0
#        print("tabu search optimize")
#        while self.iterations < self.numIter and maxRetry > tries:
        while maxRetry > tries:
            
            self.iterations += 1
            print("Tabu search -- iteracion {} cost {}".format(self.iterations, self.getBestCost()), end='\r')
#            distance = (tries + 1) * self.distance
#            dropout = tries/tries+3 if tries > 0 else 0
            _currState = self.problem.makeMove(currState, tries, round(self.problem.getDim()[0]*1/3))
            distance = 1
            dropout = 0.0
            neighborhood = self.obtainValidNeighbors(_currState, distance, dropout)
            if len(neighborhood) == 0:
                tries+=1
                continue
#            print("neighborhood de currstate {} es \n {}".format(currState,neighborhood))
#            exit()
#            assigned = False
            candidates = []
            candidatesCosts = []
            for neighbor in neighborhood:
#                neighbor = self.problem.decodeSt(encNeighbor)
                neighbor = np.array(neighbor)
                neighborCost = self.problem.evalObj(neighbor)
                neighborCost *= 1 if self.maximize else -1
                
#                print("self.tabuList \n{} \nneighbor \n{} \nnp.any(self.tabuList == neighbor) {}".format(self.tabuList,neighbor,np.any(self.tabuList == neighbor)))
                found = False
                for tabu in self.tabuList:
                    if(np.all(tabu == neighbor)):
                        found = True
#                        print("encontrado en tabu")
#                        if neighborCost > bestCandidateCost:
#                            highTabu = neighbor
                        break
#                print(found)
                
#                if (not found or len(candidatesCosts) == 0 or neighborCost > candidatesCosts[np.argmax(candidatesCosts)]):
                if (not found):
#                if neighborCost > bestCandidateCost:
                    candidates.append(neighbor)
                    candidatesCosts.append(neighborCost)
#                    assigned = True
                    
#                exit()
            
            if len(candidatesCosts) < 1:
                tries+=1
                continue
            bestCanIdx = np.argmax(np.array(candidatesCosts))
#            print(bestCanIdx)
#            print(np.array(candidatesCosts[bestCanIdx]))
#            exit()
            bestCandidate = candidates[bestCanIdx]
            bestCandidateCost = candidatesCosts[bestCanIdx]
            self.tabuList.append(bestCandidate)
            currState = bestCandidate
#            currState = bestCandidate if assigned else highTabu
#            print("currState {} bestCandidateCost {}".format(currState, bestCandidateCost))
                    
#            bestCandidateCost = self.problem.evalObj(bestCandidate)
#            bestCandidateCost *= 1 if self.maximize else -1
            if bestCandidateCost > self.bestCost:
#                print("costo {}".format(bestCandidateCost))
                self.costHistory.append(bestCandidateCost)
                self.bestState = bestCandidate
#                self.x = self.problem.getX(bestCandidate)
                self.bestCost = bestCandidateCost
                
                tries = 0
            else: 
                tries += 1
                dif = maxRetry - tries
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
        return neighbors
    
    
    
    def getBestCost(self):
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        