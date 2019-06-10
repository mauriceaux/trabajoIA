# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:30:52 2019

@author: mauri
"""
import numpy as np
from datetime import datetime

class HillClimbing:
    
    def __init__(self, problem, maximize=True, numN = 5, numIter = 200):
        self.numIter = numIter
        self.numN = numN
        self.maximize = maximize
        self.problem = problem
        self.bestCost = None
        self.bestState = None
        self.currState = None
        self.iterations = 0
        self.startTime = None
        self.endTime = None
        self.execTime = None
        self.x = None
        self.costHistory = []
        
    def optimize(self):
        best = None
        tries = 0
        maxTries = 10
        distance = 20
        
        dropout = 0.0
        currState = None
        print("Hill climbing --")
        while maxTries >= tries:
#        for i in range(self.numIter):
#            if maxTries < tries: break
#            dropout = 0.0 if dropout < 0.0 else dropout
#            dropout = 0.8 if dropout > 0.9 else dropout
            self._optimize(currState, distance, dropout)
#            print("******{}********".format(self.bestState))
            if best is None or self.bestCost > best:
                best = self.bestCost
                distance -= 1 if (distance -1)  > 1 else 0
#                distance = 1
                tries = 0
#                dropout -= 0.1
#                currState = self.currState
#                distance -= 10 if distance > 10 else 0
#                dropout -= 0.01 if dropout > 0.01 else 0.0
            else: 
                tries += 1
#                print("eligiendo state nuevo")
#                currState = self.currState
                distance+=1 
                
#                distance += 10
#                dropout += 0.1
            currState = self.currState
        self.bestCost = best
        print("\n")
    
    def _optimize(self, cState = None, distance = 10, dropOut = 0.0):
#        print("_optimize")
        self.iterations += 1
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        self.currState = cState
        if self.currState is None:
            self.startTime = datetime.now()
            self.currState = self.problem.getValidRandomState()
            
#        EVALÚO SI MEJORO LA SOLUCIÓN                    
        currCost = self.problem.evalObj(self.currState)
#        print("estado acual {} iteracion {}".format(self.currState,self.iterations))
        print("iteracion {} \t cost {}\t dropout {}\t distance {}              ".format(self.iterations, round(self.getBestCost()), dropOut, distance), end='\r')
        self.costHistory.append(currCost)
        currCost *= 1 if self.maximize else -1
        if self.bestCost is None or currCost > self.bestCost:
            #SI ENCONTRÉ UNA MEJOR SOLUCIÓN, ACTUALIZO
            self.bestCost = currCost
            self.bestState = self.currState
#            self.x = self.problem.getX(self.currState)
        #OBTENGO LOS VECINOS DEL STATE ACTUAL
        neighbors = self.obtainValidNeighbors(self.currState, distance, dropOut)
        
        if(len(neighbors) > 0):
            #EVALUO LA FUNCIÓN OBJETIVO PARA CADA VECINO
            neighborCosts = []       
            nArray = []
            for neighbor in neighbors:
#                neighbor = self.problem.decodeSt(encNeighbor)
                neighbor = np.array(neighbor)
                nArray.append(neighbor)
                neighborCosts.append(self.problem.evalObj(neighbor))
            
            bestNeighborCostIdx = -1
            #DEPENDIENDO DEL TIPO DE PROBLEMA, ELIJO AL MEJOR VECINO
            
            if self.maximize:
                bestNeighborCostIdx = np.argmax(neighborCosts)
            else:
                bestNeighborCostIdx = np.argmin(neighborCosts)
                
            bestNeighbor = neighborCosts[bestNeighborCostIdx]
            bestNeighbor *= 1 if self.maximize else -1
            
            #COMPARO EL OBJETIVO CON EL MEJOR ENCONTRADO
#            print("bestNeighbor {}, self.bestCost {}".format(bestNeighbor, self.bestCost))
            if bestNeighbor > self.bestCost:
                self.currState = nArray[bestNeighborCostIdx]
                return self._optimize(self.currState, distance, dropOut)
#        print("mejor solución encontrada :)")
#        print("\n")
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds / 1000
        
        return 
        
    
        
    def obtainValidNeighbors(self, currState, distance, dropout):
#        distance = 20
        neighbors = self.problem.getValidNeighborhood(currState, distance, dropout)        
        return neighbors
    
    
    
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        