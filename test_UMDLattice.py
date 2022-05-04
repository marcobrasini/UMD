# -*- coding: utf-8 -*-
"""
Created on Wed May  4 10:23:02 2022

@author: marco
"""

from UMDLattice import UMDLattice

import numpy as np


def test_UMDLattice_init_assignement():
    """
    Test the __init__ function assignement operations with a non singular
    matrix of lattice vectors.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 10, 'Y': 2}
    Lattice = UMDLattice(name, basis, atoms)
    assert Lattice.name == name
    assert Lattice.atoms == atoms
    assert np.array_equal(Lattice.dirBasis, basis)
    assert np.array_equal(Lattice.invBasis, np.linalg.inv(basis))


def test_UMDLattice_init_basis_inversion():
    """
    Test the __init__ function matrix inversion operation for a non singular
    matrix of lattice vectors. The matrix product between dirBasis and invBasis
    must be equal (or close) to the identical matrix.

    """
    name = 'LatticeName'
    basis = np.array([[2, 1, -3],
                      [-1, 0, 0],
                      [-4, 2, 1]])
    atoms = {'X': 10, 'Y': 2}
    Lattice = UMDLattice(name, basis, atoms)
    assert np.allclose(Lattice.dirBasis@Lattice.invBasis, np.identity(3))


test_UMDLattice_init_assignement()
test_UMDLattice_init_basis_inversion()
