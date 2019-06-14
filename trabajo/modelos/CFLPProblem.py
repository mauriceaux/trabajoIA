#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:28:16 2019

@author: mauri
"""

import numpy as np
import pandas as pd
import random

class CFLPProblem:
    
    
    def __init__(self):
        
        self.maxRSIter = 500
        self.nFacilities = None
        self.ncli = None
        self.TC = None
        self.FC = None
        self.dem = None
        self.ICap = None
        self.minY = None
        self.minX = None
        self.minObj = None
        self.seed = 1
        np.random.seed(self.seed)
        self.subSampleSize = 0.1
        
    def getSubSampleLimits(self, num):
        if num > self.getSubSampleNumber():
            raise Exception("No existe esa sub muestra")
        limInf = round((self.ncli) * num * self.subSampleSize)
        limSup = round(((self.ncli) * (num + 1) * self.subSampleSize))
#        return self.toBase(limInf), self.toBase(limSup)
        return limInf, limSup
#        
    def getSubSampleNumber(self):
        return round(1/self.subSampleSize)
        
    
    
    def evalObj(self, y):
        if self.TC is None:
            raise Exception("costos de transporte no cargados!")
        if self.FC is None:
            raise Exception("costos de instalacion no cargados!")
        transportCost = np.sum(y * np.array(self.TC))
        x = self.getX(y)
        openingCost = np.sum(x*np.array(self.FC, dtype=float))
        obj = openingCost + transportCost
        if self.minObj is None or obj < self.minObj:
            self.minObj = obj
            self.minX = x
            self.minY = y
        return obj
    
    def getFactibility(self, y):
        if self.dem is None:
            raise Exception("demanda de clientes no cargada!")
        if self.ICap is None:
            raise Exception("capacidad de las facilities no cargada!")
#        CADA CLIENTE ASIGNADO  Y SOLO A UNA FACILITY 
        for i in range(self.ncli):
            totalAsignacionCliente = np.sum(y[i,:])
            if totalAsignacionCliente <= 0 or totalAsignacionCliente > 1:
                return False
                
#        CAPACIDAD NO SOBREPASADA
        totalDemanda = np.sum(np.array(self.dem))
        totalCapacidad = np.sum(np.array(self.getX(y)) * np.array(self.ICap))
        if totalDemanda > totalCapacidad: 
            return False
        return True
        
    def getX(self, y):
        x = np.zeros((self.nFacilities))
        for i in range(self.ncli):
            if np.count_nonzero(y[:,i]) > 0: x[i] = 1
        return x
        
    
        
   
    
    def getValidRandomState(self):
        valid = False
        iteracion = 0
        while not valid:
            if iteracion >= self.maxRSIter or iteracion >= self.getDim()[0]:
#                print("no pude conseguir un estado valido al azar")
                return
            encVec = np.random.randint(self.getDim()[0], size=self.getDim()[1])    
#            print("vector al azar {}".format(encVec))
            
            rndState = self.decodeSt(encVec)
            valid = self.getFactibility(rndState)
            if valid: 
#                print("eligiendo estado al azar {}".format(encVec))
                return rndState
#            rndState = self.makeMove(rndState, iteracion)
            iteracion += 1
            
    def getValidNeighborhood(self, currState, distance=1, dropout=0.0):
        ret = {}
#        random.seed(self.seed)
#        print(self.getDim()[1])
#        exit()
        for pos in range(self.getDim()[1]):
#            print(pos)
#            if random.random() < dropout: continue
#            st = currState
            for i in [-1,1]:
                st = self.makeMove(currState, pos, i*distance)
                valid = self.getFactibility(st)
                if valid:
#                    print(self.encodeState(st))
                    
                    t = tuple(map(tuple, st))
                    ret[t] = [pos, 1]
#            exit()
#        exit()
        return ret
            
    def makeMove(self, state, pos, u=1):
        encState = self.encodeState(state)
        
        resState = encState
        #NO SUPERA EL NUMERO DE FABRICAS
#        for _ in range(u):
        resState[pos] += u
        if resState[pos] >= self.getDim()[0]:
            resState[pos] = 0
        if resState[pos] < 0:
            resState[pos] = self.getDim()[0] -1
#        if 0 <= resState[pos] + u < self.getDim()[0]:
        
            
        return self.decodeSt(encState)
    
    def getDim(self):
        return [self.nFacilities, self.ncli]
        
    def encodeState(self, state):
        res = np.zeros((state.shape[1]), dtype=int)
        for row in range(state.shape[1]):
            res[row] = np.argmax(state[row,:])
        return res
    
    def decodeSt(self, encVec):
        
        dim = self.getDim()
        decoded = np.zeros((dim[0], dim[1]))
#        print(decoded.shape)
        for row in range(encVec.shape[0]):
            decoded[row,encVec[row]] = 1
        return decoded       

        
    
 
        
    def envVecToDec(self, enc):
        base = self.getDim()[1]
        total = 0
        cont = base-1
        for n in enc:
            total += n * (base**cont)
            cont -= 1
        return total
        
    def testEncoding(self):
        rndState = self.getValidRandomState()
        print("random state \n{}".format(rndState))
        enc = self.encodeState(rndState)
        print("encoded state \n{}".format(enc))
        
        dec = self.decodeSt(enc)
        print("decoded state \n{}".format(dec))
        if not np.array_equal(rndState, dec):
            raise Exception("Decodificación no funciona!")
        _enc = self.encodeState(dec)
        if not np.array_equal(_enc, enc):
            raise Exception("Codificación no funciona!")
    
    def loadDemand(self, path):
        self.dem = pd.read_csv(path, header=None)
        if not self.checkClientsNumber(self.dem.shape[1]):
            raise Exception("demanda no tiene el mismo numero de elementos que el numero de clientes. Num elementos leidos {}, num clientes {}".format(self.dem.shape[0], self.ncli))
              
    def loadCapacity(self, path):
        self.ICap = pd.read_csv(path, header=None)
        if not self.checkFacilitiesNumber(self.ICap.shape[1]):
            raise Exception("capacidad no tiene el mismo numero de elementos que el numero de facilities. Num elementos leidos {}, num facilities {}".format(self.ICap.shape[0], self.nFacilities))
        
    def loadTransportCost(self, path):
        
        self.TC = pd.read_csv(path, header=None)
        if not self.checkFacilitiesNumber(np.array(self.TC).shape[0]) or not self.checkClientsNumber(np.array(self.TC).shape[1]):
            raise Exception("costo de transporte no tiene el mismo numero de elementos que el numero de facilities x numero de clientes. Num elementos leidos [{}, {}], num facilities {} num clientes".format(self.TC.shape[0], self.TC.shape[1], self.nFacilities, self.ncli))
        
    def loadFacilityCost(self, path):
        self.FC = pd.read_csv(path, header=None)
        if not self.checkFacilitiesNumber(np.array(self.FC.shape[1])):
            raise Exception("costo de instalacion no tiene el mismo numero de elementos que el numero de facilities. Num elementos leidos {}, num facilities {}".format(self.FC.shape[1], self.nFacilities))
            
    def checkFacilitiesNumber(self, fc):
        self.nFacilities = fc if self.nFacilities is None else self.nFacilities
        return True if fc == self.nFacilities else False
    
    def checkClientsNumber(self, ncli):
        self.ncli = ncli if self.ncli is None else self.ncli
        return True if ncli == self.ncli else False
        
    def getMaximize(self):
        return False
    
    def getMaxValue(self):
        return self.nFacilities
    
    def getMinValue(self):
        return 1
            
    #    def nextVector(self, vec):
##        print("next vector: inicial {}".format(vec))
#        dim = vec.shape[0]
#        _max = self.getDim()[0] 
##        print("vec inicial {}".format(vec))
#        for idx in range(dim):
#            
#            if (vec[idx]) < (_max-1):
#                vec[idx] += 1
##                print("break")
#                break
##            print("continuo en el ciclo")
#            vec[idx] = 0
##        print("fin ciclo")
##        print("next vector: final {}".format(vec))
#        return vec
#    
#    def prevVector(self, vec):
#        dim = vec.shape[0]
#        _max = self.getDim()[0]
#        for idx in range(dim):
#            if (vec[idx]) > 0:
#                vec[idx] -= 1 
#                break
#            vec[idx] = _max -1
#        return vec

#        
    def toBase(self, n):
        base = self.getDim()[1]
        string = self._toBase(n,base)
#        print(string)
        arr = np.array(list(map(int, string.split(','))))
        return np.pad(arr, (base-arr.shape[0],0), 'constant')

    def _toBase(self, n,base):
        convertString = []
        for i in range(base+1):
            convertString.append(i)
        if n < base:
            return "{}".format(convertString[n])
        else:
            return "{},{}".format(self._toBase(n//base,base), convertString[n%base])       

#    def getVector(self, currVec, pos, dist):
##        print("getVector \ncurrVec\n{} \npos\n{} \ndist\n{}".format(currVec, pos, dist))
#        _max = self.getDim()[0]
#        target = currVec
#        while dist > 0:
##            print("target {}".format(target))
#            dist -= 1
#            if pos >= target.shape[0]:
#                pos = 0
#            currVal = target[pos]
#            if currVal < (_max -1):
#                target[pos] += 1
#                continue
#            target[pos] = 0
#            pos += 1
#            
##        print("target final {}\n max {}".format(target, _max))
##        exit()
#        return target

#    def nextState(self, state):
#        vec = self.encodeState(state)
#        nextVec = self.nextVector(vec)
#        nextState = self.decodeSt(nextVec)
#        return nextState
#        
#    def prevState(self, state):
#        vec = self.encodeState(state)
#        prevVec = self.prevVector(vec)
#        prevState = self.decodeSt(prevVec)
#        return prevState