# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:15:55 2022

@author: marco
"""


from UMDSnapDynamics import UMDSnapDynamics

import numpy as np
from UMDAtom import UMDAtom
from UMDLattice import UMDLattice

O = UMDAtom('O')
H = UMDAtom('H')


# %% UMDSnapDynamics __init__ function tests
def test_UMDSnapDynamics_init_default():
    """
    Test the __init__ function defualt constructor.

    """
    snapdynamics = UMDSnapDynamics()
    assert snapdynamics.snaptime == 0.0
    assert snapdynamics.lattice == UMDLattice()
    assert snapdynamics.position == []
    assert snapdynamics.displacement == []
    assert snapdynamics.velocity == []
    assert snapdynamics.force == []


def test_UMDSnapDynamics_init_assignement():
    """
    Test the __init__ function assignement operations.

    """
    snaptime = 0.5
    lattice = UMDLattice('', np.identity(3), {O: 2, H: 4})
    position = np.random.uniform(size=(6, 3))
    displacement = np.random.uniform(size=(6, 3))
    velocity = np.random.uniform(size=(6, 3))
    force = np.random.uniform(size=(6, 3))
    snapdynamics = UMDSnapDynamics(snaptime, lattice, position,
                                   displacement, velocity, force)
    assert snapdynamics.snaptime == snaptime
    assert snapdynamics.lattice == lattice
    assert np.array_equal(snapdynamics.position, position)
    assert np.array_equal(snapdynamics.displacement, displacement)
    assert np.array_equal(snapdynamics.velocity, velocity)
    assert np.array_equal(snapdynamics.force, force)


test_UMDSnapDynamics_init_default()
test_UMDSnapDynamics_init_assignement()


# %% UMDSnapDynamics __str__ function tests
def test_UMDSnapDynamics_str():
    lattice = UMDLattice(atoms={O: 2})
    position = np.array([[0.23, 0.17, -1.43], [-0.76, 1.02, -0.71]])
    velocity = np.array([[0.42, -1.34, -0.22], [0.10, 0.49, 0.95]])
    force = np.array([[-1.58, 0.82, 0.03], [0.22, -0.49, -1.73]])
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position,
                                   velocity=velocity, force=force)
    string  = "Positions                           "
    string += "Velocities                          "
    string += "Forces                              \n"
    string += "    0.230000    0.170000   -1.430000"
    string += "    0.420000   -1.340000   -0.220000"
    string += "   -1.580000    0.820000    0.030000\n"
    string += "   -0.760000    1.020000   -0.710000"
    string += "    0.100000    0.490000    0.950000"
    string += "    0.220000   -0.490000   -1.730000"
    assert str(snapdynamics) == string


test_UMDSnapDynamics_str()
