#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 22:04:05 2018

@author: michal
"""
from readingUtilities import isBlankLine, floatInList
import numpy as np
import sys
from os.path import isdir, join, basename
from os import mkdir
from slurm import writeSlurmScript

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

def appendCoords2File( elements, coords, file2append ):
    xyz = open(file2append, 'a')
    xyz.write(str(len(elements))+"\n\n")
    
    for el, c in zip(elements, coords):
        xyz.write(el+"\t" + str(c[0])+"\t"+str(c[1])+"\t"+str(c[2])+"\n")
        
    
    xyz.close()


if len(sys.argv) != 4:
    print( "Substrate inp, product inp, dir name")
else:
    template = sys.argv[1]
    inp2fix = sys.argv[2]
    dirname = sys.argv[3]
    

    indexes, coords, elements = getFrozenIndexes(inp2fix)
    indexes2, coords2, elements2 = getFrozenIndexes(template)
    
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
    
    if not isdir(dirname):
        mkdir(dirname)
        
        xyzFile = join(dirname, dirname+".xyz")
        appendCoords2File(elements, coords2, xyzFile)
        appendCoords2File(elements, newCoords1, xyzFile)
        
        inpFile = join(dirname, dirname+".inp")
        
        inputFile = open(inpFile, 'w')
        xyzName = basename(xyzFile)
        
        inputFile.write("basis 6-31g**\n")
        inputFile.write("charge 0\n")
        inputFile.write("run ts\n")
        inputFile.write("method ub3lyp\n")
        inputFile.write("new_minimizer yes\n")
        inputFile.write("coordinates "+xyzName+"\nend\n\n")
        
        frozen = []
        for f in indexes:
            frozen.append(str(f+1))
            
            
        if frozen:
            inputFile.write("$constraint_freeze\n")
            if frozen:
                inputFile.write("xyz "+",".join(frozen)+"\n")
                
            inputFile.write("$end\n")
        
        inputFile.close()
        
        
        writeSlurmScript(join(dirname, dirname+".slurm"), basename(inpFile), True, "terachem")
    else:
        print("katalog "+dirname+" juz istnieje")
    

