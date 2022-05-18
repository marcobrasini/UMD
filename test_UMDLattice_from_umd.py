# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:38:52 2022

@author: marco
"""

from UMDSimulation_from_umd import UMDLattice_from_umd

import pytest
import numpy as np
from UMDAtom import UMDAtom


UMDfile_mag = 'tests/mag5.70a1800T.umd'

O = UMDAtom('O')
H = UMDAtom('H')
Fe = UMDAtom('Fe')


# %% UMDLattice_from_umd function tests
def test_UMDLattice_from_umd():
    """
    Test the UMDLattice_from_umd function initializing a UMDLattice object
    from an umd file.

    """
    with open(UMDfile_mag, 'r') as umd:
        lattice = UMDLattice_from_umd(umd)
        assert lattice.name == '3bccH2O+1Fe'
        assert lattice.atoms == {O: 15, H: 28, Fe: 1}
        assert np.array_equal(lattice.dirBasis, 5.70*np.identity(3))


def test_UMDLattice_from_umd_None():
    """
    Test the UMDLattice_from_umd function initializing no UMDLattice object
    from an umd file without any UMDLattice.

    """
    with open('tests/test_file_empty.umd', 'r') as umd:
        lattice = UMDLattice_from_umd(umd)
        assert lattice is None


test_UMDLattice_from_umd()
test_UMDLattice_from_umd_None()
