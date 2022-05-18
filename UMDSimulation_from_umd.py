# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:33:58 2022

@author: marco
"""


import numpy as np
from UMDLattice import UMDLattice
from UMDSimulation import UMDSimulation


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
            name = line.replace('Lattice', '').strip()
            basis = np.zeros((3, 3))
            for i in range(3):
                basis[i] = umd.readline().strip().split()
            atoms_name = umd.readline().split()
            atoms_number = [int(n) for n in umd.readline().split()]
            atoms = dict(zip(atoms_name, atoms_number))
            lattice = UMDLattice(name=name, basis=basis, atoms=atoms)
            return lattice
        line = umd.readline()


def UMDSimulation_from_umd(umdfile):
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
    line = umdfile.readline()
    while line:
        if 'Simulation:' in line:
            name = line.replace('Simulation:', '').strip()
            cycle = int(umdfile.readline().strip().split()[-1])
            steps = int(umdfile.readline().strip().split()[-1])
            time = float(umdfile.readline().strip().split()[-2])
            # In the UMD file the Lattice section follows the Simulation.
            lattice = UMDLattice_from_umd(umdfile)
            simulation = UMDSimulation(name=name, lattice=lattice, cycle=cycle,
                                       steps=steps, time=time)
            return simulation
        line = umdfile.readline()
