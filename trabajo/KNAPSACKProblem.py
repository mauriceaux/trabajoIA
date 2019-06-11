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
        self.seed = 1
        self.PESO_ITEMS = None
        self.MAX_CAPACITY = None
        self.req = None
    
    
    def evalObj(self, y):
        if self.PESO_ITEMS is None:
            raise Exception("pesos items no cargados!")
        if self.MAX_CAPACITY is None:
            raise Exception("no se definió el tamaño de la mochila!")
            
        pesoItems = np.array(self.PESO_ITEMS)
        pesoItems = y * pesoItems
        
        capUsed = self.MAX_CAPACITY - np.sum(pesoItems, axis=1)
        itmExcl = self.PESO_ITEMS.shape[0] - np.sum(y)
        obj = capUsed 
        return obj[0]
    
    def getFactibility(self, y):
        
        y = np.reshape(y, (1,self.PESO_ITEMS.shape[1]))
        npPesoItems = np.array(self.PESO_ITEMS)
        suma = np.sum(y * npPesoItems, axis=1)
        for i in y[0]:
            if i > 1 or i <0:
                return False
        if suma[0] > self.MAX_CAPACITY:
            return False
        if self.req is not None:
            req = np.array(self.req)
            
            oblEcl = np.array_equal(req ,(y * req))
            if not oblEcl: 
                return False
        return True
        
    
    def getValidRandomState(self):
        valid = False
        iteracion = 0
        np.random.seed(self.seed)
        
        rndState = np.random.randint(self.getMaxValue(),size=self._getDim())
        
        while not valid:
            if iteracion >= self._getDim():
                raise Exception(("no pude conseguir un estado valido al azar"))
            valid = self.getFactibility(rndState)
            if valid: 
                return rndState
            rndState = self.makeMove(rndState, iteracion, u=1)
            iteracion += 1
    
    def makeMove(self, state, pos, u=1):
        encState = self.encodeState(state)
        encState[pos] += u
        if encState[pos] >= self.getMaxValue():
            encState[pos] = self.getMinValue()
        if encState[pos] < self.getMinValue():
            encState[pos] = self.getMaxValue() -1        
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
    
    def getMaxValue(self):
        return 2
    
    def getMinValue(self):
        return 0
    
    
    
    
    
    
    
    
