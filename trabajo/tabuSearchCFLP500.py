#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 21:39:13 2019

@author: mauri
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:24:40 2019

@author: mauri
"""
import numpy as np
from modelos.CFLPProblem import CFLPProblem
from algoritmos.TabuSearch import TabuSearch

prob1 = CFLPProblem()
prob1.loadTransportCost("datos/cflp/TC500.csv")
prob1.loadFacilityCost("datos/cflp/FC500.csv")
prob1.loadDemand("datos/cflp/dem500.csv")
prob1.loadCapacity("datos/cflp/cap500.csv")
algorithmT = TabuSearch(prob1, maximize=False, numIter=100)
print("comienzo optimizacion")
algorithmT.optimize(winSize=0.05)
print("fin optimizacion")
totalCostT = algorithmT.getBestCost()
solutionT = algorithmT.bestState
execTimeT = algorithmT.execTime
iterationsT = algorithmT.iterations


print("fin de ejecución")
print("costo total cflp tabu: {}".format(totalCostT))
#
import pandas as pd
data = pd.read_csv("datos/cflp/optimo500c.csv", header=None)
data = np.array(data)

factibility = prob1.getFactibility(data)
print("optimo es factible? {}".format(factibility))

costo = prob1.evalObj(data)
print("costo optimo es: {}".format(costo))

porcentajeH = (totalCostT* 100)/costo-100
print("porcentaje diferencia tabu search {}%".format(porcentajeH))
print("tiempo de ejecucion {} micros".format(execTimeT))
prob1.grficarCostos()