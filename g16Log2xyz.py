#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 11:49:11 2018

@author: michal
"""
import sys

def g16Log2xyz( g16log, xyz ):
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
            while not "-----" in line:
                lineS = line.split()
                z = int(lineS[1])
                newCoords = "\t".join(lineS[-3:])
                coords +=" "+ elements[z] + " "+newCoords+"\n"
                atomNo +=1
                line = ircFile.readline()
                
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

if len(sys.argv) == 1:
    print( "Give me gaussian log")
else:
    g16Log = sys.argv[1] 
    xyz = g16Log[:-3]+"xyz"
    g16Log2xyz(g16Log, xyz)
