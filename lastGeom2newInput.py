#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:42:17 2018

@author: michal
"""
import sys
from os.path import isdir, join, basename
from os import mkdir
from readingUtilities import isBlankLine, floatInList
from slurm import writeSlurmScript

def getCoordsFromLog(logFile, index):
    gFile = open(logFile, 'r' )
    
    allCoords = []
    line = gFile.readline()
    while line:
       
        if "Coordinates" in line:
            
            for i in range(3):
                line = gFile.readline()
                
            coords = []
            atomNo = 0
            while not "-----" in line:
                lineS = line.split()
                newCoords = "\t".join(lineS[-3:])
                coords.append(newCoords.split())
                atomNo +=1
                line = gFile.readline()
                
            allCoords.append(coords)
                
        
        line = gFile.readline()
        
        
    gFile.close()
    return allCoords[index]

def getCoordInd( lineSpl ):
    floatInd = floatInList(lineSpl)

    contInd = [ floatInd[0] ]
    lastElement = floatInd[0]

    for ind in floatInd[1:]:
        if ind-lastElement == 1:
            contInd.append(ind)
        else:
            break
        lastElement = ind

    return contInd[-3:]

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
        coordInd = getCoordInd( lineSpl )
        for ci, crd in zip(coordInd, coord):
            lineSpl[ci] = str(crd)
        destiny.write("\t".join(lineSpl)+"\n")
        
    line = oldFile.readline()
    while line:
        destiny.write(line)
        line = oldFile.readline()
    
    destiny.close()
    oldFile.close()

if len(sys.argv) < 4:
    print("Potrzebuje: g16Log, oldInput, newInputName, geometry index [optional, negative indexes possible]")
else:
    
    g16Log = sys.argv[1]
    oldInput = sys.argv[2]
    newInputName = sys.argv[3]
    index = -1
    if len(sys.argv) > 4:
        index = int(sys.argv[4])
        
    newDir = newInputName.split(".")[0]
    
    if isdir(newDir):
        print("Wybrana sciezka juz istnieje!")
    else:
        mkdir(newDir)
        last = getCoordsFromLog(g16Log, index)
        newInputName = join(newDir, newInputName)
        writeNewInput(oldInput, last, newInputName)
        writeSlurmScript(join(newDir, "run.slurm"), basename(newInputName), False)
