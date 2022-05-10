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
    """
    Test the __str__ function to convert the UMDSnapDynamics data into a
    descriptive and printable string object.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={O: 2})
    position = np.array([[0.23, 0.17, -1.43], [-0.76, 1.02, -0.71]])
    velocity = np.array([[0.42, -1.34, -0.22], [0.10, 0.49, 0.95]])
    force = np.array([[-1.58, 0.82, 0.03], [0.22, -0.49, -1.73]])
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position,
                                   velocity=velocity, force=force)
    string = "Positions                           "
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


# %% UMDSnapDynamics displacement function tests
def test_UMDSnapDynamics_get_displacement_null():
    """
    Test the get_displacement function when the atoms displacement is zero.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={O: 2})
    position = np.array([[0.1, 0.1, 0.1],
                         [0.5, 0.5, 0.5]])
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    position0 = np.copy(position)
    displacement = snapdynamics.get_displacement(position0)
    assert np.array_equal(displacement, np.zeros((2, 3)))


def test_UMDSnapDynamics_get_displacement_small():
    """
    Test the get_displacement function when the atoms displacement is small.
    A small displacement is a displacement whose reduced components are all
    smaller than the half of the lattice basis vectors. In this case, no
    periodic correction to the displacement is necessary.

    """
    basis = np.array([[1.0, 0.0, 1.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 2.0]])
    lattice = UMDLattice(basis=basis, atoms={O: 2})
    position0 = np.array([[0.1, 0.1, 0.1],
                         [0.5, 0.5, 0.5]])
    small_displacement = np.array([[-0.4, 0.1, 0.5],
                                   [-0.2, 0.1, 0.5]])
    real_displacement = small_displacement @ basis
    position = position0 + real_displacement
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(position0)
    assert np.allclose(displacement, real_displacement)


def test_UMDSnapDynamics_get_displacement_large():
    """
    Test the get_displacement function when the atoms displacement is large.
    A large displacement is a displacement whose some components are larger
    than the half of the lattice basis vectors. In this case, a periodic
    correction to the displacement is necessary.

    """
    basis = np.array([[1.0, 0.0, 1.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 2.0]])
    lattice = UMDLattice(basis=basis, atoms={O: 2})
    position0 = np.array([[0.1, 0.1, 0.1],
                         [0.5, 0.5, 0.5]])
    large_displacement = np.array([[-0.7, 0.1, 0.5],
                                   [-0.2, 0.9, 0.5]])
    real_displacement = large_displacement @ basis
    position = position0 + real_displacement
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(position0)
    large_displacement = np.array([[0.3, 0.1, 0.5],
                                   [-0.2, -0.1, 0.5]])
    real_displacement = large_displacement @ basis
    assert np.allclose(displacement, real_displacement)


test_UMDSnapDynamics_get_displacement_null()
test_UMDSnapDynamics_get_displacement_small()
test_UMDSnapDynamics_get_displacement_large()
