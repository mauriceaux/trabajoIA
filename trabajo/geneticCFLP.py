#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:58:29 2019

@author: mauri
"""

import numpy as np
from CFLPProblem import CFLPProblem
from KNAPSACKProblem import KNAPSACKProblem
from Genetic import Genetic

prob1 = CFLPProblem()
prob1.loadTransportCost("TC.csv")
prob1.loadFacilityCost("FC.csv")
prob1.loadDemand("dem.csv")
prob1.loadCapacity("cap.csv")

knapSack = KNAPSACKProblem()
knapSack.loadItemWeights("itemWeights.csv")
knapSack.loadRequired("required.csv")
knapSack.setMaxCap(70)

genetic = Genetic(prob1, maximize=False, n=20)
#genetic = Genetic(knapSack, maximize=False, n=20)

print("comienzo optimizacion")
genetic.optimize()
print("fin optimizacion")

totalCostG = genetic.getBestCost()
solutionG = genetic.bestState
execTimeG = genetic.execTime
iterationsG = genetic.iterations

#print("costo total knpsack genetic: {}".format(totalCostG))

print("costo total cflp genetic: {}".format(totalCostG))
#
import pandas as pd

data = pd.read_csv("optimo.csv", header=None)
data = np.array(data)
factibility = prob1.getFactibility(data)
print("optimo es factible? {}".format(factibility))
costo = prob1.evalObj(data)
print("costo optimo es: {}".format(costo))

porcentajeG = (totalCostG* 100)/costo-100
print("porcentaje diferencia genetic {}%".format(porcentajeG))
#
print("tiempo de ejecucion {} milis".format(execTimeG))