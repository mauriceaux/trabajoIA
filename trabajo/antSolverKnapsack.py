# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:16:06 2019

@author: mauri
"""

from algoritmos.Ants import Ants
from modelos.KNAPSACKProblem import KNAPSACKProblem
import numpy as np

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("datos/knapsack/itemWeights.csv")
knapSack.loadRequired("datos/knapsack/required.csv")
knapSack.setMaxCap(70)


antColony = Ants(knapSack)

antColony.optimize()

totalCost = antColony.getBestCost()
solution = antColony.bestState
execTime = antColony.execTime
iterations = antColony.iterations

print("costo total knpsack hormigas: {}".format(totalCost))
print("tiempo de ejecucion {} micros".format(execTime))
knapSack.grficarCostos()