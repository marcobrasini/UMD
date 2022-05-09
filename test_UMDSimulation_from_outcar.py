# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:19:27 2022

@author: marco
"""
"""
To test UMDSimulation_from_OUTCAR we use two examples of OUTCARfile:
 - the OUTCAR_nomag, 
 - the OUTCAR_mag,
 - the OUTCAR_magpU, 

Each simulation has the same structure:
 + it is run on a 2x2x2 supercelll of a bcc structure with lattice parameter
   of 5.70 ang. The matrix of basis vectors is:    
       5.70     0.00     0.00
       0.00     5.70     0.00
       0.00     0.00     5.70
   and the cell contains the following elements:
     - O: 15 atoms, 
     - H: 28 atoms,
     - Fe: 1 atom.
 + the simulation is divided in three cycles:
     - cycle 0:  300 steps and 0.5 snap duration
     - cycle 1:  600 steps and 0.5 snap duration
     - cycle 2: 1000 steps and 0.4 snap duration
"""

from UMDSimulation_from_outcar import UMDSimulation_from_outcar

import numpy as np

from UMDAtom import UMDAtom
from UMDLattice import UMDLattice
from UMDSimulation import UMDSimulation


# According to the header, we initialize the reference UMDLattice object ...
name = '2bccH2O+1Fe'
basis = np.array([[5.7, 0.0, 0.0],
                  [0.0, 5.7, 0.0],
                  [0.0, 0.0, 5.7]])
H = UMDAtom('H', mass=1.00, valence=1.0)
O = UMDAtom('O', mass=16.00, valence=6.0)
Fe = UMDAtom('Fe', mass=55.85, valence=8.0)
lattice = UMDLattice(name, basis, atoms={O: 15, H: 28, Fe: 1})

# ... and the simulation cycle parameters 
snaps = [300, 600, 1000]
snaptime = [0.5, 0.5, 0.4]


def test_UMDSimulation_from_single_outcar_nomag():
    for cyc in range(3):
        testOUTCAR_nomag = 'tests/nomag5.70a1800T.outcar'+'.cyc'+str(cyc)
        simulation = UMDSimulation(cyc, snaps[cyc], snaptime[cyc], lattice)
        with open(testOUTCAR_nomag, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


def test_UMDSimulation_from_single_outcar_mag():
    for cyc in range(3):
        testOUTCAR_nomag = 'tests/mag5.70a1800T.outcar'+'.cyc'+str(cyc)
        simulation = UMDSimulation(cyc, snaps[cyc], snaptime[cyc], lattice)
        with open(testOUTCAR_nomag, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


def test_UMDSimulation_from_single_outcar_magpU():
    for cyc in range(3):
        testOUTCAR_nomag = 'tests/magpU5.70a1800T.outcar'+'.cyc'+str(cyc)
        simulation = UMDSimulation(cyc, snaps[cyc], snaptime[cyc], lattice)
        with open(testOUTCAR_nomag, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


test_UMDSimulation_from_single_outcar_nomag()
test_UMDSimulation_from_single_outcar_mag()
test_UMDSimulation_from_single_outcar_magpU()
