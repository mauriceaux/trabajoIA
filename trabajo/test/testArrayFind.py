# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 17:09:14 2019

@author: mauri
"""

import numpy as np
lista = []
unos = np.ones((3,3), dtype=int)
lista.append(unos)
arr = np.ones((3,3), dtype=int)*2
lista.append(arr)
arr = np.ones((3,3), dtype=int)*3
lista.append(arr)
arr = np.ones((3,3), dtype=int)*4
lista.append(arr)

print("lista {}".format(lista))
print("lista contiene una matriz de puros unos?")

resultado = np.any(lista == (np.ones((3,3), dtype=int))*4)
print(resultado)