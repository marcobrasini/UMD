# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:55:14 2022

@author: marco
"""


def UMDVaspParser(OUTCARfile):
    """
    Generate the UMD file extracting information from a Vasp OUTCAR file.

    Parameters
    ----------
    OUTCARfile : input file
        The OUTCAR file.

    Returns
    -------
    None.

    """
    # We open the output UMDfile 
    UMDfile = OUTCARfile.replace('outcar', 'umd')
    with open(UMDfile, 'w') as umd:
        simcycle = 0
        # We open the input OUTCARfile
        with open(OUTCARfile, 'r') as outcar:
            # We read a line per time untill the end of the OUTCARfile.
            # At each step of the loop, a complete simulation cycle is read
            # by the function load_SimulationCycle.
            line = outcar.readline()
            while line:
                # The function load_SimulationCycle() returns a UMDSimulation
                # object or None, if all the OUTCARfile has been read.
                simulation = simulationCycleParser(simcycle, outcar, umd)
                if simulation is None:
                    break
                simcycle += 1   # update the simulation cycle number.
                line = outcar.readline()
