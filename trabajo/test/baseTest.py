#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 20:54:29 2019

@author: mauri
"""
import numpy as np
from CFLPProblem import CFLPProblem

prob1 = CFLPProblem()
prob1.loadTransportCost("TC.csv")
prob1.loadFacilityCost("FC.csv")
prob1.loadDemand("dem.csv")
prob1.loadCapacity("cap.csv")



def toBase(n,base):
    string = _toBase(n,base)
    arr = np.array(list(map(int, string.split(','))))
    return np.pad(arr, (base-arr.shape[0],0), 'constant')

def _toBase(n,base):
    convertString = []
    for i in range(base+1):
        convertString.append(i)
    if n < base:
        return "{}".format(convertString[n])
    else:
        return "{},{}".format(_toBase(n//base,base), convertString[n%base])
  
array = toBase(50, 50)
for i in range(prob1.getSubSampleNumber()):
    limInf, limSup = prob1.getSubSampleLimits(i)
#    print(prob1.getSubSampleNumber())
    print("limite inferior {}\nlimite superior {}".format(limInf, limSup))