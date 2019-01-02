#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:41:20 2018

@author: michal
"""
from math import sqrt
from copy import copy
import sys

def readAllXyz( xyz ):
 
    xyzF = open(xyz, 'r')
    
    line = xyzF.readline()
    atomsNo = int(line)

    line = xyzF.readline()
    allCoords = []
    allElements = []
    while line:
        elements = []
        coords = []
        for i in range(atomsNo):
            line = xyzF.readline()
            line = line.split()
            elements.append(  line[0])
            coords.append( [ float(c) for c in line[-3:] ]  )
            
        line = xyzF.readline()
        line = xyzF.readline()
        allElements.append(elements)
        allCoords.append(coords)
 
    xyzF.close()
    return allElements, allCoords

def dist(coord1, coord2):
    dist = 0
    for c1, c2 in zip(coord1, coord2):
        dist += (c1 - c2)*(c1-c2)
        
    return sqrt(dist)

def readIndexes( indexFile):
    indF = open(indexFile, 'r')
    line = indF.readline()
    indexes = []
    while line:
        newIndexes = [ int(el) for el in line.split() ]
        indexes += newIndexes
        line = indF.readline()
    
    indF.close()
    
    return indexes

def fixXyz( elements, coords, crds2omit):
    crd1 = coords[0][crds2omit:]
    el1 = elements[0][crds2omit:]
    
    crd2 = coords[1][crds2omit:]
    el2 = elements[1][crds2omit:]
    
    mapping = {}
    
    ind1 = 0
    for c1, e1 in zip(crd1, el1):
        mapping[ind1] = None
        
        ind2 = 0
        minDist = 666
        for c2, e2 in zip(crd2, el2):
            if e1 != e2:
                ind2+=1
                continue
            
            if ind2 in mapping.values():
                ind2 += 1
                continue
            
            if dist(c1, c2) < minDist:
                minDist =dist(c1, c2)
                mapping[ind1] = ind2
            
            ind2 += 1
            
        ind1 += 1
        
    crd2Fixed = copy(crd2)
    el2Fixed = copy(el2)
    
    for i in mapping:
        crd2Fixed[i] = crd2[mapping[i]]
        el2Fixed[i] = el2[mapping[i]]
        
    fixedCoords = [  coords[0] , coords[1][:crds2omit] + crd2Fixed ]
    fixedElements = [ elements[0], elements[1][:crds2omit] + el2Fixed]
    
    return fixedElements, fixedCoords

def writeXyz( elements1, elements2, coords1, coords2, destiny ):
    dest = open(destiny, "w")
    dest.close()
    
    dest = open(destiny, 'a+')
    dest.write( str( len(elements1) ) + "\n\n" )
    
    for el, cor in zip(elements1, coords1):
        dest.write(el+" "+str(cor[0])+" "+str(cor[1])+" "+str(cor[2])+"\n")
        
    dest.write( str( len(elements2) ) + "\n\n" )
    for el, cor in zip(elements2, coords2):
        dest.write(el+" "+str(cor[0])+" "+str(cor[1])+" "+str(cor[2])+"\n")
        
    dest.close()

if len(sys.argv) != 3:
    print("Potrzebuje: xyz, indexFile")
else:
    
    xyz = sys.argv[1]
    indexFile = sys.argv[2]
    
    el, crds = readAllXyz(xyz)
    crds2omit = len(readIndexes(indexFile))
    el, crds = fixXyz(el, crds, crds2omit)
    writeXyz(el[0], el[1], crds[0], crds[1], xyz)