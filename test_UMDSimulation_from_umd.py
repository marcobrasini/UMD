# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:54:02 2022

@author: marco
"""

from UMDSimulation_from_umd import UMDSimulation_from_umd

import pytest
import numpy as np
from UMDAtom import UMDAtom
from UMDLattice import UMDLattice


UMDfile_mag = 'tests/mag5.70a1800T.umd'

O = UMDAtom('O')
H = UMDAtom('H')
Fe = UMDAtom('Fe')


# %% UMDSimulation_from_umd function tests
def test_UMDSimulation_from_umd():
    """
    Test the UMDSimulation_from_umd function initializing a UMDSimulation
    object from an umd file.

    """
    with open(UMDfile_mag, 'r') as umd:
        basis = 5.70*np.identity(3)
        atoms = {O: 15, H: 28, Fe: 1}
        lattice = UMDLattice('3bccH2O+1Fe', basis, atoms)
        simulation = UMDSimulation_from_umd(umd)
        assert simulation.name == 'mag5.70a1800T'
        assert simulation.cycle == 3
        assert simulation.steps == 1900
        assert simulation.time == 0.85
        assert simulation.lattice == lattice


def test_UMDSimulation_from_umd_None():
    """
    Test the UMDSimulation_from_umd function initializing no UMDSimulation
    object from an umd file without any UMDSimulation.

    """
    with open('tests/test_file_empty.umd', 'r') as umd:
        simulation = UMDSimulation_from_umd(umd)
        assert simulation is None


test_UMDSimulation_from_umd()
test_UMDSimulation_from_umd_None()
