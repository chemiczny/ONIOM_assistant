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

def getLastCoordsFromLog(logFile):
    gFile = open(logFile, 'r' )
    
    
    line = gFile.readline()
    firstCoords = True
    while line:
       
        if "Coordinates" in line:
            if firstCoords:
                firstCoords = False
                line = gFile.readline()
                continue
            
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
                
        
        line = gFile.readline()
        
        
    gFile.close()
    return coords

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

if len(sys.argv) < 4:
    print("Potrzebuje: g16Log, oldInput, newInputName, GPU(optional)")
else:
    
    g16Log = sys.argv[1]
    oldInput = sys.argv[2]
    newInputName = sys.argv[3]
    GPU = False
    if len(sys.argv) > 4:
        GPU = True
        
    newDir = newInputName.split(".")[0]
    
    if isdir(newDir):
        print("Wybrana sciezka juz istnieje!")
    else:
        mkdir(newDir)
        last = getLastCoordsFromLog(g16Log)
        newInputName = join(newDir, newInputName)
        writeNewInput(oldInput, last, newInputName)
        writeSlurmScript(join(newDir, "run.slurm"), basename(newInputName), GPU)
