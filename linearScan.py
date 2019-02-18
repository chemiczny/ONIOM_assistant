#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 13:38:30 2019

@author: michal
"""
import sys
from readingUtilities import isBlankLine, floatInList
import numpy as np
from os import mkdir
from slurm import writeSlurmScript
from os.path import join, basename

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
    elements = []
    while not isBlankLine(line):
        
        lineSpl = line.split()
        if lineSpl[1] == "-1":
            indexes.append(ind)
            
        coordInd = floatInList(lineSpl)[-3:]
        newCoords = [ float(lineSpl[c]) for c in coordInd]
        coords.append(newCoords)
        elements.append(lineSpl[0])
        
        line = oldFile.readline()
        ind += 1
    
    oldFile.close()
    
    return indexes, coords, elements

def fixCoordinates(frozenIndexes, templateCoords, coords2fix):
    coordMat1 = []
    for c in coords2fix:
        coordMat1.append( c + [1] )
    coordMat1 = np.array(coordMat1)
    
    coordMat2 = []
    for c in templateCoords:
        coordMat2.append( c + [1] )
    coordMat2 = np.array(coordMat2)
    
    frozen1Mat = []
    for i in frozenIndexes:
        frozen1Mat.append(coords2fix[i]+[1])
        
    frozen1Mat = np.transpose(np.array(frozen1Mat[:4]))
    
    frozen2Mat = []
    for i in frozenIndexes:
        frozen2Mat.append(templateCoords[i]+[1])
        
    frozen2Mat = np.transpose(np.array(frozen2Mat[:4]))
    
    T = np.matmul(  frozen2Mat, np.linalg.inv(frozen1Mat))
    newCoords1Temp = np.matrix.transpose(np.matmul(T, np.matrix.transpose(coordMat1)))
    newCoords1 = []
    for row in newCoords1Temp:
        newCoords1.append( [row[0], row[1], row[2]] )
        
    return newCoords1

def appendCoords2File( elements, coords, file2append ):
    xyz = open(file2append, 'a')
    xyz.write(str(len(elements))+"\n\n")
    
    for el, c in zip(elements, coords):
        xyz.write(el+"\t" + str(c[0])+"\t"+str(c[1])+"\t"+str(c[2])+"\n")
        
    
    xyz.close()
    
def generateFrames(coordsStart, coordsStop, frameNo):
    frames = []
    
    for i in range(1, frameNo):
        newFrame = []
        for rowStart, rowStop in zip(coordsStart, coordsStop):
            newRow = []
            for coordStart, coordStop in zip(rowStart, rowStop):
                newCoord = float(i)/frameNo*coordStop + float(frameNo-i)/frameNo*coordStart
                newRow.append(newCoord)
            newFrame.append(newRow)
        frames.append(newFrame)
    
    return frames

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

if len(sys.argv) < 3:
    print("Potrzebuje: input start, input final, steps, gpu(optional)")
else:
    inputStart = sys.argv[1]
    inputFinal = sys.argv[2]
    steps = int(sys.argv[3])
    gpu = False
    if len(sys.argv) > 4:
        gpu = True
    
    indexesStart, coordsStart, el = getFrozenIndexes(inputStart)
    indexesFinal, coordsFinal, el = getFrozenIndexes(inputFinal)
    
    coordsFinalFixed = fixCoordinates(indexesStart, coordsStart, coordsFinal)
    frames = generateFrames(coordsStart, coordsFinalFixed, steps)
    
    for n, frame in enumerate(frames):
        dirname = "linerScan_"+str(n)
        mkdir(dirname)
        inputName = join(dirname, "linearScan.com")
        slurmFile = join(dirname, "linearScan.slurm")
        writeNewInput(inputStart, frame, inputName)
        writeSlurmScript(slurmFile, basename(inputName), gpu)
    
