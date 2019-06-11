#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:49:30 2019

@author: mauri
"""

from CFLPProblem import CFLPProblem
from KNAPSACKProblem import KNAPSACKProblem
from HillClimbing import HillClimbing
import numpy as np

cflp = CFLPProblem()
cflp.loadTransportCost("TC.csv")
cflp.loadFacilityCost("FC.csv")
cflp.loadDemand("dem.csv")
cflp.loadCapacity("cap.csv")

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("itemWeights.csv")
knapSack.loadRequired("required.csv")
knapSack.setMaxCap(70)

algorithmH = HillClimbing(cflp, maximize=False, numIter=50)
#algorithmH = HillClimbing(knapSack, maximize=False, numIter=50)
print("comienzo optimizacion")
algorithmH.optimize()
print("fin optimizacion")

totalCost = algorithmH.getBestCost()
solution = algorithmH.bestState
#print(knapSack.getFactibility(solution))
execTime = algorithmH.execTime
iterations = algorithmH.iterations

print("costo total knpsack hill climbing: {}".format(totalCost))

#print("costo total cflp hill climbing: {}".format(totalCost))
#
#import pandas as pd
#data = pd.read_csv("optimo.csv", header=None)
#data = np.array(data)
#
#factibility = cflp.getFactibility(data)
#print("optimo es factible? {}".format(factibility))
#
#costo = cflp.evalObj(data)
#print("costo optimo es: {}".format(costo))
#
#porcentajeH = (totalCost* 100)/costo-100
#print("porcentaje diferencia hill climbing {}%".format(porcentajeH))
#
print("tiempo de ejecucion {} micros".format(execTime))