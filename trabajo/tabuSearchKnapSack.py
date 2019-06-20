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
from modelos.KNAPSACKProblem import KNAPSACKProblem
from algoritmos.TabuSearch import TabuSearch

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("datos/knapsack/itemWeights.csv")
knapSack.loadRequired("datos/knapsack/required.csv")
knapSack.setMaxCap(70)


algorithmT = TabuSearch(knapSack, maximize=False, numIter=100)
print("comienzo optimizacion")
algorithmT.optimize()
print("fin optimizacion")
totalCostT = algorithmT.getBestCost()
solutionT = algorithmT.bestState
execTimeT = algorithmT.execTime
iterationsT = algorithmT.iterations

print("fin de ejecución")
print("costo total knapsack tabu: {}".format(totalCostT))
print("tiempo de ejecucion {} micros".format(execTimeT))
knapSack.grficarCostos()