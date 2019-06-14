# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:16:06 2019

@author: mauri
"""

from algoritmos.Ants import Ants
from modelos.KNAPSACKProblem import KNAPSACKProblem
from modelos.CFLPProblem import CFLPProblem

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("datos/knapsack/itemWeights.csv")
knapSack.loadRequired("datos/knapsack/required.csv")
knapSack.setMaxCap(70)

prob1 = CFLPProblem()
prob1.loadTransportCost("datos/cflp/TC.csv")
prob1.loadFacilityCost("datos/cflp/FC.csv")
prob1.loadDemand("datos/cflp/dem.csv")
prob1.loadCapacity("datos/cflp/cap.csv")


antColony = Ants(prob1)
#antColony = Ants(knapSack)

antColony.optimize()