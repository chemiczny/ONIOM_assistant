#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 16:09:15 2018

@author: michal
"""
import sys
from readingUtilities import isBlankLine, floatInList

def readHighLayerIndexesFromInput( oldInput ):
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
    actualIndex = 0
    while not isBlankLine(line):
        
        lineSpl = line.split()
        coordInd = floatInList(lineSpl)[-3:]
        
        layerInd = lineSpl[coordInd[-1]+1]
        
        if "H" == layerInd.upper():
            indexes.append(actualIndex)
            
        line = oldFile.readline()
        actualIndex += 1
    
    oldFile.close()
    
    return indexes

def g16Log2xyz( g16log, xyz, indexes ):
    ircFile = open(g16log, 'r' )
    xyz = open(xyz, 'w')
    
    
    line = ircFile.readline()
    elements = { 6 : "C", 7 : "N", 8 : "O", 1 : "H", 16 : "S", 15 : "S" }
    firstCoords = True
    while line:
       
        if "Coordinates" in line:
            if firstCoords:
                firstCoords = False
                line = ircFile.readline()
                continue
            
            for i in range(3):
                line = ircFile.readline()
                
            coords = ""
            atomNo = 0
            actualIndex = 0
            
            while not "-----" in line:
                if actualIndex in indexes:
                    lineS = line.split()
                    z = int(lineS[1])
                    newCoords = "\t".join(lineS[-3:])
                    coords +=" "+ elements[z] + " "+newCoords+"\n"
                    atomNo +=1
                line = ircFile.readline()
                actualIndex += 1
                
            limit = 1000
            it = 0
            while not "SCF Done" in line and it < limit:
                line = ircFile.readline()
                it += 1
            if not "SCF Done" in line:
                line = ircFile.readline()
                continue
                
            energy = float(line.split()[4])
            xyz.write(" "+str(atomNo)+ "\n")
            xyz.write("scf done: "+str(energy)+"\n")
            xyz.write(coords)
        
        
        line = ircFile.readline()
        
        
    ircFile.close()
    xyz.close()

if len(sys.argv) < 4:
    print("Potrzebuje: input, log, xyz (output) ")
else:
    
    inputFile = sys.argv[1]
    logFile = sys.argv[2]
    xyzFile = sys.argv[3]
    
    highIndexes = readHighLayerIndexesFromInput(inputFile)
    g16Log2xyz(logFile, xyzFile, highIndexes)