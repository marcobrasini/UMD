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
    Load_OUTCAR
    UMDSimulation

"""


import os
import numpy as np

from .load_OUTCAR import Load_OUTCAR
from .libs.UMDSimulation import UMDSimulation


def UMDVaspParser(outcarfile_name, initialStep=0, nSteps=np.infty):
    """
    Generate the UMD file extracting information from a Vasp OUTCAR file.

    Parameters
    ----------
    outcarfile : string
        The name of the input OUTCAR file.
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

    load_OUTCAR = Load_OUTCAR(initialStep=initialStep, nSteps=nSteps)

    simulation_name = outcarfile_name.replace('.outcar', '').split('/')[-1]
    simulation = UMDSimulation(name=simulation_name)

    # We open a temporary UMD output file to store the UMDSnapshot information.
    UMDfile = outcarfile_name.replace('outcar', 'umd')
    with open(UMDfile+'.temp', 'w+') as temp:
        # We open the OUTCAR input file to read all the UMDSimulation and
        # UMDSnapshot information.
        with open(outcarfile_name, 'r') as outcar:
            # The OUTCAR file is read line by line untill its end.
            # Each simulation run is read by the Load_OUTCAR.load function
            # and added to the total simulation in the UMDSimulation object.
            try:
                for line in outcar:
                    # The Load_OUTCAR.load function returns the updated
                    # UMDSimulation object. If the end of the OUTCAR file is
                    # reached, then a EOFError is raised.
                    simulation = load_OUTCAR.load(outcar, temp, simulation)
                    if load_OUTCAR.loadedSteps >= initialStep+nSteps:
                        break
            except(EOFError) as eof:
                print(eof)

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

    # The temporary UMD file is removed.
    os.remove(UMDfile+'.temp')

    print(simulation)
    return simulation
