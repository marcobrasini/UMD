# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:19:27 2022

@author: marco
"""
"""
To test UMDSimulation_from_OUTCAR we use two examples of OUTCARfile:
 - the OUTCAR_nomag, /tests/nomag5.70a1800T.outcar
 - the OUTCAR_mag,   /tests/mag5.70a1800T.outcar
 - the OUTCAR_magpU, /tests/magpU5.70a1800T.outcar

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


testOUTCAR_nomag = 'tests/nomag5.70a1800T.outcar'
testOUTCAR_mag = 'tests/mag5.70a1800T.outcar'
testOUTCAR_magpU = 'tests/magpU5.70a1800T.outcar'


# According to the header, we initialize the lattice structure and the
# simulation parameters used in the following tests as a reference to compare # the UMDSimulation_from_outcar results.
name = '2bccH2O+1Fe'
basis = np.array([[5.7, 0.0, 0.0],
                  [0.0, 5.7, 0.0],
                  [0.0, 0.0, 5.7]])
H = UMDAtom('H', mass=1.00, valence=1.0)
O = UMDAtom('O', mass=16.00, valence=6.0)
Fe = UMDAtom('Fe', mass=55.85, valence=8.0)
lattice = UMDLattice(name, basis, atoms={O: 15, H: 28, Fe: 1})
simulation_parameter = [(300, 0.5), (600, 0.5), (1000, 0.4)]


# %% UMDSimulation_from_outcar function tests for single OUTCAR files
def test_UMDSimulation_from_single_outcar_nomag():
    """
    Test UMDSimulation_from_outcar function when it reads many OUTCAR files,
    each one correspondent to a single simulation cycle with its own
    parameters (all in non magnetic configuration).
    For each cycle file, the UMDSimulation_from_outcar must return a
    UMDSimulation object equal to what described in the header.

    """
    for cyc in range(3):
        testOUTCAR = testOUTCAR_nomag + '.cyc'+str(cyc)
        steps, steptime = simulation_parameter[cyc]
        simulation = UMDSimulation('', cyc, steps, steptime, lattice)
        with open(testOUTCAR, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


def test_UMDSimulation_from_single_outcar_mag():
    """
    Test UMDSimulation_from_outcar function when it reads many OUTCAR files,
    each one correspondent to a single simulation cycle with its own
    parameters (all in magnetic configuration).
    For each cycle file, the UMDSimulation_from_outcar must return a
    UMDSimulation object equal to what described in the header.

    """
    for cyc in range(3):
        testOUTCAR = testOUTCAR_mag + '.cyc'+str(cyc)
        steps, steptime = simulation_parameter[cyc]
        simulation = UMDSimulation('', cyc, steps, steptime, lattice)
        with open(testOUTCAR, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


def test_UMDSimulation_from_single_outcar_magpU():
    """
    Test UMDSimulation_from_outcar function when it reads many OUTCAR files,
    each one correspondent to a single simulation cycle with its own
    parameters (all in magnetic configuration with +U potential correction). 
    For each cycle file, the UMDSimulation_from_outcar must return a
    UMDSimulation object equal to what described in the header.

    """
    for cyc in range(3):
        testOUTCAR = testOUTCAR_magpU + '.cyc'+str(cyc)
        steps, steptime = simulation_parameter[cyc]
        simulation = UMDSimulation('', cyc, steps, steptime, lattice)
        with open(testOUTCAR, 'r') as outcar:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            assert simulation == simulation_from_outcar


test_UMDSimulation_from_single_outcar_nomag()
test_UMDSimulation_from_single_outcar_mag()
test_UMDSimulation_from_single_outcar_magpU()


# %% UMDSimulation_from_outcar function tests for multiple concatenated
# OUTCAR files
def test_UMDSimulation_from_concatenated_outcar_nomag():
    """
    Test UMDSimulation_from_outcar function when it reads single OUTCAR file,
    containing many OUTCAR files concatenated. Each part of the whole OUTCAR
    corresponds to a particular simulation cycle with its own parameters
    (all in non magnetic configuration).
    Scrolling all the OUTCAR file, the UMDSimulation_from_outcar must return
    as many UMDSimulation object as the number of OUTCAR file concatenated,
    and each one must be identical to what described in the header.

    """
    cyc = 0
    with open(testOUTCAR_nomag, 'r') as outcar:
        while True:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            if simulation_from_outcar is None:
                break
            else:
                steps, steptime = simulation_parameter[cyc]
                simulation = UMDSimulation('', cyc, steps, steptime, lattice)
                assert simulation == simulation_from_outcar
                cyc += 1
        assert cyc == 3


def test_UMDSimulation_from_concatenated_outcar_mag():
    """
    Test UMDSimulation_from_outcar function when it reads single OUTCAR file,
    containing many OUTCAR files concatenated. Each part of the whole OUTCAR
    corresponds to a particular simulation cycle with its own parameters
    (all in magnetic configuration).
    Scrolling all the OUTCAR file, the UMDSimulation_from_outcar must return
    as many UMDSimulation object as the number of OUTCAR file concatenated,
    and each one must be identical to what described in the header.

    """
    cyc = 0
    with open(testOUTCAR_mag, 'r') as outcar:
        while True:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            if simulation_from_outcar is None:
                break
            else:
                steps, steptime = simulation_parameter[cyc]
                simulation = UMDSimulation('', cyc, steps, steptime, lattice)
                assert simulation == simulation_from_outcar
                cyc += 1


def test_UMDSimulation_from_concatenated_outcar_magpU():
    """
    Test UMDSimulation_from_outcar function when it reads single OUTCAR file,
    containing many OUTCAR files concatenated. Each part of the whole OUTCAR
    corresponds to a particular simulation cycle with its own parameters
    (all in magnetic configuration with +U potential correction).
    Scrolling all the OUTCAR file, the UMDSimulation_from_outcar must return
    as many UMDSimulation object as the number of OUTCAR file concatenated,
    and each one must be identical to what described in the header.

    """
    cyc = 0
    with open(testOUTCAR_magpU, 'r') as outcar:
        while True:
            simulation_from_outcar = UMDSimulation_from_outcar(outcar, cyc)
            if simulation_from_outcar is None:
                break
            else:
                steps, steptime = simulation_parameter[cyc]
                simulation = UMDSimulation('', cyc, steps, steptime, lattice)
                assert simulation == simulation_from_outcar
                cyc += 1


test_UMDSimulation_from_concatenated_outcar_nomag()
test_UMDSimulation_from_concatenated_outcar_mag()
test_UMDSimulation_from_concatenated_outcar_magpU()
