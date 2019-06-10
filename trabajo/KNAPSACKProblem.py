#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:28:16 2019

@author: mauri
"""

import numpy as np
import pandas as pd
import random

class KNAPSACKProblem:
    
    
    def __init__(self):
        
        self.maxRSIter = 500
#        self.nFacilities = None
#        self.ncli = None
#        self.TC = None
#        self.FC = None
#        self.dem = None
#        self.ICap = None
#        self.minY = None
#        self.minX = None
#        self.minObj = None
        self.seed = 1
        self.PESO_ITEMS = None
        self.MAX_CAPACITY = None
        self.req = None
    
    
    def evalObj(self, y):
        if self.PESO_ITEMS is None:
            raise Exception("pesos items no cargados!")
        if self.MAX_CAPACITY is None:
            raise Exception("no se definió el tamaño de la mochila!")
            
#        print("y \n{}\n* self.PESO_ITEMS \n{}\n".format(y, self.PESO_ITEMS))
        pesoItems = np.array(self.PESO_ITEMS)
#        print("y\n{}".format(pesoItems*y))
#        print("y\n{}".format(y))
        pesoItems = y * pesoItems
        
        capUsed = self.MAX_CAPACITY - np.sum(pesoItems, axis=1)
        itmExcl = self.PESO_ITEMS.shape[0] - np.sum(y)
#        obj = capUsed - itmExcl
        obj = capUsed 
#        print("OBJ {}".format(obj))
#        exit()
        return obj[0]
    
    def getFactibility(self, y):
        
        y = np.reshape(y, (1,self.PESO_ITEMS.shape[1]))
        npPesoItems = np.array(self.PESO_ITEMS)
#        print("y \n {} npPesoItems \n {}".format(y, npPesoItems))
        suma = np.sum(y * npPesoItems, axis=1)
#        print("suma items {}".format(suma[0]))
#        print("self.MAX_CAPACITY {}".format(self.MAX_CAPACITY))
#        print(y)
        for i in y[0]:
#            print(i)
            if i > 1 or i <0:
#                print("no permitido")
                return False
#        exit()
        if suma[0] > self.MAX_CAPACITY:
#            print("total items {} maxor a la capacidad {} ".format(suma[0],self.MAX_CAPACITY))
            return False
        if self.req is not None:
#            print("self.req \n{}".format(self.req))
#            print("y \n{}".format(y))
#            print("y * self.req \n{}".format(y * self.req))
            req = np.array(self.req)
            
            oblEcl = np.array_equal(req ,(y * req))
#            oblEcl = np.any(self.req == (y * self.req))
            if not oblEcl: 
#                print("y*req \n{}\n, req \n{}".format(y * req, req))
#                print("no estan todos los items requeridos")
                return False
        return True
    
            
    def getValidNeighborhood(self, currState, distance=1, dropout=0.0):
        print("buscando vecinos de {}".format(currState))
        ret = {}
        nDim = self._getDim()
#        nMovs = nDim*2
        movs = []
        for i in range(nDim):
            zeros = np.zeros((nDim),dtype=int)
#            print(zeros)
            zeros[i] = distance
            movs.append(zeros)
            movs.append(zeros*-1)
            
        print(movs)
        for mov in movs:
            
            print("currState {} mov {}".format(currState, mov))
            st = np.zeros((nDim),dtype=int)
            st = currState + (mov*distance)
#            for i in range(currState.shape[0]):
#                st[i] += mov[i] if 0< st[i] + mov[i] < 1 else currState[i]
            print(st)
            if(self.getFactibility(st)):
                t = tuple(st)
                ret[t] = mov
                print("agregado")
#        exit()
        
#        if len(ret) < 1: raise Exception("no se encontraron vecinos")
        
#        distance = self._getDim() if distance >= self._getDim() else distance
        
#        enc = self.encodeState(currState)
        
#        print("buscando vecinos de {}".format(enc))
#        random.seed(self.seed)
#        for pos in range(self._getDim()):
#            if random.random() < dropout: continue
#            st = currState
#            st = self.makeMove(st, pos, distance)
#            valid = self.getFactibility(st)
#            if valid:
#                t = tuple(st)
#                ret[t] = [pos, distance]
#            
##            for u in range(distance):
##                for direction in [-1, 1]:
##                    st = self.makeMove(st, pos, direction*(u+1))
#                    
##                    
##                    if valid:
###                        enc = self.encodeState(st)
###                        print("---{}\n".format(enc))
##                        t = tuple(st)
###                        print("---{}\n".format(t))
##                        ret[t] = [pos, u+1]
#                    
##        print("encontrados {}".format(len(ret)))
        return ret 
    
#    def getX(self):
        
    
    def getValidRandomState(self):
        valid = False
        iteracion = 0
        np.random.seed(self.seed)
        rndState = np.random.randint(2,size=self._getDim())
        
#        print("rndState {}".format(rndState))
        
        
        while not valid:
            #print("iteracion \n{}\n self.maxRSIter \n{}\n self._getDim() {}".format(iteracion,self.maxRSIter,self._getDim()))
            if iteracion >= self.maxRSIter or iteracion >= self._getDim():
                raise Exception(("no pude conseguir un estado valido al azar"))
            
            valid = self.getFactibility(rndState)
#            print("random state {} valid {}".format(rndState,valid))
#            print("fin")
#            exit()
            if valid: return rndState
            rndState = self.makeMove(rndState, iteracion, u=1)
            iteracion += 1
    
    def makeMove(self, state, pos, u=1):
        encState = self.encodeState(state)
        print("encState {}".format(encState))
        while pos >= encState.shape[0] - 1:
            pos -= (encState.shape[0]-1)
        print("moviendo pos {} de encState {} a pos {}".format(pos, encState, pos+1))    
        
        curr = encState[pos]
        encState[pos] = encState[pos+1]
        encState[pos+1] = curr
        print("termino movimiento: {}".format(encState))
#        exit()
        
        
        
#        encState = self.encodeState(state)
##        encState = encState.reshape((-1,1))
##        print("moviendo state {} en posicion {} por {} unidades".format(state, pos, u))
#        print("encState {}".format(encState))
#        print("moviendo pos {} de encState {} a pos {}".format(pos, encState, pos+1))    
#        multiplicador = 1
#        if u < 0:
#            multiplicador = -1
#            
#        
#        
#        posFinal = encState[pos]
#        for _ in range(u):
#            
#            posFinal += 1*multiplicador
#            
#            if posFinal > 1: 
#                posFinal = 0
#            elif posFinal < 1: 
#                posFinal = 1
##            print("pos final {}".format(posFinal))
#            
#            
#        
#        encState[pos] = posFinal
#        print("resultado {}".format(encState))
#        exit()
#        exit()
        return self.decodeSt(encState)
        
    def getDim(self):
        return [self._getDim()]
    def _getDim(self):
        if self.PESO_ITEMS is None:
            raise Exception("pesos items no cargados!")
        
        return self.PESO_ITEMS.shape[1]
    
    def encodeState(self, state):
        return state
    
    def decodeSt(self, enc):
        return enc
    
    def loadItemWeights(self, path):
        self.PESO_ITEMS = pd.read_csv(path, header=None)
        if(self.PESO_ITEMS.shape[0] != 1):
            raise Exception("la lista de items tiene mas de una dimension {}".format(self.PESO_ITEMS.shape))
            
    def loadRequired(self, path):
        self.req = pd.read_csv(path, header=None)
        if(self.req.shape[0] != 1 and self._getDim() != self.req.shape[0]):
            raise Exception("la lista de items requeridos ({}) no tiene el mismo tamaño que la lista de pesos. {}".format(self.req.ndim, self._getDim()))
            
    def setMaxCap(self, maxCap):
        self.MAX_CAPACITY = maxCap
        
    def getMaximize(self):
        return False
    
    
    
    
    
    
    
    
