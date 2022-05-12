# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:30:45 2022

@author: marco
"""
"""
To test UMDSnapshot_from_outcar we use three examples of OUTCARfile:
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


from UMDSnapshot_from_outcar import UMDSnapshot_from_outcar

import numpy as np

from UMDAtom import UMDAtom
from UMDLattice import UMDLattice
from UMDSimulation import UMDSimulation
from UMDSnapshot import UMDSnapshot


testOUTCAR_nomag = 'tests/nomag5.70a1800T.outcar'
testOUTCAR_mag = 'tests/mag5.70a1800T.outcar'
testOUTCAR_magpU = 'tests/magpU5.70a1800T.outcar'

# %% The lattice structure values
# According to the header, we initialize the lattice structure and the
# simulation parameters, necessary to reset the UMDSnapshot attributes and
# make the load_Snapshot function work properly.
name = '2bccH2O+1Fe'
basis = np.array([[5.7, 0.0, 0.0],
                  [0.0, 5.7, 0.0],
                  [0.0, 0.0, 5.7]])
H = UMDAtom('H', mass=1.00, valence=1.0)
O = UMDAtom('O', mass=16.00, valence=6.0)
Fe = UMDAtom('Fe', mass=55.85, valence=8.0)
lattice = UMDLattice(name, basis, atoms={O: 15, H: 28, Fe: 1})
simulation_parameter = [(300, 0.5), (600, 0.5), (1000, 0.4)]


# %% UMDSnapshot_from_outcar function tests
def test_UMDSnapshot_from_outcar_nSnapshot_single_nomag():
    """
    Test the number of snapshot catched by UMDSnapshot_from_outcar when it
    reads many OUTCAR files, each one correspondent to a single simulation
    cycle with its own parameters (all in non magnetic configuration).
    For each cycle file, the UMDSnapshot_from_outcar must read a number of
    snapshot object equal to what described in the header.

    """
    for cyc in range(3):
        UMDSnapshot.reset(simulation_parameter[cyc][1], lattice)
        testOUTCAR = testOUTCAR_nomag + '.cyc'+str(cyc)
        with open(testOUTCAR, 'r') as outcar:
            nsnapshot = 0
            while True:
                snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
                if snapshot is None:
                    break
                nsnapshot += 1
            assert nsnapshot == simulation_parameter[cyc][0]


def test_UMDSnapshot_from_outcar_nSnapshot_single_mag():
    """
    Test the number of snapshot catched by UMDSnapshot_from_outcar when it
    reads many OUTCAR files, each one correspondent to a single simulation
    cycle with its own parameters (all in magnetic configuration).
    For each cycle file, the UMDSnapshot_from_outcar must read a number of
    snapshot object equal to what described in the header.

    """
    for cyc in range(3):
        UMDSnapshot.reset(simulation_parameter[cyc][1], lattice)
        testOUTCAR = testOUTCAR_mag + '.cyc'+str(cyc)
        with open(testOUTCAR, 'r') as outcar:
            nsnapshot = 0
            while True:
                snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
                if snapshot is None:
                    break
                nsnapshot += 1
            assert nsnapshot == simulation_parameter[cyc][0]


def test_UMDSnapshot_from_outcar_nSnapshot_single_magpU():
    """
    Test the number of snapshot catched by UMDSnapshot_from_outcar when it
    reads many OUTCAR files, each one correspondent to a single simulation
    cycle with its own parameters (all magnetic configuration with +U).
    For each cycle file, the UMDSnapshot_from_outcar must read a number of
    snapshot object equal to what described in the header.

    """
    for cyc in range(3):
        UMDSnapshot.reset(simulation_parameter[cyc][1], lattice)
        testOUTCAR = testOUTCAR_magpU + '.cyc'+str(cyc)
        with open(testOUTCAR, 'r') as outcar:
            nsnapshot = 0
            while True:
                snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
                if snapshot is None:
                    break
                nsnapshot += 1
            assert nsnapshot == simulation_parameter[cyc][0]


def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_nomag():
    """
    Test Test the number of snapshot catched by UMDSnapshot_from_outcar when
    it reads single OUTCAR file, containing many OUTCAR files concatenated.
    Each part of the whole OUTCAR corresponds to a particular simulation cycle
    with its own parameters (all in non magnetic configuration).
    Scrolling all the OUTCAR file, the number of snapshots catched by
    UMDSimulation_from_outcar function must equal to what described in the
    header.

    """
    nsnapshot = 0
    UMDSnapshot.reset(lattice)
    with open(testOUTCAR_nomag, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
            if snapshot is None:
                break
            nsnapshot += 1
        assert nsnapshot == 1900


def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_mag():
    """
    Test Test the number of snapshot catched by UMDSnapshot_from_outcar when
    it reads single OUTCAR file, containing many OUTCAR files concatenated.
    Each part of the whole OUTCAR corresponds to a particular simulation cycle
    with its own parameters (all in magnetic configuration).
    Scrolling all the OUTCAR file, the number of snapshots catched by
    UMDSimulation_from_outcar function must equal to what described in the
    header.

    """
    nsnapshot = 0
    UMDSnapshot.reset(lattice)
    with open(testOUTCAR_nomag, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
            if snapshot is None:
                break
            nsnapshot += 1
        assert nsnapshot == 1900


def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_magpU():
    """
    Test Test the number of snapshot catched by UMDSnapshot_from_outcar when
    it reads single OUTCAR file, containing many OUTCAR files concatenated.
    Each part of the whole OUTCAR corresponds to a particular simulation cycle
    with its own parameters (all in magnetic configuration with +U correction).
    Scrolling all the OUTCAR file, the number of snapshots catched by
    UMDSimulation_from_outcar function must equal to what described in the
    header.

    """
    nsnapshot = 0
    UMDSnapshot.reset(lattice)
    with open(testOUTCAR_mag, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, nsnapshot)
            if snapshot is None:
                break
            nsnapshot += 1
        assert nsnapshot == 1900


test_UMDSnapshot_from_outcar_nSnapshot_single_nomag()
test_UMDSnapshot_from_outcar_nSnapshot_single_mag()
test_UMDSnapshot_from_outcar_nSnapshot_single_magpU()
test_UMDSnapshot_from_outcar_nSnapshot_concatenated_nomag()
test_UMDSnapshot_from_outcar_nSnapshot_concatenated_mag()
test_UMDSnapshot_from_outcar_nSnapshot_concatenated_magpU()
