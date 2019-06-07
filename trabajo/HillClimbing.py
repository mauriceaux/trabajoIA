# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:30:52 2019

@author: mauri
"""
import numpy as np
from datetime import datetime

class HillClimbing:
    
    def __init__(self, problem, maximize=True, numN = 5):
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
        self.iterations += 1
#        EN LA PRIMERA EJECUCIÓN SE MARCA EL INICIO Y SE SELECCIONA UN STATE AL AZAR
        if self.currState is None:
            self.startTime = datetime.now()
            self.currState = self.problem.getValidRandomState()
            
#        EVALÚO SI MEJORO LA SOLUCIÓN                    
        currCost = self.problem.evalObj(self.currState)
        self.costHistory.append(currCost)
        currCost *= 1 if self.maximize else -1
        if self.bestCost is None or currCost > self.bestCost:
            #SI ENCONTRÉ UNA MEJOR SOLUCIÓN, ACTUALIZO
            self.bestCost = currCost
            self.bestState = self.currState
            self.x = self.problem.getX(self.currState)
        #OBTENGO LOS VECINOS DEL STATE ACTUAL
        neighbors = self.obtainValidNeighbors(self.currState)
        
        if(len(neighbors) > 0):
            #EVALUO LA FUNCIÓN OBJETIVO PARA CADA VECINO
            neighborCosts = []        
            for neighbor in neighbors:
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
            if bestNeighbor > self.bestCost:
                self.currState = neighbors[bestNeighborCostIdx]
                return self.optimize()
        print("mejor solución encontrada :)")
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds / 1000
        
        return
        
    
        
    def obtainValidNeighbors(self, currState):
        distance = 10
        neighbors = self.problem.getValidNeighborhood(currState, distance, dropProb=0.0)        
        return neighbors
    
    
    
    def getBestCost(self):
        return self.bestCost * (1 if self.maximize else -1)
    
    
        
        