#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:58:29 2019

@author: mauri
"""

import numpy as np
from modelos.KNAPSACKProblem import KNAPSACKProblem
from algoritmos.Genetic import Genetic



knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("datos/knapsack/itemWeights.csv")
knapSack.loadRequired("datos/knapsack/required.csv")
knapSack.setMaxCap(70)

genetic = Genetic(knapSack, maximize=False, n=20)

print("comienzo optimizacion")
genetic.optimize()
print("fin optimizacion")

totalCostG = genetic.getBestCost()
solutionG = genetic.bestState
execTimeG = genetic.execTime
iterationsG = genetic.iterations

print("costo total knpsack genetic: {}".format(totalCostG))
