# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:15:55 2022

@author: marco
"""


from UMDSnapDynamics import UMDSnapDynamics

import hypothesis as hp
import hypothesis.strategies as st

import numpy as np
import numpy.random as rnd
from UMDAtom import UMDAtom
from UMDLattice import UMDLattice

rnd.seed(62815741)
at = UMDAtom()


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


@hp.given(snaptime=st.floats(allow_infinity=False, allow_nan=False),
          natoms=st.integers(min_value=0, max_value=(1000)))
def test_UMDSnapDynamics_init_assignement(snaptime, natoms):
    """
    Test the __init__ function assignement operations.

    """
    snaptime = snaptime
    lattice = UMDLattice('', np.identity(3), {at: natoms})
    position = rnd.uniform(size=(natoms, 3))
    displacement = rnd.uniform(size=(natoms, 3))
    velocity = rnd.uniform(size=(natoms, 3))
    force = rnd.uniform(size=(natoms, 3))
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
    lattice = UMDLattice(basis=np.identity(3), atoms={at: 2})
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


# %% UMDSnapDynamics displacement function tests
@hp.given(N=st.integers(1, 500))
def test_UMDSnapDynamics_get_displacement_cubic_null(N):
    """
    Test the get_displacement function when the atoms displacement is zero.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={at: N})
    position0 = rnd.uniform(size=(N, 3))
    position = np.copy(position0)
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(position0)
    assert np.array_equal(displacement, np.zeros((N, 3)))


@hp.given(N=st.integers(1, 500))
def test_UMDSnapDynamics_get_displacement_cubic_small(N):
    """
    Test the get_displacement function when the atoms displacement is small.
    A small displacement is a displacement whose reduced components are all
    smaller than the half of the lattice basis vectors. In this case, no
    periodic correction to the displacement is necessary.

    """
    basis = np.identity(3)
    lattice = UMDLattice(basis=basis, atoms={at: N})
    pos0 = rnd.uniform(size=(N, 3))
    disp = rnd.uniform(-0.5, 0.5, size=(N, 3))

    position = pos0 + (disp @ basis)
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(pos0)
    assert np.allclose(displacement, disp @ basis)


@hp.given(N=st.integers(1, 500))
def test_UMDSnapDynamics_get_displacement_cubic_large_positive(N):
    """
    Test the get_displacement function when the atoms displacement is large.
    A large displacement is a displacement whose some components are larger
    than the half of the lattice basis vectors. In this case, a periodic
    correction to the displacement is necessary.

    """
    basis = np.identity(3)
    lattice = UMDLattice(basis=basis, atoms={at: N})
    pos0 = rnd.uniform(size=(N, 3))
    disp = rnd.uniform(0.5, 1, size=(N, 3))

    position = pos0 + (disp @ basis)
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(pos0)
    assert np.allclose(displacement, (disp - 1) @ basis)


@hp.given(N=st.integers(1, 500))
def test_UMDSnapDynamics_get_displacement_cubic_large_negative(N):
    """
    Test the get_displacement function when the atoms displacement is large.
    A large displacement is a displacement whose some components are larger
    than the half of the lattice basis vectors. In this case, a periodic
    correction to the displacement is necessary.

    """
    basis = np.identity(3)
    lattice = UMDLattice(basis=basis, atoms={at: N})
    pos0 = rnd.uniform(size=(N, 3))
    disp = rnd.uniform(-1, -0.5, size=(N, 3))

    position = pos0 + (disp @ basis)
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(pos0)
    assert np.allclose(displacement, (disp + 1) @ basis)


@hp.given(N=st.integers(1, 500))
def test_UMDSnapDynamics_get_displacement_cubic_size(N):
    """
    Test the get_displacement function results. Independently on the position
    the atoms position in the unit cell, the displacement returned must be
    smaller then the half unit cell.

    """
    basis = np.identity(3)
    lattice = UMDLattice(basis=basis, atoms={at: N})
    pos0 = rnd.uniform(size=(N, 3))
    pos1 = rnd.uniform(size=(N, 3))

    snapdynamics = UMDSnapDynamics(lattice=lattice, position=pos1)
    displacement = snapdynamics.get_displacement(pos0)
    max_displacement = np.linalg.norm(np.array([0.5, 0.5, 0.5]) @ basis)
    assert (np.linalg.norm(displacement, axis=1) < max_displacement).all()


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
    lattice = UMDLattice(basis=basis, atoms={at: 2})
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
    lattice = UMDLattice(basis=basis, atoms={at: 2})
    position0 = np.array([[0.1, 0.1, 0.1],
                         [0.5, 0.5, 0.5]])
    large_displacement = np.array([[0.7, 0.1, 0.5],
                                   [0.2, 0.9, 0.5]])
    real_displacement = large_displacement @ basis
    position = position0 + real_displacement
    snapdynamics = UMDSnapDynamics(lattice=lattice, position=position)
    displacement = snapdynamics.get_displacement(position0)
    large_displacement = np.array([[-0.3, 0.1, 0.5],
                                   [0.2, -0.1, 0.5]])
    real_displacement = large_displacement @ basis
    assert np.allclose(displacement, real_displacement)


test_UMDSnapDynamics_get_displacement_cubic_null()
test_UMDSnapDynamics_get_displacement_cubic_small()
test_UMDSnapDynamics_get_displacement_cubic_large_positive()
test_UMDSnapDynamics_get_displacement_cubic_large_negative()
test_UMDSnapDynamics_get_displacement_cubic_size()
test_UMDSnapDynamics_get_displacement_small()
test_UMDSnapDynamics_get_displacement_large()
