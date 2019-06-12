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
            
        def elegirAccion(self, stateActual, pheromones):
            t = tuple(copy.deepcopy(stateActual))
            self.direccion = random.choice([-1,1])
            
            if t in pheromones:
                totFerMov = []
                dirs = []
#                print("********************")
#                print("********************")
                for item in pheromones[t]:
#                    print(item)
                    totFerMov.append(np.sum(item[1]))
                    dirs.append(item[0])
                
#                exit()
                totFerMov = np.array(totFerMov, dtype=float)
                
                totFerMov *= 1.0/np.sum(totFerMov)
#                if np.all(totFerMov != totFerMov):
#                    totFerMov = np.ones(totFerMov.shape)
#                print("********************")
#                print(totFerMov)
#                print(dirs)
#                exit()
#                if np.sum(totFerMov) > 0:
#                    self.direccion = choice(dirs, p=totFerMov) 
                self.direccion = random.choice([-1,1])
                
#                print(pheromones[t][0][1])
#                exit()
                movs = copy.deepcopy(pheromones[t][0][1])
                movs = np.array(movs, dtype=float)
                
                movs *= 1.0/np.sum(movs)
                movs = np.array(movs)
                print(t)
                print(movs)
                if np.sum(movs) > 0:
                    return choice(movs.shape[0], p=movs)
#                if np.all(totFerMov != totFerMov):
#                    movs = np.ones(movs.shape)
                
            return round(random.random() * (stateActual.shape[0]-1))
            
        def dejarFeromonas(self, pheromones, direccion, mov, rastro):
            t = tuple(copy.deepcopy(self.stateActual))
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
            
            
            
        def paso(self, pheromones):
            if self.stateActual is None:
                self.stateActual = self.stateInicio
            currCost = self.problem.evalObj(self.problem.decodeSt(self.stateActual))
#            print("self.stateActual, currCost, self.bestCost {} {} {}".format(self.stateActual, currCost, self.bestCost))
            currCost *= -1 if not self.problem.getMaximize() else 1
#            print("state actual {}".format(self.stateActual))
            if self.bestCost is None:
                self.bestCost = currCost
                
            
            if self.bestCost < currCost:
                self.bestCost = currCost
                #ENCONTRE COMIDA, VUELVO
                self.volviendo = True
                self.bestCost = currCost
#                state = copy.deepcopy(self.stateInicio)
            rastro = 20
            if len(self.camino) > 0:
                self.dejarFeromonas(pheromones, self.camino[-1][0], self.camino[-1][1], rastro)
                
            if self.volviendo and len(self.camino) > 0:
                direccion, pos = self.camino[-1]
                nuevoState = copy.deepcopy(self.stateActual)
                nuevoState[pos] -= direccion
                self.stateActual = nuevoState
                self.camino.pop(-1)
                print("hormiga {} camino en direccion {} en la posicion {} (volviendo)".format(self.nombre, direccion, pos))
                
            else:
                self.volviendo = False
                nuevoState = copy.deepcopy(self.stateActual)
                accion = self.elegirAccion(self.stateActual, pheromones)
                nuevoState[accion] += self.direccion if self.problem.getMinValue() <= nuevoState[accion] + self.direccion < self.problem.getMaxValue() else 0
                
                
                if self.problem.getFactibility(self.problem.decodeSt(nuevoState)):
                    self.stateActual = nuevoState
                    self.camino.append([self.direccion, accion])
                    
                print("hormiga {} camino en direccion {} en la posicion {}".format(self.nombre, self.direccion, accion))
            
            
                    
                
    
    def __init__(self, problem):
        self.problem = problem
        self.nest = self.problem.encodeState(self.problem.getValidRandomState())
        self.movsPosibles = self.nest.shape[0]
        self.pheromones = {}
        self.ants = []
        self.bestCost = None
        np.random.seed(1)
        random.seed(1)
        
    def addAnt(self, direccion):
        ant = Ants.Ant(self.nest, direccion, self.bestCost, self.problem, self.movsPosibles, nombre=len(self.ants))
        self.ants.append(ant)
        
    def optimize(self):
#        self.addAnt(-1)
#        for i in range(10):
            
        for i in range (15):
            if(len(self.ants) < 1):
                self.addAnt(random.randint(-1,1))
            
            for ant in self.ants:
#                print("posicion inicio hormiga: {}".format(ant.stateInicio))
#                print(len(self.pheromones))
                ant.paso(self.pheromones)
#                print(len(self.pheromones))
#                exit()
#                print("mapa de feromonas \n{}".format(self.pheromones))
#                print("posicion hormiga: {}".format(ant.stateActual))
#                if ant.volviendo:
                    #LA HORMIGA ENCONTRO UN MAXIMO
                if self.bestCost is None or self.bestCost < ant.bestCost:
                    self.bestCost = ant.bestCost
            self.evaporarFeromonas()
#            print("iteracion {} \t cost {}\t ".format(i+1, round(self.getBestCost())), end='\r')
#        print("camino hormiga negativa {}".format(self.ants[1].camino))
#        print("mapa de feromonas \n{}".format(self.pheromones))
        print("\n")
        print("mejor encontrado {}".format(self.getBestCost()))
        
    def evaporarFeromonas(self):
        for item in self.pheromones:
            for direccion in self.pheromones[item]:
#                print(direccion)
                for pos in direccion[1:]:
#                    print(pos)
                    ones = np.ones(len(pos)) * -1
                    pos += ones
                    
                    np.clip(pos, 0, 50,out=pos)
#        print(self.pheromones)
                        
    def getBestCost(self):
        if self.bestCost is None:
            return -1
        return self.bestCost * (1 if self.problem.getMaximize() else -1)
                        