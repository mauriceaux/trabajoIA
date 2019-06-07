#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:28:16 2019

@author: mauri
"""

import numpy as np
import pandas as pd

class CFLPProblem:
    
    
    def __init__(self):
        
        self.nFacilities = None
        self.ncli = None
        self.TC = None
        self.FC = None
        self.dem = None
        self.ICap = None
        self.minY = None
        self.minX = None
        self.minObj = None
    
    
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
        print("obteniendo state al azar")
        
        valid = False
        iteracion = 0
        encVec = np.random.randint(2, size=self.getDim()[1])    
#        print(self.getDim())
        while not valid:
            iteracion += 1
#            print("iteracion: {}".format(iteracion), end='\r')
            
            rndState = self.decodeSt(encVec)
            valid = self.getFactibility(rndState)
            encVec = self.nextVector(encVec)
#            print("rndState {} \nvalido {}".format(rndState, valid))
        print("fin obteniendo state al azar")
        return rndState
    
    def getDim(self):
        return [self.nFacilities, self.ncli]
        
    def encodeState(self, state):
#        state = np.array(state)
#        print(state.shape)
        res = np.zeros((state.shape[1]), dtype=int)
#        print(res)
        for row in range(state.shape[1]):
#            print("row {}".format(row))
#            print("state {}".format(state))
#            print("state[row,:] {}".format(state[row,:]))
#            print("np.argmax(state[row,:] {}".format(np.argmax(state[row,:])))
#            exit()
            res[np.argmax(state[row,:])] = 1
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
            
    def nextVector(self, vec):
#        print("next vector ini {}".format(vec))
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
#        print("vec final {}".format(vec))
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
