# -*- coding: utf-8 -*-
"""
Created on Thu May  5 16:13:26 2022

@author: marco
"""

from UMDSimulation import UMDSimulation
from UMDLattice import UMDLattice

import numpy as np


# %% UMDSimulation __init__ function tests
def test_UMDSimulation_init_default():
    """
    Test the __init__ function defualt constructor.

    """
    simulation = UMDSimulation()
    assert simulation.name == ''
    assert simulation.Cycle == -1
    assert simulation.Snaps == 0
    assert simulation.snapTime == 0.
    assert simulation.Lattice == UMDLattice()


def test_UMDLattice_init_assignement():
    """
    Test the __init__ function assignement operations with a non singular
    matrix of lattice vectors.

    """
    name = 'magx.xxaYYYYT'
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation(name=name, cycle=2, snaps=30000, snaptime=0.5,        
                               lattice=lattice)
    assert simulation.name =='magx.xxaYYYYT'
    assert simulation.Cycle == 2
    assert simulation.Snaps == 30000
    assert simulation.snapTime == 0.5
    assert simulation.Lattice == lattice


test_UMDSimulation_init_default()
test_UMDLattice_init_assignement()


# %% UMDSimulation time function tests
def test_UMDSimulation_time():
    simulation = UMDSimulation('', 2, 30000, 0.5)
    assert simulation.time() == 15.


test_UMDSimulation_time()


# %% UMDSimulation __eq__ function tests
def test_UMDSimulation_eq_true():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two identical simulations. The value returned must be True.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice2)
    assert simulation1 == simulation2


def test_UMDSimulation_eq_false_name():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different name. The value returned must be False.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName1', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName2', 1, 30000, 0.5, lattice2)
    assert not simulation1 == simulation2


def test_UMDSimulation_eq_false_cycle():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different cycle number. The value returned must be
    False.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName', 1, 30000, 0.5, lattice2)
    assert not simulation1 == simulation2


def test_UMDSimulation_eq_false_snaps():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different number of snapshots. The value returned
    must be False.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName', 2, 20000, 0.5, lattice2)
    assert not simulation1 == simulation2


def test_UMDSimulation_eq_false_snaptime():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different snapshots time duration. The value returned
    must be False.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName', 2, 30000, 0.4, lattice2)
    assert not simulation1 == simulation2


def test_UMDSimulation_eq_false_lattice():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different lattices. The value returned must be False.

    """
    basis = np.identity(3)
    atoms1 = {'X': 2, 'Y': 4}
    atoms2 = {'X': 2}
    lattice1 = UMDLattice(basis=basis, atoms=atoms1)
    lattice2 = UMDLattice(basis=basis, atoms=atoms2)
    simulation1 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice1)
    simulation2 = UMDSimulation('SimulationName', 2, 30000, 0.5, lattice2)
    assert not simulation1 == simulation2


test_UMDSimulation_eq_true()
test_UMDSimulation_eq_false_name()
test_UMDSimulation_eq_false_cycle()
test_UMDSimulation_eq_false_snaps()
test_UMDSimulation_eq_false_snaptime()
test_UMDSimulation_eq_false_lattice()


# %% UMDSimulation __str__ function tests
def test_UMDSimulation_str():
    """
    Test the __str__ function to convert the UMDSimulation parameters into a
    descriptive and printable string object.

    """
    name = 'magx.xxaYYYYT'
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation(name=name, cycle=2, snaps=30000, snaptime=0.5,        
                               lattice=lattice)
    string  = 'Simulation: magx.xxaYYYYT\n'
    string += 'Total cycles = 2\n'
    string += 'Total steps = 30000\n'
    string += 'Total time = 15.0 ps'
    assert str(simulation) == string


test_UMDSimulation_str()

