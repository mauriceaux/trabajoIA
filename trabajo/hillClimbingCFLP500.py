#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:49:30 2019

@author: mauri
"""

from modelos.CFLPProblem import CFLPProblem
from algoritmos.HillClimbing import HillClimbing
import numpy as np

cflp = CFLPProblem()
cflp.loadTransportCost("datos/cflp/TC500.csv")
cflp.loadFacilityCost("datos/cflp/FC500.csv")
cflp.loadDemand("datos/cflp/dem500.csv")
cflp.loadCapacity("datos/cflp/cap500.csv")

algorithmH = HillClimbing(cflp, maximize=False, numIter=50)
print("comienzo optimizacion")
algorithmH.optimize(winSize=0.05)
print("fin optimizacion")

totalCost = algorithmH.getBestCost()
solution = algorithmH.bestState
#print(knapSack.getFactibility(solution))
execTime = algorithmH.execTime
iterations = algorithmH.iterations

#print("costo total knpsack hill climbing: {}".format(totalCost))

print("costo total cflp hill climbing: {}".format(totalCost))
#
import pandas as pd
data = pd.read_csv("datos/cflp/optimo500c.csv", header=None)
data = np.array(data)

factibility = cflp.getFactibility(data)
print("optimo es factible? {}".format(factibility))

costo = cflp.evalObj(data)
print("costo optimo es: {}".format(costo))

porcentajeH = (totalCost* 100)/costo-100
print("porcentaje diferencia hill climbing {}%".format(porcentajeH))
#
print("tiempo de ejecucion {} micros".format(execTime))
cflp.grficarCostos()