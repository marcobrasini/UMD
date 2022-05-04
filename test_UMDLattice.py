# -*- coding: utf-8 -*-
"""
Created on Wed May  4 10:23:02 2022

@author: marco
"""

from UMDLattice import UMDLattice

import numpy as np


# %% UMDLattice __init__ function tests
def test_UMDLattice_init_assignement():
    """
    Test the __init__ function assignement operations with a non singular
    matrix of lattice vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    assert Lattice.name == name
    assert Lattice.atoms == atoms
    assert np.array_equal(Lattice.dirBasis, basis)
    assert np.array_equal(Lattice.invBasis, np.linalg.inv(basis))


def test_UMDLattice_init_basis_inversion():
    """
    Test the __init__ function matrix inversion operation for a non singular
    matrix of lattice vectors. The matrix product ('dirBasis' x 'invBasis') 
    must be equal (or close) to the identical matrix.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    assert np.allclose(Lattice.dirBasis@Lattice.invBasis, np.identity(3))


def test_UMDLattice_init_basis_inversion_error():
    """
    Test the __init__ function matrix inversion operation for a singular 
    matrix of lattice vectors. The invBasis attribute returned must be a
    matrix of np.nan.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 0, 0]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    assert np.isnan(Lattice.invBasis).all()


test_UMDLattice_init_assignement()
test_UMDLattice_init_basis_inversion()
test_UMDLattice_init_basis_inversion_error()


# %% UMDLattice natoms function tests
def test_UMDLattice_natoms():
    """
    Test the natoms function. The number of atoms returned must be equal to
    the sum of the number of atoms per each element in the 'atoms' dictionary.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    assert Lattice.natoms() == 44


test_UMDLattice_natoms()


# %% UMDLattice reduced function tests
def test_UMDLattice_reduced_basis():
    """
    Test the reduced function to convert a vector in cartesian coordiates to
    reduced coordinates refered to the lattice vector system.
    To test it we assert that the cartesian basis vectors in reduced
    coordinates must be equal to the canonical basis vectors .

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    reduced_a = Lattice.reduced(basis[0])
    reduced_b = Lattice.reduced(basis[1])
    reduced_c = Lattice.reduced(basis[2])
    assert np.allclose(reduced_a, np.array([1, 0, 0]))
    assert np.allclose(reduced_b, np.array([0, 1, 0]))
    assert np.allclose(reduced_c, np.array([0, 0, 1]))


test_UMDLattice_reduced_basis()


# %% UMDLattice cartesian function tests
def test_UMDLattice_cartesian_basis():
    """
    Test the cartesian function to convert a vector in reduced coordiates 
    refered to the lattice vector system to cartesian coordinates.
    To test it, we assert that the canonical basis vectors in the reduced
    coordinates systemmust be equal to the cartesian basis vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    cartesian_a = Lattice.cartesian(np.array([1, 0, 0]))
    cartesian_b = Lattice.cartesian(np.array([0, 1, 0]))
    cartesian_c = Lattice.cartesian(np.array([0, 0, 1]))
    assert np.allclose(cartesian_a, basis[0])
    assert np.allclose(cartesian_b, basis[1])
    assert np.allclose(cartesian_c, basis[2])


test_UMDLattice_cartesian_basis()
