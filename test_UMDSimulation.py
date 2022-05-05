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
    assert simulation.Cycle == -1
    assert simulation.Snaps == 0
    assert simulation.snapTime == 0.
    assert simulation.Lattice == UMDLattice()


def test_UMDLattice_init_assignement():
    """
    Test the __init__ function assignement operations with a non singular
    matrix of lattice vectors.

    """
    basis = np.identity(3)
    atoms = {'X': 2, 'Y': 4}
    lattice = UMDLattice(basis=basis, atoms=atoms)
    simulation = UMDSimulation(2, 10000, 0.5, lattice)
    assert simulation.Cycle == 2
    assert simulation.Snaps == 10000
    assert simulation.snapTime == 0.5
    assert simulation.Lattice == lattice


test_UMDSimulation_init_default()
test_UMDLattice_init_assignement()

