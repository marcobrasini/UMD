"""
===============================================================================
                           load_UMDSimulation_from_umd
===============================================================================

This module provides the load_UMDSimulation_from_umd function implementation.
The load_UMDSimulation_from_umd function is necessary to extract the simulation
parameters from a UMD file.
Simulation informations are reported at the beginning of the UMD file. From the
initial part of the UMD file, we get the informations to initialize both
UMDLattice (atom types, number of atoms and basis vectors), the UMDSimulation
and the UMDSimulationRun (number of iteration and snapshot time duration).

UMD HEADER
The header is divided in three different sections.
 + the simulation section summarizing the total simulation parameters.
   The simulation section has the following structure:
       Simulation: ""
       Total cycles = xxxxxxxxxxxx
       Total steps  = xxxxxxxxxxxx
       Total time   = xxxxxxxxxxxx fs
 + the simulation run section where there are listed the parameters for each
   simulation run.
   Each simulation run section has the following structure:
       Run        x:
       Steps     = xxxxxxxx
       Step time = xxxxxxxx (fs)
 + the lattice section where it is described the cell structure and the atoms.
   The lattice section has the following structure:
       Lattice: ""
              a_x             a_y             a_z
              b_x             b_y             b_z
              c_x             c_y             c_z
       [atom1]       [atom2]       ...
           [mass1]      [mass2]    ...
        [valence1]   [valence2]    ...
         [number1]    [number2]    ...
"""


import numpy as np

from .libs.UMDAtom import UMDAtom
from .libs.UMDLattice import UMDLattice
from .libs.UMDSimulationRun import UMDSimulationRun


def load_UMDSimulationRun_from_umd(umd):
    """
    Load the simulation runs from UMD file.

    Parameters
    ----------
    umd : input stream
        The UMD input stream.

    Returns
    -------
    runs : list
        A list of UMDSimulationRun objects.

    """
    # We read line by line the UMD file. When we encounter the Simulation
    # section strating with 'Simulation:', we read the simulation information.
    runs = []
    for line in umd:
        if 'Run' in line:
            cycle = int(line.replace(':', '').strip().split()[-1])
            steps = int(umd.readline().strip().split()[-1])
            steptime = float(umd.readline().strip().split()[-2])
            runs.append(UMDSimulationRun(cycle, steps, steptime))
        elif '--------------------------------------------' in line:
            # In the UMD file the Lattice section follows the Simulation.
            return runs
    raise(EOFError('UMD file end with UMDSimulation uninitialized.'))


def load_UMDLattice_from_umd(umd):
    """
    Load a lattice from a UMD file and initialize a UMDLattice object.

    Parameters
    ----------
    umd : input file
        The UMD input file.

    Returns
    -------
    lattice : UMDLattice
        A UMDLattice object.

    """
    # We read line by line the UMD file. When we encounter the Lattice section
    # strating with 'Lattice:', we read the lattice structure data.
    for line in umd:
        if 'Lattice:' in line:
            lattice_name = line.replace('Lattice:', '').strip()
            lattice_basis = np.zeros((3, 3))
            for i in range(3):
                lattice_basis[i] = umd.readline().strip().split()
            name = [at for at in umd.readline().split()]
            mass = [float(m) for m in umd.readline().split()]
            valence = [float(v) for v in umd.readline().split()]
            atoms_number = [int(n) for n in umd.readline().split()]
            atoms_key = [UMDAtom(name=name[i], mass=mass[i],
                                 valence=valence[i]) for i in range(len(name))]
            atoms = dict(zip(atoms_key, atoms_number))
            lattice = UMDLattice(name=lattice_name, basis=lattice_basis,
                                 atoms=atoms)
            return lattice
    raise(EOFError('UMD file end with UMDLattice uninitialized.'))
