#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:25:40 2018

@author: michal
"""

def writeSlurmScript( filename, file2run):
    slurmFile = open(filename, 'w')
    slurmFile.write("#!/bin/env bash\n")
    slurmFile.write("#SBATCH --nodes=1\n")
    slurmFile.write("#SBATCH --cpus-per-task=24\n")
    slurmFile.write("#SBATCH --time=72:00:00\n")
    slurmFile.write("#SBATCH -p plgrid\n\n")
                    
    slurmFile.write("module add plgrid/apps/gaussian/g16.B.01\n")
    slurmFile.write("inputDir=`pwd`\n")
    slurmFile.write("cp * $SCRATCHDIR\n")
    slurmFile.write("cd $SCRATCHDIR\n")
    slurmFile.write("g16 " + file2run + "\n")
    slurmFile.write("cp *.log $inputDir 2>/dev/null\n")
    
    slurmFile.close()