#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 15:13:58 2018

@author: michal
"""
import sys
from os.path import join, basename
from os import mkdir
from slurm import writeSlurmScript

def rewriteInput ( oldInput, newInputName, key, replacement ):
    oldFile = open(oldInput, 'r')
    line = oldFile.readline()
    destiny = open(newInputName, 'w')
    
    #route section
    while line:
        if key in line:
            line = line.replace(key, replacement)
        destiny.write(line)
        line = oldFile.readline()
    
    destiny.close()
    oldFile.close()
    
def writeSeries( oldInput, key, replacements, GPU = False ):
    mainDir = basename(oldInput).split(".")[0]+"series"
    mkdir(mainDir)
    
    for repl in replacements:
        newDir = "step"+str(repl)
        newDir = join(mainDir, newDir)
        mkdir(newDir)
        
        inputName = join(newDir, "step"+str(repl)+".com")
        rewriteInput(oldInput, inputName, key, repl )
        writeSlurmScript(join(newDir, "run.slurm"), basename(inputName), GPU)
        
if len(sys.argv) < 5:
    print("Potrzebuje: oldInput, gpu/cpu , key , replacement1, replacement2 ...")
else:
    
    oldInput = sys.argv[1]
    gpuOrCpu = sys.argv[2]
    key = sys.argv[3]
    replacements = sys.argv[4:]
    
    GPU = False
    if gpuOrCpu.upper() == "GPU":
        GPU = True
    
    writeSeries( oldInput, key, replacements, GPU)