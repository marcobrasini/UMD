# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:55:14 2022

@author: marco
"""

import numpy as np

from UMDSimulation_from_outcar import UMDSimulation_from_outcar
from UMDSnapshot_from_outcar import UMDSnapshot_from_outcar
from UMDSnapshot_from_outcar import UMDSnapshot_from_outcar_null
from UMDSimulation import UMDSimulation
from UMDSnapshot import UMDSnapshot


loadedSteps = 0
initialStep = 0
nSteps = np.infty


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
        # Initialize and print a default UMDSimulation, totSimulation.
        # totSimulation records the real simulation information considered.
        # It is immediately printed in order to save the space that is
        # necessary to print the simulation total info at the end.
        simulation_name = OUTCARfile.replace('.outcar', '').split('/')[-1]
        totSimulation = UMDSimulation()
        totSimulation.save(umd)

        cycle = 0
        totalTime = 0.0
        totalSteps = 0
        # We open the input OUTCARfile
        with open(OUTCARfile, 'r') as outcar:
            # We read a line per time untill the end of the OUTCARfile.
            # At each step of the loop, a complete simulation cycle is read
            # by the function load_SimulationCycle.
            line = outcar.readline()
            while line:
                # The function load_SimulationCycle() returns a UMDSimulation
                # object or None, if all the OUTCARfile has been read.
                simulation = simulationCycleParser(outcar, umd, cycle)
                if simulation is None:
                    break
                cycle += 1   # update the simulation cycle number.
                totalSteps += simulation.steps
                totalTime += simulation.simtime()
                if loadedSteps >= initialStep + nSteps:
                    break
                line = outcar.readline()

        # Overwrite the defualt totSimulation initially printed in umd file,
        # with the updated and collective simulation info.
        umd.seek(0)
        totSimulation = UMDSimulation(name=simulation_name, cycle=cycle,
                                      steps=totalSteps,
                                      time=totalTime)
        totSimulation.save(umd)


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
    global loadedSteps, initialStep, nSteps

    simulation = UMDSimulation_from_outcar(outcar, cycle)
    if simulation is None:
        return
    else:
        simsteps = simulation.steps
        finalStep = min(initialStep+nSteps, loadedSteps+simsteps)
        UMDSnapshot.reset(simulation.steptime, simulation.lattice)
        if initialStep > loadedSteps + simsteps:
            for step in range(loadedSteps, loadedSteps + simsteps):
                UMDSnapshot_from_outcar_null(outcar)
            simulation.steps = 0
        elif initialStep > loadedSteps:
            for step in range(loadedSteps, initialStep):
                UMDSnapshot_from_outcar_null(outcar)
            for step in range(initialStep, finalStep):
                snapshot = UMDSnapshot_from_outcar(outcar, step)
                snapshot.save(umd)
            simulation.steps = finalStep - initialStep
        else:
            for step in range(loadedSteps, finalStep):
                snapshot = UMDSnapshot_from_outcar(outcar, step)
                snapshot.save(umd)
            simulation.steps = finalStep - loadedSteps

        loadedSteps += simsteps
        return simulation


UMDVaspParser('tests/mag5.70a1800T.outcar')
