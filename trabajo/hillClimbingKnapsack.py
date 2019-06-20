#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:49:30 2019

@author: mauri
"""

from modelos.KNAPSACKProblem import KNAPSACKProblem
from algoritmos.HillClimbing import HillClimbing

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("datos/knapsack/itemWeights.csv")
knapSack.loadRequired("datos/knapsack/required.csv")
knapSack.setMaxCap(70)

algorithmH = HillClimbing(knapSack, maximize=False, numIter=50)
print("comienzo optimizacion")
algorithmH.optimize()
print("fin optimizacion")

totalCost = algorithmH.getBestCost()
solution = algorithmH.bestState
#print(knapSack.getFactibility(solution))
execTime = algorithmH.execTime
iterations = algorithmH.iterations

print("costo total knpsack: {}".format(totalCost))


print("tiempo de ejecucion {} micros".format(execTime))
knapSack.grficarCostos()