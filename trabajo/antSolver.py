# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:16:06 2019

@author: mauri
"""

from Ants import Ants
from KNAPSACKProblem import KNAPSACKProblem
from CFLPProblem import CFLPProblem

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("itemWeights.csv")
knapSack.loadRequired("required.csv")
knapSack.setMaxCap(70)

prob1 = CFLPProblem()
prob1.loadTransportCost("TC.csv")
prob1.loadFacilityCost("FC.csv")
prob1.loadDemand("dem.csv")
prob1.loadCapacity("cap.csv")


antColony = Ants(prob1)
antColony.optimize()