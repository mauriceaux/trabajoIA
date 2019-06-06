# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:24:40 2019

@author: mauri
"""
import numpy as np
from CFLPProblem import CFLPProblem
from HillClimbing import HillClimbing

prob = CFLPProblem()
prob.loadTransportCost("TC.csv")
prob.loadFacilityCost("FC.csv")
prob.loadDemand("dem.csv")
prob.loadCapacity("cap.csv")

algorithm = HillClimbing(prob, maximize=False, numN = 10)
print("comienzo optimizacion")
algorithm.optimize()
print("fin optimizacion")
totalCost = algorithm.getBestCost()
solution = algorithm.bestState
execTime = algorithm.execTime
iterations = algorithm.iterations
print("fin de ejecución")
print("solución encontrada: \n{}".format(solution))
print("facilities asignadas \n{}".format(algorithm.x))
print("costo total: {}".format(totalCost))
print("costo historico: {}".format(algorithm.costHistory))
print("tiempo de ejecucion {}".format(execTime))
print("numero de iteraciones {}".format(iterations))

print("costo total de instalación {}".format(np.sum(np.array(algorithm.x) * np.array(prob.FC))))
print("capacidad total {}".format(np.sum(np.array(algorithm.x) * np.array(prob.ICap))))
print("demanda total {}".format(np.sum(np.array(prob.dem))))