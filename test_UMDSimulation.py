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
    assert simulation.lattice == UMDLattice()
    assert simulation.cycle == -1
    assert simulation.steps == 0
    assert simulation.steptime == 0.0
    assert simulation.time == 0.0


def test_UMDLattice_init_assignement():
    """
    Test the __init__ function assignement operations with a non singular
    matrix of lattice vectors.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation('SimulationName', lattice, 2, 30000, 0.5, 15.0)
    assert simulation.name == 'SimulationName'
    assert simulation.lattice == lattice
    assert simulation.cycle == 2
    assert simulation.steps == 30000
    assert simulation.steptime == 0.5
    assert simulation.time == 15.0


test_UMDSimulation_init_default()
test_UMDLattice_init_assignement()


# %% UMDSimulation simtime function tests
def test_UMDSimulation_simtime_with_time():
    simulation = UMDSimulation('', cycle=2, steps=30000, steptime=0.5, time=10)
    assert simulation.simtime() == 10.0


def test_UMDSimulation_simtime_with_no_time():
    simulation = UMDSimulation('', cycle=2, steps=30000, steptime=0.5)
    assert simulation.simtime() == 15.0


test_UMDSimulation_simtime_with_time()
test_UMDSimulation_simtime_with_no_time()


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
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 2, 30000, 0.5, 3.)
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
    simulation1 = UMDSimulation('SimulationName1', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName2', lattice2, 2, 30000, 0.5, 3.)
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
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 2, 30000, 0.5, 3.)
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
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 1, 30000, 0.5, 3.)
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
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 2, 20000, 0.5, 3.)
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
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 2, 30000, 0.3, 3.)
    assert not simulation1 == simulation2


def test_UMDSimulation_eq_false_time():
    """
    Test the __eq__ function to compare two UMDSimulation objects representing
    two simulations with different snapshots time duration. The value returned
    must be False.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice1 = UMDLattice(basis=basis, atoms=atoms)
    lattice2 = UMDLattice(basis=basis, atoms=atoms)
    simulation1 = UMDSimulation('SimulationName', lattice1, 2, 30000, 0.5, 3.)
    simulation2 = UMDSimulation('SimulationName', lattice2, 2, 30000, 0.5, 1.)
    assert not simulation1 == simulation2


test_UMDSimulation_eq_true()
test_UMDSimulation_eq_false_name()
test_UMDSimulation_eq_false_lattice()
test_UMDSimulation_eq_false_cycle()
test_UMDSimulation_eq_false_snaps()
test_UMDSimulation_eq_false_snaptime()
test_UMDSimulation_eq_false_time()


# %% UMDSimulation __str__ function tests
def test_UMDSimulation_str():
    """
    Test the __str__ function to convert the UMDSimulation parameters into a
    descriptive and printable string object.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation('SimulationName', lattice, 2, 30000, 0.5)
    string = 'Simulation: SimulationName                \n'
    string += 'Total cycles =          2\n'
    string += 'Total steps  =      30000\n'
    string += 'Total time   =    15.0000 ps'
    assert str(simulation) == string


def test_UMDSimulation_str_legnth():
    """
    Test the __str__ function correct length of the string object returned.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation('SimulationName', lattice, 2, 30000, 0.5)
    stringlength = (12+30+1) + (15+10+1) + (15+10+1) + (15+10+3)
    assert len(str(simulation)) == stringlength


test_UMDSimulation_str()
test_UMDSimulation_str_legnth()
