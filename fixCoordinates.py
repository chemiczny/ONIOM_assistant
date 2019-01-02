#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 22:04:05 2018

@author: michal
"""
from readingUtilities import isBlankLine, floatInList
import numpy as np
def writeNewInput ( oldInput, newCoords, newInputName ):
    oldFile = open(oldInput, 'r')
    beginning = ""
    line = oldFile.readline()
    destiny = open(newInputName, 'w')
    
    #route section
    while not isBlankLine(line):
        beginning += line
        line = oldFile.readline()
        
    beginning += line
    line = oldFile.readline()
    #comment
    while not isBlankLine(line):
        beginning += line
        line = oldFile.readline()
        
    beginning += line
    line = oldFile.readline()
    
    beginning += line
    destiny.write(beginning)
    for coord in newCoords:
        line = oldFile.readline()
        lineSpl = line.split()
        coordInd = floatInList(lineSpl)[-3:]
        for ci, crd in zip(coordInd, coord):
            lineSpl[ci] = str(crd)
        destiny.write("\t".join(lineSpl)+"\n")
        
    line = oldFile.readline()
    while line:
        destiny.write(line)
        line = oldFile.readline()
    
    destiny.close()
    oldFile.close()

def getFrozenIndexes( oldInput ):
    oldFile = open(oldInput, 'r')
    line = oldFile.readline()
    
    #route section
    while not isBlankLine(line):
        line = oldFile.readline()
        
    line = oldFile.readline()
    #comment
    while not isBlankLine(line):
        line = oldFile.readline()
        
    line = oldFile.readline() #charges and multiplicity
    line = oldFile.readline()
    
    indexes = []
    ind = 0
    coords = []
    while not isBlankLine(line):
        
        lineSpl = line.split()
        if lineSpl[1] == "-1":
            indexes.append(ind)
            
        coordInd = floatInList(lineSpl)[-3:]
        newCoords = [ float(lineSpl[c]) for c in coordInd]
        coords.append(newCoords)
        line = oldFile.readline()
        ind += 1
    
    oldFile.close()
    
    return indexes, coords

indexes, coords = getFrozenIndexes("/home/michal/KSTD/qmmm/newGeom/cluster/pm7/irevLastFrame.inp")
indexes2, coords2 = getFrozenIndexes("/home/michal/KSTD/qmmm/newGeom/cluster/pm7/s1LastFrame.inp")

coordMat1 = []
for c in coords:
    coordMat1.append( c + [1] )
coordMat1 = np.array(coordMat1)

coordMat2 = []
for c in coords2:
    coordMat2.append( c + [1] )
coordMat2 = np.array(coordMat2)

frozen1Mat = []
for i in indexes:
    frozen1Mat.append(coords[i]+[1])
    
frozen1Mat = np.transpose(np.array(frozen1Mat[:4]))

frozen2Mat = []
for i in indexes2:
    frozen2Mat.append(coords2[i]+[1])
    
frozen2Mat = np.transpose(np.array(frozen2Mat[:4]))

T = np.matmul(  frozen2Mat, np.linalg.inv(frozen1Mat))
newCoords1Temp = np.matrix.transpose(np.matmul(T, np.matrix.transpose(coordMat1)))
newCoords1 = []
for row in newCoords1Temp:
    newCoords1.append( [row[0], row[1], row[2]] )


writeNewInput ( "/home/michal/KSTD/qmmm/newGeom/cluster/pm7/irevLastFrame.inp", newCoords1 ,  "/home/michal/KSTD/qmmm/newGeom/cluster/pm7/irevLastFrameFixed.inp" )

