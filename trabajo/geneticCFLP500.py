#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:58:29 2019

@author: mauri
"""

import numpy as np
from modelos.CFLPProblem import CFLPProblem
from algoritmos.Genetic import Genetic

prob1 = CFLPProblem()

prob1.loadTransportCost("datos/cflp/TC500.csv")
prob1.loadFacilityCost("datos/cflp/FC500.csv")
prob1.loadDemand("datos/cflp/dem500.csv")
prob1.loadCapacity("datos/cflp/cap500.csv")


genetic = Genetic(prob1, maximize=False, n=20)

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

data = pd.read_csv("datos/cflp/optimo500c.csv", header=None)
data = np.array(data)
#print(data)
#exit()
factibility = prob1.getFactibility(data)
print("optimo es factible? {}".format(factibility))
costo = prob1.evalObj(data)
print("costo optimo es: {}".format(costo))

porcentajeG = (totalCostG* 100)/costo-100
print("porcentaje diferencia genetic {}%".format(porcentajeG))

print("tiempo de ejecucion {} milis".format(execTimeG))