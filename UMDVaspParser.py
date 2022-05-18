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


from decorator_ProgressBar import ProgressBar

loadedSteps = 0
initialStep = 0
finalStep = 0
nSteps = np.infty


def UMDVaspParser(OUTCARfile, step0=0, nsteps=np.infty):
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

    # We open the output UMDfile
    UMDfile = OUTCARfile.replace('outcar', 'umd')
    with open(UMDfile, 'w') as umd:
        # Initialize and print a default UMDSimulation, totSimulation.
        # totSimulation records the real simulation information considered.
        # It is immediately printed in order to save the space that is
        # necessary to print the simulation total info at the end.
        simulation_name = OUTCARfile.replace('.outcar', '').split('/')[-1]
        totSimulation = UMDSimulation(name=simulation_name, cycle=0)
        totSimulation.save(umd)
        totSimulation.lattice.save(umd)
        umd.write(' '*6*20+'\n')
        umd.write(' '*6*20+'\n')

        # We open the input OUTCARfile
        with open(OUTCARfile, 'r') as outcar:
            # We read line by line untill the end of the OUTCAR file.
            # At each step of the loop, a complete simulation cycle is read
            # by the function load_SimulationCycle.
            line = outcar.readline()
            while line:
                # The function load_SimulationCycle() returns a UMDSimulation
                # object or None, if all the OUTCAR file has been read.
                simulation = load_SimulationCycle(outcar, umd,
                                                  totSimulation.cycle)
                if simulation is None:
                    break
                totSimulation.cycle += 1
                totSimulation.steps += simulation.steps
                totSimulation.time += simulation.simtime()
                totSimulation.lattice = simulation.lattice
                if loadedSteps >= initialStep + nSteps:
                    break
                line = outcar.readline()

        # Overwrite the defualt totSimulation initially printed in umd file,
        # with the updated and collective simulation info.
        umd.seek(0)
        totSimulation.save(umd)
        totSimulation.lattice.save(umd)
        print(totSimulation)
        return totSimulation


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
    simsteps = simulation.steps
    for step in range(loadedSteps, loadedSteps + simsteps):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/simsteps
    simulation.steps = 0


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
    simsteps = simulation.steps
    for step in range(loadedSteps, initialStep):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/simsteps
    for step in range(initialStep, loadedSteps+simsteps):
        snapshot = UMDSnapshot_from_outcar(outcar, step)
        snapshot.save(umd)
        yield float(step-loadedSteps)/simsteps
    simulation.steps = finalStep - initialStep


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
    simsteps = simulation.steps
    for step in range(loadedSteps, loadedSteps + simsteps):
        snapshot = UMDSnapshot_from_outcar(outcar, step)
        snapshot.save(umd)
        yield float(step-loadedSteps)/simsteps
    simulation.steps = finalStep - loadedSteps


def load_SimulationCycle(outcar, umd, cycle):
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

    simulation = UMDSimulation_from_outcar(outcar, cycle)
    if simulation is None:
        return
    else:
        print('Loaded simulation ...')
        print(simulation)
        print('Loading snapshots ...')
        simsteps = simulation.steps
        finalStep = min(initialStep+nSteps, loadedSteps+simsteps)
        UMDSnapshot.reset(simulation.steptime, simulation.lattice)
        if initialStep > loadedSteps + simsteps:
            simulation_before_initialStep(outcar, simulation)
        elif initialStep > loadedSteps:
            simulation_around_initialStep(outcar, umd, simulation)
        else:
            simulation_after_initialStep(outcar, umd, simulation)
        loadedSteps += simsteps
        print(' ... {} snapshots saved.\n'.format(simulation.steps))
        return simulation


UMDVaspParser('tests/mag5.70a1800T.outcar')