#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:25:40 2018

@author: michal
"""

def writeSlurmScript( filename, file2run, GPU = False, software = "g16"):
    slurmFile = open(filename, 'w')
    if not GPU:
        slurmFile.write("#!/bin/env bash\n")
        slurmFile.write("#SBATCH --nodes=1\n")
        slurmFile.write("#SBATCH --cpus-per-task=24\n")
        slurmFile.write("#SBATCH --time=72:00:00\n")
        slurmFile.write("#SBATCH -p plgrid\n\n")
    else:
        slurmFile.write("#!/bin/env bash\n")
        slurmFile.write("#SBATCH --nodes=1\n")
        if software == "g16" :
            slurmFile.write("#SBATCH --cpus-per-task=24\n")
        else:
            slurmFile.write("#SBATCH --ntasks-per-node=2\n")
        slurmFile.write("#SBATCH --gres=gpu:2\n")
        slurmFile.write("#SBATCH --time=3-0\n")
        slurmFile.write("#SBATCH -p plgrid-gpu\n\n")
                    
    if software == "g16":
        slurmFile.write("module add plgrid/apps/gaussian/g16.B.01\n")
        slurmFile.write("g16 " + file2run + "\n")
    else:
        slurmFile.write("module add  plgrid/apps/terachem\n")
        slurmFile.write("$TERACHEMRUN " + file2run + " > output.log\n")
    
    slurmFile.close()