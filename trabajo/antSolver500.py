# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:16:06 2019

@author: mauri
"""

from algoritmos.Ants import Ants
from modelos.KNAPSACKProblem import KNAPSACKProblem
from modelos.CFLPProblem import CFLPProblem
import numpy as np

prob1 = CFLPProblem()

prob1.loadTransportCost("datos/cflp/TC500bkp.csv")
prob1.loadFacilityCost("datos/cflp/FC500.csv")
prob1.loadDemand("datos/cflp/dem500.csv")
prob1.loadCapacity("datos/cflp/cap500.csv")


antColony = Ants(prob1)

antColony.optimize(winSize=0.3)

totalCost = antColony.getBestCost()
solution = antColony.bestState
execTime = antColony.execTime
iterations = antColony.iterations

import pandas as pd
data = pd.read_csv("datos/cflp/optimo500c.csv", header=None)
data = np.array(data)

factibility = prob1.getFactibility(data)
print("optimo es factible? {}".format(factibility))

costo = prob1.evalObj(data)
print("costo optimo es: {}".format(costo))

porcentajeH = (totalCost* 100)/costo-100
print("porcentaje diferencia hormigas {}%".format(porcentajeH))
#
print("tiempo de ejecucion {} micros".format(execTime))
prob1.grficarCostos()