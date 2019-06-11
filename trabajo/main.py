# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:24:40 2019

@author: mauri
"""
import numpy as np
from CFLPProblem import CFLPProblem
from HillClimbing import HillClimbing
#from KNAPSACKProblem import KNAPSACKProblem
from TabuSearch import TabuSearch
from Genetic import Genetic

prob1 = CFLPProblem()
prob1.loadTransportCost("TC.csv")
prob1.loadFacilityCost("FC.csv")
prob1.loadDemand("dem.csv")
prob1.loadCapacity("cap.csv")
#
#prob2 = CFLPProblem()
#prob2.loadTransportCost("TC.csv")
#prob2.loadFacilityCost("FC.csv")
#prob2.loadDemand("dem.csv")
#prob2.loadCapacity("cap.csv")

#knapSack = KNAPSACKProblem()
#knapSack.loadItemWeights("itemWeights.csv")
#knapSack.loadRequired("required.csv")
#knapSack.setMaxCap(70)



#algorithmH = HillClimbing(prob1, maximize=False, numIter=50)
#algorithmHKP = HillClimbing(knapSack, maximize=knapSack.getMaximize(), numIter=50)
#algorithmT = TabuSearch(prob2, maximize=False, numIter=100)
#algorithmT = TabuSearch(knapSack, maximize=False, numIter=100)
genetic = Genetic(prob1, maximize=False, n=10)


#exit()



#100 pruebas de codificacion
#for _ in range(100):
#    prob.testEncoding()
print("comienzo optimizacion")
#algorithmH.optimize()
#algorithmHKP.optimize()
#algorithmT.optimize()
genetic.optimize()
print("fin optimizacion")
#totalCostT = algorithmT.getBestCost()
#solutionT = algorithmT.bestState
#execTimeT = algorithmT.execTime
#iterationsT = algorithmT.iterations
#
#totalCostH = algorithmH.getBestCost()
#solutionH = algorithmH.bestState
#execTimeH = algorithmH.execTime
#iterationsH = algorithmH.iterations

totalCostG = genetic.getBestCost()
solutionG = genetic.bestState
execTimeG = genetic.execTime
iterationsG = genetic.iterations
#
#totalCostKP = algorithmHKP.getBestCost()
#solutionKP = algorithmHKP.bestState
#execTimeKP = algorithmHKP.execTime
#iterationsKP = algorithmHKP.iterations
print("fin de ejecución")
#print("solución encontrada: \n{}".format(solutionT))
#print("costo total cflp tabu: {}".format(totalCostT))
#print("solución encontrada: \n{}".format(solutionH))
#print("costo total cflp hill climbing: {}".format(totalCostH))
print("costo total cflp genetic: {}".format(totalCostG))
#print("solución encontrada: \n{}".format(solutionKP))
#print("espacio disponible knacksack: {}".format(totalCostKP))
#print("solución encontrada: \n{}".format(solution))
#print("facilities asignadas \n{}".format(algorithmT.x))
#print("costo total: {}".format(totalCostT))
#print("costo historico: {}".format(algorithmT.costHistory))
#print("tiempo de ejecucion {}".format(execTime))
#print("numero de iteraciones {}".format(iterations))
#
#print("costo total de instalación {}".format(np.sum(np.array(algorithmT.x) * np.array(prob.FC))))
#print("capacidad total {}".format(np.sum(np.array(algorithmT.x) * np.array(prob.ICap))))
#print("demanda total {}".format(np.sum(np.array(prob.dem))))

import pandas as pd

data = pd.read_csv("optimo.csv", header=None)
data = np.array(data)
#print(data.shape)
#factibility = prob2.getFactibility(data)
factibility = prob1.getFactibility(data)
print("optimo es factible? {}".format(factibility))
#costo = prob2.evalObj(data)
costo = prob1.evalObj(data)
print("costo optimo es: {}".format(costo))

#porcentajeH = (totalCostH* 100)/costo-100
#porcentajeT = (totalCostT* 100)/costo-100
porcentajeG = (totalCostG* 100)/costo-100
#
#print("diferencia con Hill Climbing {}".format(totalCostH - costo))
#print("diferencia con tabu search {}".format(totalCostT - costo))

#print("porcentaje diferencia hill climbing {}%".format(porcentajeH))
#print("porcentaje diferencia tabu search {}%".format(porcentajeT))
print("porcentaje diferencia genetic {}%".format(porcentajeG))