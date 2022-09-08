"""
==============================================================================
                                UMDVaspParser
==============================================================================

This module provides the UMDVaspParser function necessary to generate the UMD
file starting from a Vasp OUTCAR file.
The Vasp OUTCAR file can also contain multiple simulations run concatenated.

Functions
---------
    UMDVaspParser
    load_UMDSimulationRun

See Also
--------
    UMDSimulation_from_outcar
    UMDSnapshot_from_outcar
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

_loadedSteps = 0
_initialStep = 0
_finalStep = 0
_nSteps = np.infty


def UMDVaspParser(outcarfile, initialStep=0, nSteps=np.infty):
    """
    Generate the UMD file extracting information from a Vasp OUTCAR file.

    Parameters
    ----------
    outcarfile : input file
        The OUTCAR file.
    initialStep : int
        The initial snapshot index from which it starts to convert data. If the
        initial snapshot exceeds the number of snapshots available, no
        snapshot is used.
    nSteps : int
        The total number of snapshots to convert. If the number of snapshot
        exceeds the number of snapshots available, all the possible snapshots
        (after the initialStep) in the OUTCAR file are used.

    # Returns
    -------
    simulation : UMDSimulation
        The UMDSimulation object with the total information of all the
        simulation runs contained in the OUTCAR file.

    """
    if initialStep < 0:
        raise(ValueError('invalid initialStep value: it must be positive.'))
    if nSteps < 0:
        raise(ValueError('invalid nStep value: it must be positive.'))
    
    global _initialStep, _finalStep, _nSteps, _loadedSteps
    _loadedSteps = 0
    _finalStep = 0
    _initialStep = initialStep
    _nSteps = nSteps

    simulation_name = outcarfile.replace('.outcar', '').split('/')[-1]
    simulation = UMDSimulation(name=simulation_name)

    # We open a temporary UMD output file to store the UMDSnapshot information.
    UMDfile = outcarfile.replace('outcar', 'umd')
    with open(UMDfile+'.temp', 'w+') as temp:
        # We open the OUTCAR input file to read all the UMDSimulation and
        # UMDSnapshot information.
        with open(outcarfile, 'r') as outcar:
            # The OUTCAR file is read line by line untill its end.
            # At each simulation run is read by the load_SimulationRun function
            # and added to the total simulation in the UMDSimulation object.
            line = outcar.readline()
            while line:
                # The load_SimulationRun function returns the updated
                # UMDSimulation object. If the UMDSimulationRun object is not
                # updated, then it has reached the end of the OUTCAR file.
                cycle = simulation.cycle()
                simulation = load_UMDSimulationRun(outcar, temp, simulation)
                if simulation.cycle() == cycle:
                    break
                if _loadedSteps >= _initialStep + _nSteps:
                    break
                line = outcar.readline()
            outcar.close()

        with open(UMDfile, 'w') as umd:
            # We now create the real UMD file, with the UMDSimulation
            # information in the header and then all the UMDSnapshot stored in
            # the temporary UMD file.
            simulation.save(umd, saveRuns=True)
            umd.write(145*'-'+'\n\n')
            simulation.lattice.save(umd)
            umd.write(145*'-'+'\n\n')
            temp.seek(0)
            umd.write(temp.read())
            umd.close()
        # The temporary UMD file is removed.
        temp.close()
        os.remove(UMDfile+'.temp')

    print(simulation)
    return simulation


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
    global _loadedSteps, _initialStep, _finalStep, _nSteps

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
        _finalStep = min(_initialStep+_nSteps, _loadedSteps+steps)
        if _initialStep > _loadedSteps + steps:
            _simulation_before_initialStep(outcar, simulation)
        elif _initialStep > _loadedSteps:
            _simulation_around_initialStep(outcar, umd, simulation)
        else:
            _simulation_after_initialStep(outcar, umd, simulation)
        _loadedSteps += steps
        print(' ... {} snapshots saved.\n'.format(run.steps))
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
    steps = run.steps
    for step in range(_loadedSteps, _loadedSteps + steps):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-_loadedSteps)/steps
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
    for step in range(_loadedSteps, _initialStep):
        UMDSnapshot_from_outcar_null(outcar)
        yield float(step-_loadedSteps)/steps
    for step in range(_initialStep, _loadedSteps+steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot = UMDSnapshot_from_outcar(outcar, snapshot)
        snapshot.save(umd)
        yield float(step-_loadedSteps)/steps
    simulation.runs[-1].steps = _finalStep - _initialStep


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
    for step in range(_loadedSteps, _loadedSteps + steps):
        snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
        snapshot = UMDSnapshot_from_outcar(outcar, snapshot)
        snapshot.save(umd)
        yield float(step-_loadedSteps)/steps
    simulation.runs[-1].steps = _finalStep - _loadedSteps