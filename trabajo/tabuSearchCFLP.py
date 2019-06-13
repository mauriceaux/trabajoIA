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
from CFLPProblem import CFLPProblem
from KNAPSACKProblem import KNAPSACKProblem
from TabuSearch import TabuSearch

prob1 = CFLPProblem()
prob1.loadTransportCost("TC500.csv")
prob1.loadFacilityCost("FC500.csv")
prob1.loadDemand("dem500.csv")
prob1.loadCapacity("cap500.csv")
#prob1.loadTransportCost("TC.csv")
#prob1.loadFacilityCost("FC.csv")
#prob1.loadDemand("dem.csv")
#prob1.loadCapacity("cap.csv")

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("itemWeights.csv")
knapSack.loadRequired("required.csv")
knapSack.setMaxCap(70)


#algorithmT = TabuSearch(knapSack, maximize=False, numIter=100)
algorithmT = TabuSearch(prob1, maximize=False, numIter=100)
print("comienzo optimizacion")
algorithmT.optimize()
print("fin optimizacion")
totalCostT = algorithmT.getBestCost()
solutionT = algorithmT.bestState
execTimeT = algorithmT.execTime
iterationsT = algorithmT.iterations

print("fin de ejecución")
print("costo total cflp tabu: {}".format(totalCostT))
#print("costo total knapsack tabu: {}".format(totalCostT))



#import pandas as pd
#
#data = pd.read_csv("optimo.csv", header=None)
#data = np.array(data)
#factibility = prob1.getFactibility(data)
#print("optimo es factible? {}".format(factibility))
#costo = prob1.evalObj(data)
#print("costo optimo es: {}".format(costo))
#porcentajeT = (totalCostT* 100)/costo-100
#print("porcentaje diferencia tabu search {}%".format(porcentajeT))
#
print("tiempo de ejecucion {} micros".format(execTimeT))