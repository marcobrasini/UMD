# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:55:14 2022

@author: marco
"""

from UMDSimulation_from_outcar import UMDSimulation_from_outcar
from UMDSnapshot_from_outcar import UMDSnapshot_from_outcar
from UMDSnapshot import UMDSnapshot


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
                simulation = simulationCycleParser(outcar, umd, simcycle)
                if simulation is None:
                    break
                simcycle += 1   # update the simulation cycle number.
                line = outcar.readline()


def simulationCycleParser(outcar, umd, cycle):
    """
    Read from OUTCAR file and print on UMD file the data of a simulation cycle.

    The function is implemented in two functions:
        - UMDSimulation_from_outcar,
          to read the lattice structure and the simulation parameters which
          are fixed for every snapshot of the simulation.
          If no UMDSimulation is initialized, then None is returned.
        - UMDSnapshot_from_outcar,
          to read each individual snapshots in the simulation.
          The number of snapshots read depends on the number of iterations set
          among the simulation parameters.

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.
    umd : output file
        The UMD file.
    cycle : int
        The cycle number of the simulation.

    Returns
    -------
    simulation : UMDsimulation
        The UMDSimulation object initialized by the UMDSimulation_from_outcar
        function. It is None when the OUTCAR file is finished.

    """
    simulation = UMDSimulation_from_outcar(outcar, cycle)
    if simulation is None:
        return
    else:
        simSteps = simulation.steps
        UMDSnapshot.reset(simulation.steptime, simulation.lattice)
        for step in range(0, simSteps):
            snapshot = UMDSnapshot_from_outcar(outcar, step)
            snapshot.save(umd)
        return simulation
