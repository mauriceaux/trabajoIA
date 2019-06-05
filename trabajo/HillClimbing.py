# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:30:52 2019

@author: mauri
"""
import numpy as np
from datetime import datetime

class HillClimbing:
    
    def __init__(self, problem, maximize=True):
        self.maximize = maximize
        self.problem = problem
        self.bestCost = None
        self.bestState = None
        self.currState = None
        self.iterations = 0
        self.startTime = None
        self.endTime = None
        self.execTime = None
        
    def optimize(self):
        self.iterations += 1
        if self.currState is None:
            self.startTime = datetime.now()
            self.currState = self.getValidRandomState()
            
        currCost = self.problem.evalObj(self.currState)
        if self.bestCost is None or self.bestCost > currCost:
            self.bestCost = currCost
            self.minState = self.currState
        neighbors = self.obtainValidNeighbors(self.currState)
        
        neighborCosts = []        
        for neighbor in neighbors:
            neighborCosts.append(self.problem.evalObj(neighbor))
        
        bestNeighborCostIdx = -1
        if self.maximize:
            bestNeighborCostIdx = np.argmax(neighborCosts)
            if neighborCosts[bestNeighborCostIdx] > self.bestCost:
                self.currState = neighbors[bestNeighborCostIdx]
                self.bestState = neighbors[bestNeighborCostIdx]
                self.bestCost = neighborCosts[bestNeighborCostIdx]
                self.optimize()
        else:
            bestNeighborCostIdx = np.argmin(neighborCosts)    
            if neighborCosts[bestNeighborCostIdx] < self.bestCost:
                self.currState = neighbors[bestNeighborCostIdx]
                self.bestState = neighbors[bestNeighborCostIdx]
                self.bestCost = neighborCosts[bestNeighborCostIdx]
                self.optimize()
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).miliseconds
        return
        
    def getValidRandomState(self):
        valid = False
        rndState = None
        while not valid:
            rndState = np.random.randint(2, size=(self.problem.dim[0], self.problem.dim[1]))
            valid = self.problem.getFactibility(rndState)
        return rndState
        
    def obtainValidNeighbors(self, currState):
        neighbors = []
        print("eligiendo vecinos")
        while len(neighbors) <= 5:
            rndState = self.getValidRandomState()
#            print("np.where(np.array(neighbors == rndState)) {}".format((np.where(np.array(neighbors == rndState))[0])))
#            print("np.where(np.array(neighbors == rndState)) {}".format(len(np.where(np.array(neighbors == rndState))[0])))
#            exit()
#            print("np.where(np.array(neighbors == rndState)) {}".format(len(np.where(np.array(neighbors == rndState)))))
            
            if len(np.where(np.array(neighbors) == rndState)[0]) < 1:
                print("agregando")
                neighbors.append(rndState)
            else:
                print("si esta")
                print("random state {}".format(rndState))
                print("neighbors \n{}".format(neighbors))
        print("vecinos elegidos \n{}".format(neighbors))
        return neighbors
    
        
        