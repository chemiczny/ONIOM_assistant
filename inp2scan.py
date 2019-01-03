#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 15:13:58 2018

@author: michal
"""
import numpy as np
import sys
from os.path import join, basename
from os import mkdir
from readingUtilities import isBlankLine, floatInList
from slurm import writeSlurmScript

def getCoordsFromInp( oldInput ):
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
    
    coords = []
    while not isBlankLine(line):
        
        lineSpl = line.split()
        coordInd = floatInList(lineSpl)[-3:]
        newCoords = [ float(lineSpl[c]) for c in coordInd]
        coords.append(newCoords)
        line = oldFile.readline()
    
    oldFile.close()
    
    return coords

def writeNewInput ( oldInput, newCoords, newInputName, modredundantLines ):
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
    nonBondParameters = False
    while line:
        if "NonBon" in line and modredundantLines:
            destiny.write(modredundantLines)
            destiny.write("\n\n")
            nonBondParameters = True
        
        destiny.write(line)
        line = oldFile.readline()
        
    if not nonBondParameters:
        destiny.write(modredundantLines)
        destiny.write("\n")
    
    destiny.close()
    oldFile.close()
    
def writeScans( oldInput, coords, atomStart, atom2Move, atomDir, nSteps, minDist, GPU = False ):
    atomStartIndex = atomStart
    atomStart = np.array(coords[atom2Move])
    atomStop = np.array(coords[atomDir])
    
    moveVector = atomStop - atomStart
    length = np.linalg.norm(moveVector)
    
    moveVector = moveVector*(length-minDist)/length
    step = moveVector/nSteps
    mainDir = basename(oldInput).split(".")[0]+"scan"
    mkdir(mainDir)
    
    for i in range(nSteps):
        newDir = "step"+str(i)
        newDir = join(mainDir, newDir)
        mkdir(newDir)
        atomStart += step
        coords[atom2Move] = atomStart.tolist() 
        inputName = join(newDir, "step"+str(i)+".com")
        writeNewInput(oldInput, coords, inputName, "B "+str(atomStartIndex+1)+" " + str(atom2Move+1)+" F\n")
        writeSlurmScript(join(newDir, "run.slurm"), basename(inputName), GPU)
        
if len(sys.argv) < 7:
    print("Potrzebuje: oldInput, atomStart, atom2push, atomStop, nSteps, minDist, GPU(optional)")
else:
    
    oldInput = sys.argv[1]
    atomStart = int(sys.argv[2])
    atom2move = int(sys.argv[3])
    atomDir = int(sys.argv[4])
    nSteps = int(sys.argv[5])
    minDist = float(sys.argv[6])
    GPU = False
    if len(sys.argv) > 7:
        GPU = True
    
    coords = getCoordsFromInp(oldInput)
    writeScans( oldInput, coords, atomStart, atom2move, atomDir , nSteps, minDist, GPU)