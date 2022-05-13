 # -*- coding: utf-8 -*-
"""
Created on Thu May  5 16:55:51 2022

@author: marco
"""
"""
Simulation informations are reported in the header of the OUTCAR file.

From the initial part of the OUTCAR file we get the informations to initialize
both UMDLattice (atom types, number of atoms and basis vectors) and the
UMDSimulation (number of iteration and snapshot time duration).

OUTCAR header structure.
The header if devided into the following section:
+ A header with the Vasp version, data-time of the beginning and executing
  machine information (type, number of cores and the number of cores per band)
+ A summary of the Vasp input files:
    - the INCAR:
    - the POTCAR:
      # VRHFIN =X: ele.conf. -> to obtain the atomic symbol 'X'
    - the POSCAR:
    - the KPOINTS:
+ A report of all the run parameters grouped in the following sections:
    - Dimension of arrays:
      # ions per type = -> to obtain the number of atoms per type
    - SYSTEM = name label
    - POSCAR = name label
    - Startparameter for this run:
        - Electronic Relaxation 1
        - Ionic relaxation
          # NSW = -> to obtain the number of iterations performed in this run
          # POTIM  = -> to obtain the time duration of each snapshot
          # POMASS = -> to obtain the mass of each atom type
          # ZVAL   = -> to obtain the number of valence electron per atom type
        - Mass of Ions in am
    - DOS related values:
        - Electronic relaxation 2 (details)
        - Intra band minimization:
    - Write flags
    - Dipole corrections
    - LDA+U
    - Exchange correlation treatment
    - Linear response parameters
    - Orbital magnetization related
+ A description of the molecular dinamics procedure
+ A recap of the atomic struture in the cell and of k-vectors in the
  reciprocal space.
  # energy-cutoff  :
  # volume of cell : 
  # direct lattice vectors                  reciprocal lattice vectors
  # dir_a_x     dir_a_y     dir_a_Z         rec_a_x     rec_a_y     rec_a_z
  # dir_a_x     dir_a_y     dir_a_Z         rec_a_x     rec_a_y     rec_a_z
  # dir_a_x     dir_a_y     dir_a_Z         rec_a_x     rec_a_y     rec_a_z
  #
  # length of vectors
  # norm_dir_a  norm_dir_b  norm_dir_z      norm_rec_a  norm_rec_b  norm_rec_z
  -> to obtain the lattice basis vectors
+ A log of the planewaves, chrage density and projector initialization

Finally at the end of the header, the simulation iteration process starts
(for the OUTCAR structure of this parte see UMDSnapshot_from_outcar.py).
"""


import numpy as np

from UMDAtom import UMDAtom
from UMDLattice import UMDLattice 
from UMDSimulation import UMDSimulation


def UMDSimulation_from_outcar(outcar, cyc):
    """
    Initialize a UMDSimulation object from a Vasp OUTCAR file.

    Parameters
    ----------
    outcar : input file
        The Vasp OUTCAR file.
    cyc : int
        The cycle number of the simulation.

    Returns
    -------
    simulation : UMDSimulation
        UMDSimulation object with the information about the Vasp run.

    """
    # Variable necessary for the UMDLattice and UMDSimulation initialization.
    lattice_name = ''
    atoms_name = []
    atoms_mass = []
    atoms_valence = []
    atoms_number = []
    basis = np.zeros((3, 3), dtype=float)

    steps = 0
    steptime = 0

    # With the following cycle, we scroll all the lines of the OUTCAR file
    # header till the beginnig of the iterative part of the OUTCAR file.
    # Everytime we find a section of the header containing useful information,
    # an inner loops is started on the section in order to initialize the
    # previously defined variables.
    line = outcar.readline()
    while line:
        if "POTCAR:" in line:
            # Once in a POTCAR section we scroll the lines till we find the
            # atomic symbol reported in the 'TITLE' line.
            while line:
                if "TITEL  =" in line:
                    atoms_name.append(line.strip().split()[-2])
                    break
                line = outcar.readline()

        elif "Dimension of arrays:" in line:
            # Once in the 'Dimension of arrays' group of parameters, we scroll
            # the lines till we find 'ion per type line' containing the number
            # of atoms per each type.
            while line:
                if "ions per type =" in line:
                    line = line.replace("ions per type", '').replace("=", '')
                    atoms_number = [int(at) for at in line.strip().split()]
                    break
                line = outcar.readline()
        elif "SYSTEM =" in line:
            lattice_name = line.strip().split()[-2]

        elif "Startparameter for this run:" in line:
            # Once in the 'Startparameter for this run' group of parameters,
            # we scroll the lines till we find the:
            # - 'NSW' to set the number of itrations in the simulation run
            # - 'POTIM' to set the time duration of each snapshot
            # - 'POMASS' to set the atomic mass per atom type
            # - 'ZVAL' to set the number of valence electrons per atom type
            while line:
                if 'NSW' in line:
                    steps = int(line.strip().split()[2])
                if 'POTIM' in line:
                    steptime = float(line.strip().split()[2])
                if 'POMASS' in line:
                    line = line.replace("POMASS", '').replace("=", '')
                    atoms_mass = [float(at) for at in line.strip().split()]
                if 'ZVAL' in line:
                    line = line.replace("ZVAL", '').replace("=", '')
                    atoms_valence = [float(at) for at in line.strip().split()]
                if "DOS related values" in line:
                    # It marks the beginnig of the new section of parameters.
                    break
                line = outcar.readline()

        elif ("direct lattice vectors" in line
              and "reciprocal lattice vectors" in line):
            # Once in the recap of the atomic structure of the unit cell, we
            # read the three following lines to obtain the three lattice
            # vectors in the direct space
            for i in range(3):
                basis[i] = outcar.readline().strip().split()[:3]

        elif "Iteration" in line:
            # ------------------- Iteration      1(   1)  -------------------
            # It is the beginning of the iterative part of the simulation and
            # it marks the end of the header part with simulation information.
            # At this point, the UMDSimulation can be built and returned.
            assert len(atoms_name) == len(atoms_mass)
            assert len(atoms_mass) == len(atoms_valence)
            assert len(atoms_valence) == len(atoms_number)
            atoms = {}
            for i in range(len(atoms_name)):
                atom = UMDAtom(name=atoms_name[i], mass=atoms_mass[i],
                               valence=atoms_valence[i])
                atoms[atom] = atoms_number[i]
            lattice = UMDLattice(lattice_name, basis, atoms)
            if not lattice.atoms == {}:
                simulation = UMDSimulation('', lattice, cyc, steps, steptime)
                return simulation
        line = outcar.readline()
