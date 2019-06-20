# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:59:16 2019

@author: mauri
"""
import numpy as np
import copy
from numpy.random import choice
import random
from collections import deque
from datetime import datetime


class Ants:
    class Ant:
        def __init__(self, inicio, direccion, bestCost, problem, movsPosibles, nombre="hormiga"):
            self.stateInicio = inicio
            self.direccion = direccion
            self.camino = []
            self.bestCost = bestCost
            self.problem = problem
            self.stateActual = None
            self.movsPosibles = movsPosibles
            self.volviendo = False
            self.nombre = nombre
            self.distancia = 1
            self.bestState = None
            
        def elegirAccion(self, stateActual, pheromones, subProblmNum):
            t = tuple(copy.deepcopy(self.stateActual))
            self.direccion = random.choice([-1,1])
            
            if t in pheromones:
                self.direccion = random.choice([-1,1])
                movs = copy.deepcopy(pheromones[t][0][1])
                movs = np.array(movs, dtype=float)
                if np.sum(movs) > 0:
                    movs *= 1.0/np.sum(movs)
                    movs = np.array(movs)
                    return choice(movs.shape[0], p=movs)
#            limInf, limSup = self.problem.getSubSampleLimits(self.numSubSample)
#            return random.randint(limInf, limSup)
            minN, maxN = self.problem.getSubSampleLimits(subProblmNum)
            return random.randint(minN, maxN)
#            return random.randint(0, self.problem.getMaxValue()-1)
            
        def dejarFeromonas(self, pheromones, state, direccion, mov, rastro):
            t = tuple(copy.deepcopy(state))
            zeros = np.zeros(len(t))
            zeros[mov] = rastro
            mov = zeros
            if pheromones is None or t not in pheromones:
                pheromones[t] = []
                pheromones[t].append([direccion, mov])
            else:
                if len(np.where(np.array(pheromones[t])[:,0] == self.direccion)[0]) > 0:
                    idx = np.where(np.array(pheromones[t])[:,0] == self.direccion)[0][0]
                    pheromones[t][idx][1] += (pheromones[t][idx][1] + mov)
                    pheromones[t][idx][1] = np.clip(pheromones[t][idx][1], 0, 50)
                else:
                    pheromones[t].append([direccion, mov])
            
            
            
        def paso(self, pheromones, subPrbNum):
            if self.stateActual is None:
                self.stateActual = self.stateInicio
                
            if self.volviendo and len(self.camino) > 0:
                direccion, pos = self.camino[-1]
                nuevoState = copy.deepcopy(self.stateActual)
                nuevoState[pos] -= direccion
                nuevoState = np.clip(nuevoState, self.problem.getMinValue(), (self.problem.getMaxValue() -1),out=nuevoState)
                self.stateActual = nuevoState
                self.camino.pop(-1)
            else:
                currCost = self.problem.evalObj(self.problem.decodeSt(self.stateActual))
                currCost *= -1 if not self.problem.getMaximize() else 1
                if self.bestCost is None:
                    self.bestCost = currCost
                
                if self.bestCost < currCost:
                    self.bestCost = currCost
                    #ENCONTRE COMIDA, VUELVO
                    self.volviendo = True
                    self.bestCost = currCost
                    return
                self.volviendo = False
                nuevoState = copy.deepcopy(self.stateActual)
                accion = self.elegirAccion(self.stateActual, pheromones, subPrbNum)
                
                while accion >= self.problem.getMaxValue():
                    accion -= len(self.stateActual)
#                print(accion)
                
                nuevoState[accion] += self.direccion * self.distancia if self.problem.getMinValue() <= nuevoState[accion] + self.direccion < self.problem.getMaxValue() else 0
                nuevoState = np.clip(nuevoState, self.problem.getMinValue(), (self.problem.getMaxValue() -1),out=nuevoState)
                
                if self.problem.getFactibility(self.problem.decodeSt(nuevoState)):
                    rastro = 20
                    if len(self.camino) > 0:
                        self.dejarFeromonas(pheromones, self.stateActual, self.camino[-1][0], self.camino[-1][1], rastro)
                    self.stateActual = nuevoState
                    self.camino.append([self.direccion, accion])            
                    
                
    
    def __init__(self, problem):
        self.problem = problem
        self.nest = self.problem.encodeState(self.problem.getValidRandomState())
        self.movsPosibles = self.nest.shape[0]
        self.pheromones = {}
        self.ants = deque([],20)
        self.bestCost = None
        
        np.random.seed(1)
        random.seed(1)
        
    def addAnt(self, direccion):
        ant = Ants.Ant(self.nest, direccion, self.bestCost, self.problem, self.movsPosibles, nombre=len(self.ants))
        ant.distancia = random.randint(0, 20)
        ant.nombre = "hormiga {}".format(len(self.ants))
        self.ants.append(ant)
        
    def optimize(self, winSize = 0.1):
        maxTries = 100
        iteration = 0
        numSample = 0
        epochs = 2
        self.problem.setWinSize(winSize)
        self.startTime = datetime.now()
        self.iterations = 0
#        print(self.problem.getNumSubProb())
#        for subProbN in range(self.problem.getNumSubProb()):
#            print(self.problem.getSubSampleLimits(subProbN))
#        exit()
        for _ in range(epochs):
            for subProbN in range(self.problem.getNumSubProb()):
                self.ants = deque([],20)
                self.pheromones = {}
                for i in range (100):
        #        i = 0
        #        while iteration < maxTries:
                    self.iterations += 1
                    self.addAnt(random.randint(-1,1))
                        
                    
                    for ant in self.ants:
                        ant.paso(self.pheromones, subProbN)
                        if len(self.pheromones) > 200:
                            minimo = None
                            for f in self.pheromones:
                                if minimo is None: minimo = f
                                if np.all(self.pheromones[f][0][1] < self.pheromones[minimo][0][1]): 
                                    minimo = f
                            del self.pheromones[minimo]
                            #LA HORMIGA ENCONTRO UN MAXIMO
                        if self.bestCost is None or self.bestCost < ant.bestCost:
                            self.bestCost = ant.bestCost
                            self.nest = ant.stateActual
                            self.bestState = ant.stateActual
        #                    iteration = 0
        #                else:
        #                    iteration += 1
        #                    numSample = numSample + 1 if numSample < self.problem.getSubSampleNumber() else 0
                    self.evaporarFeromonas()
                    print("iteracion {} \t tamaño mapa feromonas {} tamaño colonia {} cost {}\t ".format(self.iterations, len(self.pheromones), len(self.ants), round(self.getBestCost())), end='\r')
    #            i+=1
        print("\n")
        print("mejor encontrado {}".format(self.getBestCost()))
        self.endTime = datetime.now()
        self.execTime = (self.endTime - self.startTime).microseconds 
        
    def evaporarFeromonas(self):
        for item in self.pheromones:
            for direccion in self.pheromones[item]:
                for pos in direccion[1:]:
                    ones = np.ones(len(pos)) * -1
                    pos += ones
                    
                    np.clip(pos, 0, 50,out=pos)
                        
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.problem.getMaximize() else -1)
                        