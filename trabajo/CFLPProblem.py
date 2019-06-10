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
    
    
    def evalObj(self, y):
        if self.TC is None:
            raise Exception("costos de transporte no cargados!")
        if self.FC is None:
            raise Exception("costos de instalacion no cargados!")
        transportCost = np.sum(y * np.array(self.TC))
#        print("y {}".format(y))
#        print("transportCost {}".format(y * np.array(self.TC)))
        x = self.getX(y)
        openingCost = np.sum(x*np.array(self.FC, dtype=float))
#        print("openingCost {}".format(x*np.array(self.FC)))
        obj = openingCost + transportCost
        if self.minObj is None or obj < self.minObj:
            self.minObj = obj
            self.minX = x
            self.minY = y
        return obj
        
    def getX(self, y):
        x = np.zeros((self.nFacilities))
        for i in range(self.ncli):
#            print("y[:,i] {}".format(y[:,i]))
            if np.count_nonzero(y[:,i]) > 0: x[i] = 1
        return x
        
    def getFactibility(self, y):
        if self.dem is None:
            raise Exception("demanda de clientes no cargada!")
        if self.ICap is None:
            raise Exception("capacidad de las facilities no cargada!")
#        CADA CLIENTE ASIGNADO  Y SOLO A UNA FACILITY 
        for i in range(self.ncli):
            totalAsignacionCliente = np.sum(y[i,:])
            if totalAsignacionCliente <= 0 or totalAsignacionCliente > 1: 
#                print("mas de un facilty asignado al cliente {}".format(i))                
                return False
            
#        CAPACIDAD NO SOBREPASADA
        totalDemanda = np.sum(np.array(self.dem))
        totalCapacidad = np.sum(np.array(self.getX(y)) * np.array(self.ICap))
        if totalDemanda > totalCapacidad: 
            return False
        return True
        
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
    
    def getValidRandomState(self):
        valid = False
        iteracion = 0
        np.random.seed(self.seed)
        encVec = np.random.randint(self.getDim()[0], size=self.getDim()[1])    
        while not valid:
            if iteracion >= self.maxRSIter or iteracion >= self.getDim()[0]:
                print("no pude conseguir un estado valido al azar")
                return
            rndState = self.decodeSt(encVec)
            valid = self.getFactibility(rndState)
            if valid: return rndState
            rndState = self.makeMove(rndState, iteracion)
            iteracion += 1
            
    def makeMove(self, state, pos, u=1):
        encState = self.encodeState(state)
#        print("encState {}".format(encState))
        while pos >= encState.shape[0] - 1:
            pos -= (encState.shape[0]-1)
#        print("moviendo pos {} de encState {} a pos {}".format(pos, encState, pos+1))    
        
        curr = encState[pos]
        encState[pos] = encState[pos+1]
        encState[pos+1] = curr
        
        
#        encState = self.encodeState(state)
#        print("encState {}".format(encState))
#        while pos >= encState.shape[0] - 1:
#            pos -= (encState.shape[0]-1)
#        print("moviendo pos {} de encState {} a pos {}".format(pos, encState, pos+1))    
#        
#        curr = encState[pos]
#        encState[pos] = encState[pos+1]
#        encState[pos+1] = curr
#        print("termino movimiento: {}".format(encState))
#        exit()
        
#        encState[pos] += u if 0 <= (encState[pos] + u) < self.getDim()[1] else 0
        return self.decodeSt(encState)
    
    def getDim(self):
        return [self.nFacilities, self.ncli]
        
    def encodeState(self, state):
#        state = np.array(state)
#        print(state.shape)
        res = np.zeros((state.shape[1]), dtype=int)
#        print("res {}".format(res.shape))
        for row in range(state.shape[1]):
#            print("row {}".format(row))
#            print("state {}".format(state))
#            print("state[row,:] {}".format(state[row,:]))
#            print("np.argmax(state[row,:] {}".format(np.argmax(state[row,:])))
#            exit()
            
            res[row] = np.argmax(state[row,:])
        return res
    
    def decodeSt(self, encVec):
        
#        dim = np.array([np.amax(encVec), encVec.shape[0]], dtype=int)
#        print(encVec)
        dim = self.getDim()
        decoded = np.zeros((dim[0], dim[1]))
#        print(decoded.shape)
        for row in range(encVec.shape[0]):
#            print("encVec {}".format(encVec))
#            print("row {} ,encVec[row] {}".format(row,encVec[row]))
#            print("row {}".format(row))
#            print("encVec {}".format(encVec))
#            print("encVec[row] {}".format(encVec[row]))
#            print("decoded {}".format(decoded))
            decoded[row,encVec[row]] = 1
        return decoded
        
    def nextState(self, state):
        vec = self.encodeState(state)
        nextVec = self.nextVector(vec)
        nextState = self.decodeSt(nextVec)
        return nextState
        
    def prevState(self, state):
        vec = self.encodeState(state)
        prevVec = self.prevVector(vec)
        prevState = self.decodeSt(prevVec)
        return prevState
            
    def nextVector(self, vec):
#        print("next vector: inicial {}".format(vec))
        dim = vec.shape[0]
        _max = self.getDim()[0] 
#        print("vec inicial {}".format(vec))
        for idx in range(dim):
            
            if (vec[idx]) < (_max-1):
                vec[idx] += 1
#                print("break")
                break
#            print("continuo en el ciclo")
            vec[idx] = 0
#        print("fin ciclo")
#        print("next vector: final {}".format(vec))
        return vec
    
    def prevVector(self, vec):
        dim = vec.shape[0]
        _max = self.getDim()[0]
        for idx in range(dim):
            if (vec[idx]) > 0:
                vec[idx] -= 1 
                break
            vec[idx] = _max -1
        return vec
        
    def getVector(self, currVec, pos, dist):
#        print("getVector \ncurrVec\n{} \npos\n{} \ndist\n{}".format(currVec, pos, dist))
        _max = self.getDim()[0]
        target = currVec
        while dist > 0:
#            print("target {}".format(target))
            dist -= 1
            if pos >= target.shape[0]:
                pos = 0
            currVal = target[pos]
            if currVal < (_max -1):
                target[pos] += 1
                continue
            target[pos] = 0
            pos += 1
            
#        print("target final {}\n max {}".format(target, _max))
#        exit()
        return target
        
    def getValidNeighborhood(self, currState, distance=1, dropout=0.0):
        ret = {}
        enc = self.encodeState(currState)
        distance = self.getDim()[0] if distance >= self.getDim()[0] else distance
#        print("buscando vecinos de {}".format(enc))
        random.seed(self.seed)
        for pos in range(self.getDim()[0]):
            
            
            if random.random() < dropout: continue
#            
            st = currState
            
            st = self.makeMove(st, pos, 1)
            valid = self.getFactibility(st)
            if valid:
                t = tuple(map(tuple, st))
                ret[t] = [pos, 1]
            
#            for u in range(distance):
#                
#                for direction in [-1, 1]:
#                    st = self.makeMove(st, pos, direction*u)
#                    valid = self.getFactibility(st)
#                    
#                    if valid:
##                        enc = self.encodeState(st)
##                        print("---{}\n".format(enc))
#                        t = tuple(map(tuple, st))
##                        print("---{}\n".format(t))
#                        ret[t] = [pos, u]
                    
#        print("encontrados {}".format(len(ret)))
        return ret
        
    def toBase(self, n):
        base = self.getDim()[1]
        string = self._toBase(n,base)
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

