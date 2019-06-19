#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 23:43:19 2019

@author: mauri
"""
import re
import numpy as np
file = open('optimo500bkp.csv')
lines = file.readlines()
newlines = None
buffer=[]
cont = 0
maxVal = len(lines)-100
for line in lines:
#for idx1 in range(maxVal):
#    if cont >= len(lines)-501: break
#    print("*{}*".format(line[0]))
    
    
#        cont = 0
#        newlines.append(buffer)
#        newlines = np.array(newlines)
#        newlines = newlines.reshape([500,7])
#        print(newlines)
#        exit()
#        
##        newlines += buffer
##        buffer = []
##    for idx1 in range(len(lines)):
#    lines[idx1] = re.sub(r'\s+', ',', lines[idx1])
#    lines[idx1] = re.sub(r'\n', '', lines[idx1])
#    lines[idx1] = re.sub(r' ', '', lines[idx1])
    line = re.sub(r'\s+', ',', line)
    line = re.sub(r'\n', '', line)
#    line = re.sub(r' ', '', line)
    splited = line.split(',')
#    print(splited)
#    if line[0] == '\n': continue
#    lines[idx1] = np.array(list(map(float,lines[idx1].split(',')[:-1])))
#    print("{} {}".format(cont,line.split(',')))
#    print(list(map(float,lines[idx1].split(',')[:-1])))
#    if cont > 3: exit()
#    print(splited)
    if len(splited) < 3: 
        
        continue
    if len(splited) >= 4: 
        
        line = list(map(float,splited[:-1]))
    else:
        line = list(map(float,splited))
#    if len(line) < 3: 
#        print(line)
#        continue
#    if len(newlines) <= 0:
#        newlines = line
#    print(line)
    buffer.append(line)
    if len(buffer) >= 500:
        traspuesta = np.array(buffer).T
#        print(traspuesta.shape)
        if newlines is None:
            newlines = traspuesta
#            continue
        else:
            newlines = np.array(newlines)
            newlines = np.vstack((newlines, traspuesta))
        print(newlines.shape)
        
#        newlines = np.array(newlines).reshape((-1))
#        print(np.array(newlines).shape)
#        exit()
        buffer = []
#    buffer.append(lines[idx1][:7])
#    buffer.append(np.array(lines[idx1]).split(',')))
    cont+=1

newlines = newlines.T
np.savetxt('optimo500c.csv', newlines, delimiter=',')
print(newlines.shape)
exit()
newlines = newlines.reshape([500,500])

#print(np.array(buffer).shape)
#exit()

#resto = []
#for line in lines:
#    
#    
#    
#    line = re.sub(r'\s+', ',', line)
#    line = re.sub(r'\n', '', line)
#    line = re.sub(r' ', '', line)
#      
#    
##    lines[idx1] = np.array(list(map(float,lines[idx1].split(',')[:-1])))
##    print("{} {}".format(cont,line.split(',')))
##    print(list(map(float,lines[idx1].split(',')[:-1])))
##    if cont > 3: exit()
#    line = line.split(',')
#    if line[0] == '': continue
#    if len(line) >= 7: continue
##    print("*{}*".format(line))
#    line = list(map(float,line[:-1]))
#    if line[0] == '\n': continue
#    resto.append(line)
#resto = np.array(resto)
#print(resto.shape)
#resto = resto.reshape((500,3))
#print(resto)
#exit()
#print(np.array(newlines))
#print(np.array(newlines).shape)