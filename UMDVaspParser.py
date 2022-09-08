"""
==============================================================================
                                UMDVaspParser
==============================================================================

This module provides the UMDVaspParser function necessary to generate the UMD
file starting from a Vasp OUTCAR file.
The Vasp OUTCAR file can contain a single simulation run or aslo multiple
simulation runs concatenated. The UMDVaspParser function allows to set the
index of the initial snapshot and the total number of snapshots to consider
thanks to the initialStep and the nSteps arguments respectively.

Functions
---------
    UMDVaspParser

See Also
--------
    UMDSimulation
    load_UMDSimulationRun

"""


import os
import numpy as np

from .libs.UMDSimulation import UMDSimulation
from .load_UMDSimulationRun import load_UMDSimulationRun
from .load_UMDSimulationRun import _param_


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

    _param_._loadedSteps = 0
    _param_._finalStep = 0
    _param_._initialStep = initialStep
    _param_._nSteps = nSteps

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
                if _param_._loadedSteps >= initialStep + nSteps:
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
