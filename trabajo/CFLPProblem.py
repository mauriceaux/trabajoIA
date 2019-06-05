#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:28:16 2019

@author: mauri
"""
import numpy as np
import pandas as pd

class CFLPProblem:

    def __init__(self, numCli, numFacilities):
        self.nFacilities = numFacilities
        self.ncli = numCli
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
        x = np.zeros((self.nFacilities))
        for i in range(self.ncli):
#            print("y[:,i] {}".format(y[:,i]))
            if np.count_nonzero(y[:,i]) > 0: x[i] = 1
        openingCost = np.sum(x*np.array(self.FC))
#        print("openingCost {}".format(x*np.array(self.FC)))
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
#        CADA CLIENTE ASIGNADO SOLO A UNA FACILITY
        for i in range(self.ncli):
            totalAsignacionCliente = np.sum(y[i,:])
            if totalAsignacionCliente > 1: 
                print("mas de un facilty asignado al cliente {}".format(i))                
                return False
            
#        DEMANDA NO SOBREPASADA
        for i in range(self.nFacilities):
            totalDemanda = np.sum(y[i]*np.array(self.dem))
            
#            print("total demanda {}".format(totalDemanda))
#            print("self.ICap {}".format(np.array(self.ICap.iloc[0])))
            if totalDemanda > np.array(self.ICap.iloc[0])[i]: 
                print("total demanda {} sobrepasa la capacidad {}".format(totalDemanda, self.ICap.iloc[i, 0]))                
                return False
        return True
        
    def loadDemand(self, path):
        self.dem = pd.read_csv(path, header=None)
        if self.dem.shape[1] != self.ncli:
            raise Exception("demanda no tiene el mismo numero de elementos que el numero de clientes. Num elementos leidos {}, num clientes {}".format(self.dem.shape[0], self.ncli))
              
    def loadCapacity(self, path):
        self.ICap = pd.read_csv(path, header=None)
        if self.ICap.shape[1] != self.nFacilities:
            raise Exception("capacidad no tiene el mismo numero de elementos que el numero de facilities. Num elementos leidos {}, num facilities {}".format(self.ICap.shape[0], self.nFacilities))
        
    def loadTransportCost(self, path):
        self.TC = pd.read_csv(path, header=None)        
        if self.TC.shape[0] != self.nFacilities and self.TC.shape[1] != self.ncli:
            raise Exception("costo de transporte no tiene el mismo numero de elementos que el numero de facilities x numero de clientes. Num elementos leidos [{}, {}], num facilities {} num clientes".format(self.TC.shape[0], self.TC.shape[1], self.nFacilities, self.ncli))
        
    def loadFacilityCost(self, path):
        self.FC = pd.read_csv(path, header=None)
        if self.FC.shape[1] != self.nFacilities:
            raise Exception("costo de instalacion no tiene el mismo numero de elementos que el numero de facilities. Num elementos leidos {}, num facilities {}".format(self.FC.shape[1], self.nFacilities))


prob = CFLPProblem(3,3)
prob.loadTransportCost("TC.csv")
prob.loadFacilityCost("FC.csv")
prob.loadDemand("dem.csv")
prob.loadCapacity("cap.csv")
solucionPosible = np.array([[1,0,0],[1,0,0],[0,1,0]])
print("evaluadando solucion: \n{}".format(solucionPosible))
if prob.getFactibility(solucionPosible):
    print ("Factible")
else:
    print ("no factible")
obj = prob.evalObj(solucionPosible)
print("objetivo {}".format(obj))
print("x \n{}".format(prob.minX))
print("y \n{}".format(prob.minY))