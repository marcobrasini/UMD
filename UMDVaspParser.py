#
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:55:14 2022

@author: marco
"""

import os
import sys
import getopt
import numpy as np


from .UMDSimulation_from_outcar import UMDSimulation_from_outcar
from .UMDSnapshot_from_outcar import UMDSnapshot_from_outcar
from .UMDSnapshot_from_outcar import UMDSnapshot_from_outcar_null
from .libs.UMDSimulation import UMDSimulation
from .libs.UMDSnapshot import UMDSnapshot


from .decorator_ProgressBar import ProgressBar

loadedSteps = 0
initialStep = 0
finalStep = 0
nSteps = np.infty


def UMDVaspParser(outcarfile, step0=0, nsteps=np.infty):
    """
    Generate the UMD file extracting information from a Vasp OUTCAR file.

    Parameters
    ----------
    OUTCARfile : input file
        The OUTCAR file.

    # Returns
    -------
    totSimulation : UMDSimulation
        UMDSimulation object with the total cumulative information of all the
        cycles.

    """
    global initialStep, finalStep, nSteps, loadedSteps
    loadedSteps = 0
    finalStep = 0
    initialStep = step0
    nSteps = nsteps
    
    simulation_name = outcarfile.replace('.outcar', '').split('/')[-1]
    simulation = UMDSimulation(name=simulation_name)

    # We open the output UMDfile
    UMDfile = outcarfile.replace('outcar', 'umd')
    with open(UMDfile, 'w') as umd:
        # Initialize and print a default UMDSimulation, totSimulation.
        # totSimulation records the real simulation information considered.
        # It is immediately printed in order to save the space that is
        # necessary to print the simulation total info at the end.
        simulation.save(umd)

        # We open the input OUTCARfile
        with open(outcarfile, 'r') as outcar:
            # We read line by line untill the end of the OUTCAR file.
            # At each step of the loop, a complete simulation cycle is read
            # by the function load_SimulationCycle.
            line = outcar.readline()
            while line:
                # The function load_SimulationCycle() returns a UMDSimulation
                # object or None, if all the OUTCAR file has been read.
                cycle = simulation.cycle()
                simulation = load_SimulationRun(outcar, umd, simulation)
                if simulation.cycle() == cycle:
                    break
                if loadedSteps >= initialStep + nSteps:
                    break
                line = outcar.readline()
            outcar.close()

        # Overwrite the defualt totSimulation initially printed in umd file,
        # with the updated and collective simulation info.
        umd.seek(0)
        simulation.save(umd)
        umd.close()
        
    print(simulation)
    return simulation


@ProgressBar(20)
def simulation_before_initialStep(outcar, simulation):
    """
    Read the snapshots before the initialStep.

    The snapshots are read, but no UMDSnapshot object is built and saved.

    Parameters
    ----------
    outcar : input file
        The outcar file.
    simulation : UMDSimulation
        The current UMDSimulation.

    Yields
    ------
    float
        Ratio of the snapshot read.

    """
    run = simulation.runs[-1]
    steps = run.steps
    for step in range(loadedSteps, loadedSteps + steps):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = 0


@ProgressBar(20)
def simulation_around_initialStep(outcar, umd, simulation):
    """
    Read and load the snapshots when initialStep is in the current simulation.

    The snapshots before initialSteps are read, but no UMDSnapshot object is
    built and saved. The snapshots after initialSteps are read and for each a
    UMDSnapshot object is built and saved in the umd file.

    Parameters
    ----------
    outcar : input file
        The outcar file.
    umd : output file
        The umd file.
    simulation : UMDSimulation
        The current UMDSimulation.

    Yields
    ------
    float
        Ratio of the snapshot read.

    """
    run = simulation.runs[-1]
    steps = run.steps
    for step in range(loadedSteps, initialStep):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/steps
    for step in range(initialStep, loadedSteps+steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot = UMDSnapshot_from_outcar(outcar, snapshot)
        snapshot.save(umd)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = finalStep - initialStep


@ProgressBar(20)
def simulation_after_initialStep(outcar, umd, simulation):
    """
    Read and load the snapshots after initialStep.

    All the snapshots after initialSteps in the simulation are read and for
    each a UMDSnapshot object is built and saved in the umd file.

    Parameters
    ----------
    outcar : input file
        The outcar file.
    umd : output file
        The umd file.
    simulation : UMDSimulation
        The current UMDSimulation.

    Yields
    ------
    float
        Ratio of the snapshot read.

    """
    run = simulation.runs[-1]
    steps = run.steps
    for step in range(loadedSteps, loadedSteps + steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot = UMDSnapshot_from_outcar(outcar, snapshot)
        snapshot.save(umd)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = finalStep - loadedSteps


def load_SimulationRun(outcar, umd, simulation):
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
          According to the current simulation cycle and the initialStep, the
          snapshots are managed by one of the following functions:
              - simulation_before_initialStep
              - simulation_around_initialStep
              - simulation_after_initialStep

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
    global loadedSteps, initialStep, finalStep, nSteps

    cycle = simulation.cycle()
    simulation = UMDSimulation_from_outcar(outcar, simulation)
    if simulation.cycle() == cycle:
        return simulation
    else:
        if cycle == 0:
            simulation.lattice.save(umd)
        run = simulation.runs[-1]
        print('Loaded simulation run...')
        print(run)
        print('Loading snapshots ...')
        steps = run.steps
        finalStep = min(initialStep+nSteps, loadedSteps+steps)
        if initialStep > loadedSteps + steps:
            simulation_before_initialStep(outcar, simulation)
        elif initialStep > loadedSteps:
            simulation_around_initialStep(outcar, umd, simulation)
        else:
            simulation_after_initialStep(outcar, umd, simulation)
        loadedSteps += steps
        print(' ... {} snapshots saved.\n'.format(run.steps))
        return simulation


#UMDVaspParser('./tests/examples/OUTCAR_single.outcar')
