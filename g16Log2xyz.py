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
    elements = [
    "H", "He",
    "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg"] 
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
                coords +=" "+ elements[z-1] + " "+newCoords+"\n"
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
