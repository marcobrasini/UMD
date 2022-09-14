# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:08:28 2022

@author: marco
"""


import numpy as np

from .libs.UMDSnapshot import UMDSnapshot
from .UMDSimulation_from_outcar import UMDSimulation_from_outcar

from .decorator_ProgressBar import ProgressBar


class _param_:
    _initialStep = 0
    _finalStep = 0
    _loadedSteps = 0
    _nSteps = np.infty


def load_UMDSimulationRun(outcar, umd, simulation):
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
    loadedSteps = _param_._loadedSteps
    initialStep = _param_._initialStep
    finalStep = _param_._finalStep
    nSteps = _param_._nSteps

    cycle = simulation.cycle()
    simulation = UMDSimulation_from_outcar(outcar, simulation)
    if simulation.cycle() == cycle:
        return simulation
    else:
        run = simulation.runs[-1]
        print('Loaded simulation run...')
        print(run)
        print('Loading snapshots ...')
        steps = run.steps
        finalStep = min(initialStep+nSteps, loadedSteps+steps)
        if initialStep > loadedSteps + steps:
            _simulation_before_initialStep(outcar, simulation)
        elif initialStep > loadedSteps:
            _simulation_around_initialStep(outcar, umd, simulation)
        else:
            _simulation_after_initialStep(outcar, umd, simulation)
        loadedSteps += steps
        print(' ... {} snapshots saved.\n'.format(run.steps))
        
        _param_._loadedSteps = loadedSteps
        _param_._initialStep = initialStep
        _param_._finalStep = finalStep
        _param_._nSteps = nSteps
        
        return simulation


@ProgressBar(20)
def _simulation_before_initialStep(outcar, simulation):
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
    loadedSteps = _param_._loadedSteps
    steps = run.steps
    for step in range(loadedSteps, loadedSteps + steps):
        UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = 0


@ProgressBar(20)
def _simulation_around_initialStep(outcar, umd, simulation):
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
    loadedSteps = _param_._loadedSteps
    initialStep = _param_._initialStep
    finalStep = _param_._finalStep
    for step in range(loadedSteps, initialStep):
        UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
        yield float(step-loadedSteps)/steps
    for step in range(initialStep, loadedSteps+steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot.UMDSnapshot_from_outcar(outcar)
        snapshot.save(umd)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = finalStep - initialStep


@ProgressBar(20)
def _simulation_after_initialStep(outcar, umd, simulation):
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
    loadedSteps = _param_._loadedSteps
    initialStep = _param_._initialStep
    finalStep = _param_._finalStep
    for step in range(loadedSteps, loadedSteps + steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot.UMDSnapshot_from_outcar(outcar)
        snapshot.save(umd)
        yield float(step-loadedSteps)/steps
    simulation.runs[-1].steps = finalStep - loadedSteps
