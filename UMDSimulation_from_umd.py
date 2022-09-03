# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:33:58 2022

@author: marco
"""


import numpy as np

from .libs.UMDAtom import UMDAtom
from .libs.UMDLattice import UMDLattice
from .libs.UMDSimulation import UMDSimulation
from .libs.UMDSimulationRun import UMDSimulationRun


def UMDSimulation_from_umd(umd):
    """
    Load a simulation from UMD file and initialize a UMDSimulation object.

    Parameters
    ----------
    umd : input file
        The UMD input file.

    Returns
    -------
    simulation : UMDSimulation
        A UMDSimulation object.

    """
    # We read line by line the UMD file. When we encounter the Simulation
    # section strating with 'Simulation:', we read the simulation information.
    runs = []
    line = umd.readline()
    while line:
        if 'Simulation:' in line:
            name = line.replace('Simulation:', '').strip()
            totcycle = int(umd.readline().strip().split()[-1])
            totsteps = int(umd.readline().strip().split()[-1])
            tottime = float(umd.readline().strip().split()[-2])
        elif 'Run' in line:
            cycle = int(line.replace(':', '').strip().split()[-1])
            steps = int(umd.readline().strip().split()[-1])
            steptime = float(umd.readline().strip().split()[-2])
            runs.append(UMDSimulationRun(cycle, steps, steptime))
        elif '--------------------------------------------' in line:
            # In the UMD file the Lattice section follows the Simulation.
            lattice = UMDLattice_from_umd(umd)
            print(lattice)
            simulation = UMDSimulation(name=name, lattice=lattice, runs=runs)
            assert totcycle == len(runs)
            assert totsteps == simulation.steps()
            assert tottime == simulation.time()
            return simulation
        line = umd.readline()


def UMDLattice_from_umd(umd):
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
    line = umd.readline()
    while line:
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
        line = umd.readline()
