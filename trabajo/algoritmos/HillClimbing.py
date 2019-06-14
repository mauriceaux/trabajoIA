# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:30:52 2019

@author: mauri
"""
import numpy as np
from datetime import datetime
import copy
import random

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
        distance = 1
        
        dropout = 0.8
        currState = None
        print("Hill climbing --")
        self.startTime = datetime.now()
        while maxTries >= tries:
            self._optimize(currState, distance, dropout)
            if best is None or self.bestCost > best:
                best = self.bestCost
                distance -= 1 if (distance -1)  > 1 else 0
                currState = self.currState
                tries = 0
            else: 
                tries += 1
                currState = self.currState
                distance+= 1 if distance +1 < (self.problem.getMaxValue()/2)  else 0
            
        self.bestCost = best
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds 
        print("\n")
    
    def _optimize(self, cState = None, distance = 10, dropOut = 0.0):
        
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        self.currState = cState
        
        if self.currState is None:
            self.currState = self.problem.getValidRandomState()
        
        print("inicio")
        neighbors = self.obtainValidNeighbors(self.currState, distance, dropOut)
#        print(len(neighbors))
#        exit()
        while len(neighbors) > 0:
            self.iterations += 1
            
                
            
    #        EVALÚO SI MEJORO LA SOLUCIÓN                    
            currCost = self.problem.evalObj(self.currState)
            print("iteracion {} \t cost {}\t dropout {}\t distance {}              ".format(self.iterations, round(self.getBestCost()), dropOut, distance), end='\r')
            
            currCost *= 1 if self.problem.getMaximize() else -1
            
            if self.bestCost is None or currCost > self.bestCost:
                #SI ENCONTRÉ UNA MEJOR SOLUCIÓN, ACTUALIZO
                self.costHistory.append(currCost)
                self.bestCost = currCost
                self.bestState = self.currState
            
            #OBTENGO LOS VECINOS DEL STATE ACTUAL
            neighbors = self.obtainValidNeighbors(self.currState, distance, dropOut)
            
            if(len(neighbors) > 0):
                #EVALUO LA FUNCIÓN OBJETIVO PARA CADA VECINO
                neighborCosts = []       
                nArray = []
                for neighbor in neighbors:
                    neighbor = np.array(neighbor)
                    nArray.append(neighbor)
                    cost = self.problem.evalObj(neighbor)
                    cost *= 1 if self.maximize else -1
                    neighborCosts.append(cost)
                
                bestNeighborCostIdx = -1
                #DEPENDIENDO DEL TIPO DE PROBLEMA, ELIJO AL MEJOR VECINO
                
                
                bestNeighborCostIdx = np.argmax(neighborCosts)
                                
                bestNeighbor = neighborCosts[bestNeighborCostIdx]
                
                #COMPARO EL OBJETIVO CON EL MEJOR ENCONTRADO
                if bestNeighbor > self.bestCost:
    #                print("\n")
    #                print("mejor vecino encontrado: {} best cost {}".format(bestNeighbor, self.bestCost))
                    self.currState = nArray[bestNeighborCostIdx]
#                    return self._optimize(self.currState, distance, dropOut)
        
        
        return 
        
    
        
    def obtainValidNeighbors(self, currState, distance, dropout):
        neighbors = []
        encCurrentState = self.problem.encodeState(currState)
        total = len(encCurrentState)
        
        for pos in range(total):
            if random.random() < dropout: continue
            st = copy.deepcopy(encCurrentState)
            for i in [-1,1]:
                st[pos] += distance*i
                if st[pos] > self.problem.getMaxValue():
                    continue
#                    st[pos] = self.problem.getMaxValue() -1
                if st[pos] < self.problem.getMinValue():
#                    continue
                    st[pos] = self.problem.getMinValue()
                
                dec = self.problem.decodeSt(st)
#                print(st)
                valid = self.problem.getFactibility(dec)
                if valid:
                    neighbors.append(dec)
        return neighbors
    
    
    
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.problem.getMaximize() else -1)
    
    
        
        