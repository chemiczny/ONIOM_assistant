#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:06:50 2018

@author: michal
"""
from readingUtilities import isBlankLine, floatInList
import sys
from os.path import isdir, join, basename
from slurm import writeSlurmScript
from os import mkdir

def _energyFromComment( comment):
    if "scf done" in comment:
        return float(comment.split()[-1])
    elif "Energy" in comment:
        commentS = comment.split()
        return float( commentS[ commentS.index("Energy") + 1 ] )
    else:
        try:
            energy = float( comment.split()[0] )
            return energy
        except:
            return None

def readLastXyz( xyz):
 
    xyzF = open(xyz, 'r')
    
    line = xyzF.readline()
    atomsNo = int(line)

    line = xyzF.readline()
#    actualEnergy = _energyFromComment(line)
    
    i = 0
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
        
        if index != None and index != "max":
            if index == i:
                break
        
        i += 1
 
    xyzF.close()
    return elements, coords

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

def writeNewInput ( oldInput, newCoords, newInputName, indexes ):
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
    
    #charge and multiplicity    
    beginning += line
    line = oldFile.readline()
    
    beginning += line
    destiny.write(beginning)
    fullCoordsIndex = 0
    newCoordsIndex = 0
    while not isBlankLine(line):
        line = oldFile.readline()
        lineSpl = line.split()
        coordInd = floatInList(lineSpl)[-3:]
        
        if fullCoordsIndex in indexes:
            coord = newCoords[newCoordsIndex]
            for ci, crd in zip(coordInd, coord):
                lineSpl[ci] = str(crd)
            newCoordsIndex +=1
                
        destiny.write("\t".join(lineSpl)+"\n")
        fullCoordsIndex += 1
        
    line = oldFile.readline()
    while line:
        destiny.write(line)
        line = oldFile.readline()
    
    destiny.close()
    oldFile.close()
    
if len(sys.argv) < 5:
    print("Potrzebuje: g16Input, xyz file , index, file,  newInputName, ewentualnie index/max")
else:
    oldInput = sys.argv[1]
    xyz = sys.argv[2]
    indexFile = sys.argv[3]
    newInputName = sys.argv[4]
    index = None
    if len(sys) == 6:
        index = sys.argv[5]
        if index != "max":
            index = int(index)
    
    indexes = readIndexes(indexFile)
    newDir = newInputName.split(".")[0]
    
    if isdir(newDir):
        print("Wybrana sciezka juz istnieje!")
    else:
        mkdir(newDir)
        el, newCoords = readLastXyz(xyz)
        newInputName = join(newDir, newInputName)
        writeSlurmScript(join(newDir, "run.slurm"), basename(newInputName))
        writeNewInput(oldInput , newCoords, newInputName, indexes)