# -*- coding: utf-8 -*-
"""
Created on Wed May  4 10:23:02 2022

@author: marco
"""

from UMDLattice import UMDLattice

import numpy as np


# %% UMDLattice __init__ function tests
def test_UMDLattice_init_default():
    """
    Test the __init__ function defualt constructor.

    """
    Lattice = UMDLattice()
    assert Lattice.name == ''
    assert Lattice.atoms == {}
    assert np.array_equal(Lattice.dirBasis, np.zeros((3, 3)))
    assert np.array_equal(Lattice.invBasis, np.full((3, 3), np.nan), True)


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


test_UMDLattice_init_default()
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
    To test it, we assert that the each basis vector in cartesian coordinates
    must be transformed into a canonical basis vector.

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


def test_UMDLattice_reduced_allbasis():
    """
    Test the reduced function to convert a set of vectors in cartesian
    coordiates to reduced coordinates refered to the lattice vector system.
    To test it, we assert that the matrix made of all the three basis vectors
    in cartesian coordinates must be transformed into a matrix made of all
    the canonical basis vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    reduced = Lattice.reduced(basis)
    assert np.allclose(reduced, np.identity(3))


def test_UMDLattice_reduced_halfbasis():
    """
    Test the reduced function to convert a set of vectors in cartesian
    coordiates to reduced coordinates refered to the lattice vector system.
    To test it, we assert that the matrix made of only the first two basis
    vectors in cartesian coordinates must be transformed into a matrix made of
    only the first two canonical basis vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    reduced = Lattice.reduced(basis[:2])
    assert np.allclose(reduced, np.identity(3)[:2])


test_UMDLattice_reduced_basis()
test_UMDLattice_reduced_allbasis()
test_UMDLattice_reduced_halfbasis()


# %% UMDLattice cartesian function tests
def test_UMDLattice_cartesian_basis():
    """
    Test the cartesian function to convert a vector in reduced coordiates
    refered to the lattice vector system to cartesian coordinates.
    To test it, we assert that each basis vector in the reduced coordinates,
    equal to a canonical basis vector, must be transformed into the original
    cartesian basis vector.

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


def test_UMDLattice_cartesian_allbasis():
    """
    Test the cartesian function to convert a set of vectors in reduced refered
    to the lattice vector system coordiates to cartesian coordinates.
    To test it, we assert that the matrix made of all basis vectors in the
    reduced coordinates, equal to the identity matrix, must be transformed
    into a matrix made of all the original basis vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    cartesian = Lattice.cartesian(np.identity(3))
    assert np.allclose(cartesian, basis)


def test_UMDLattice_cartesian_halfbasis():
    """
    Test the cartesian function to convert a set of vectors in reduced refered
    to the lattice vector system coordiates to cartesian coordinates.
    To test it, we assert that the matrix made of only the first two basis
    vectors in the reduced coordinates, equal to the first to canonical basis
    vectors, must be transformed into a matrix made of only the first two
    original basis vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 15, 'Y': 28, 'Z': 1}
    Lattice = UMDLattice(name, basis, atoms)
    cartesian = Lattice.cartesian(np.identity(3)[:2])
    assert np.allclose(cartesian, basis[:2])


test_UMDLattice_cartesian_basis()
test_UMDLattice_cartesian_allbasis()
test_UMDLattice_cartesian_halfbasis()
