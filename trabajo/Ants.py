# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 12:59:16 2019

@author: mauri
"""
import numpy as np
from datetime import datetime
import copy
from numpy.random import choice
import random


class Ants:
    class Ant:
        def __init__(self, inicio, direccion, bestCost, problem, movsPosibles):
            self.stateInicio = inicio
            self.direccion = direccion
            self.camino = []
            self.bestCost = bestCost
            self.problem = problem
            self.stateActual = None
            self.movsPosibles = movsPosibles
            self.volviendo = False
            
        def elegirAccion(self, stateActual, pheromones):
            t = tuple(copy.deepcopy(stateActual))
            self.direccion = random.randint(-1,1)
            
            if t in pheromones:
                movs = pheromones[t][self.direccion]
                return choice(movs.shape[0], p=movs)            
            return round(random.random() * (stateActual.shape[0]-1))
            
            
        def paso(self, pheromones):
            if self.stateActual is None:
                self.stateActual = self.stateInicio
            currCost = self.problem.evalObj(self.problem.decodeSt(self.stateActual))
#            print("self.stateActual, currCost, self.bestCost {} {} {}".format(self.stateActual, currCost, self.bestCost))
            currCost *= -1 if not self.problem.getMaximize() else 1
            if self.bestCost is None:
                self.bestCost = currCost
                
            
            if self.bestCost < currCost:
                self.bestCost = currCost
#                print("volviendo")
#                exit()
                #ENCONTRE COMIDA, VUELVO
                self.volviendo = True
                self.bestCost = currCost
                state = copy.deepcopy(self.stateInicio)
                rastro = 5
                for pos in self.camino:
                    mov = np.zeros(self.movsPosibles)
                    mov[pos] = rastro
                    t = tuple(copy.deepcopy(state))
                    if pheromones is None or t not in pheromones:
                        pheromones[t] = {}
                        pheromones[t][self.direccion] = mov
                    else:
                        
                        pheromones[t][self.direccion] = (pheromones[t][1] + mov)
                    if rastro > 0:
                        rastro -= 1
                    else:
                        break
                    state[pos] += self.direccion
            else:
#                print("dando el paso")
                nuevoState = copy.deepcopy(self.stateActual)
                accion = self.elegirAccion(self.stateActual, pheromones)
#                print("accion elegida {}".format(accion))
                nuevoState[accion] += self.direccion
                
                if self.problem.getFactibility(self.problem.decodeSt(nuevoState)):
#                    if self.direccion < 0:
#                        print("state actual: {}".format(self.stateActual))
#                        print("accion: {}".format(accion))
#                        print("state nuevo: {}".format(nuevoState))
                    self.stateActual = nuevoState
                    self.camino.append(accion)
    
    def __init__(self, problem):
        self.problem = problem
        self.nest = self.problem.encodeState(self.problem.getValidRandomState())
        self.movsPosibles = self.nest.shape[0]
        self.pheromones = {}
        self.ants = []
        self.bestCost = None
        np.random.seed(1)
        
    def addAnt(self, direccion):
        ant = Ants.Ant(self.nest, direccion, self.bestCost, self.problem, self.movsPosibles)
        self.ants.append(ant)
        
    def optimize(self):
        self.addAnt(1)
        
        for i in range (50):
#            self.addAnt(1)
            for ant in self.ants:
#                print("posicion inicio hormiga: {}".format(ant.stateInicio))
            
                ant.paso(self.pheromones)
#                print("mapa de feromonas \n{}".format(self.pheromones))
#                print("posicion hormiga: {}".format(ant.stateActual))
#                if ant.volviendo:
                    #LA HORMIGA ENCONTRO UN MAXIMO
                if self.bestCost is None or self.bestCost < ant.bestCost:
                    self.bestCost = ant.bestCost
            self.evaporarFeromonas()
            print("iteracion {} \t cost {}  ".format((i+1), round(self.getBestCost())), end='\r')
#        print("camino hormiga negativa {}".format(self.ants[1].camino))
        print("\n")
        print("mejor encontrado {}".format(self.getBestCost()))
        
    def evaporarFeromonas(self):
        print("\n")
        print(self.pheromones)
        exit()
        for item in self.pheromones:
            
            for direccion in item:
                
                for pos in direccion:
                    if(pos - 1) > 0:
                        pos -= 1
                        
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.problem.getMaximize() else -1)
                        