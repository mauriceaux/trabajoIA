# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:24:40 2019

@author: mauri
"""
import numpy as np
from CFLPProblem import CFLPProblem
from HillClimbing import HillClimbing

prob = CFLPProblem(3,3)
prob.loadTransportCost("TC.csv")
prob.loadFacilityCost("FC.csv")
prob.loadDemand("dem.csv")
prob.loadCapacity("cap.csv")

algorithm = HillClimbing(prob, maximize=False)

algorithm.optimize()
totalCost = algorithm.bestCost
solution = algorithm.bestState
execTime = algorithm.execTime
iterations = algorithm.iterations
print("fin de ejecución")
print("solución encontrada: {}".format(solution))
print("costo total: {}".format(totalCost))
print("tiempo de ejecucion {}".format(execTime))
print("numero de iteraciones {}".format(iterations))



#solucionPosible = np.array([[1,0,0],[1,0,0],[0,1,0]])
#print("evaluadando solucion: \n{}".format(solucionPosible))
#if prob.getFactibility(solucionPosible):
#    print ("Factible")
#else:
#    print ("no factible")
#obj = prob.evalObj(solucionPosible)
#print("objetivo {}".format(obj))
#print("x \n{}".format(prob.minX))
#print("y \n{}".format(prob.minY))