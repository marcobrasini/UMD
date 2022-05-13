# -*- coding: utf-8 -*-
"""
Created on Thu May 12 17:13:29 2022

@author: marco
"""

from UMDSnapshot import UMDSnapshot
from UMDSnapThermodynamics import UMDSnapThermodynamics
from UMDSnapDynamics import UMDSnapDynamics

import hypothesis as hp
import hypothesis.strategies as st

import numpy as np
from UMDAtom import UMDAtom
from UMDLattice import UMDLattice


at = UMDAtom()


# %% UMDSnapshot reset static function tests
def test_UMDSnapshot_reset_default():
    """
    Test UMDSnapshot reset static function by default.

    """
    UMDSnapshot.reset()
    assert UMDSnapshot.snaptime == 0.0
    assert UMDSnapshot.lattice == UMDLattice()
    assert UMDSnapshot.natoms == 0


@hp.given(snaptime=st.floats(allow_infinity=False, allow_nan=False),
          natoms=st.integers(min_value=0, max_value=(1000)))
def test_UMDSnapshot_reset_assignement(snaptime, natoms):
    """
    Test UMDSnapshot reset static function assignement operation.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={at: natoms})
    UMDSnapshot.reset(snaptime=snaptime, lattice=lattice)
    assert UMDSnapshot.snaptime == snaptime
    assert UMDSnapshot.lattice == lattice
    assert UMDSnapshot.natoms == natoms


test_UMDSnapshot_reset_default()
test_UMDSnapshot_reset_assignement()


# %% UMDSnapshot __init_function tests
@hp.given(snaptime=st.floats(allow_infinity=False, allow_nan=False),
          natoms=st.integers(min_value=0, max_value=(1000)),
          nsnap=st.integers(min_value=0, max_value=(100000)))
def test_UMDSnapshot_init(snaptime, natoms, nsnap):
    """
    Test UMDSnapshot __init__ function assignement operation by using default
    UMDSnapDynamics and UMDSnapThermodynamics object.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={at: natoms})
    UMDSnapshot.reset(snaptime=snaptime, lattice=lattice)
    snapthermodynamics = UMDSnapThermodynamics()
    snapdynamics = UMDSnapDynamics()
    snapshot = UMDSnapshot(nsnap, snapthermodynamics, snapdynamics)
    assert snapshot.snapStep == nsnap
    assert snapshot.snapDynamics == snapdynamics
    assert snapshot.snapThermodynamics == snapthermodynamics


test_UMDSnapshot_init()


# %% UMDSnapshot __str__ function tests
@hp.given(snaptime=st.floats(allow_infinity=False, allow_nan=False),
          natoms=st.integers(min_value=0, max_value=(1000)),
          nsnap=st.integers(min_value=0, max_value=(100000)))
def test_UMDSnapshot_str_length(snaptime,natoms, nsnap):
    """
    Test the __str__ function correct length of the string object returned.
    Its length depends on the number of atoms in the lattice.

    """
    lattice = UMDLattice(basis=np.identity(3), atoms={at: natoms})
    UMDSnapshot.reset(snaptime=snaptime, lattice=lattice)
    dynamics = UMDSnapDynamics()
    thermodynamics = UMDSnapThermodynamics()
    snapshot = UMDSnapshot(nsnap, thermodynamics, dynamics)
    stringlength = (10+10+1) + (89+1) + len(str(dynamics))
    assert len(str(snapshot)) == stringlength


test_UMDSnapshot_str_length()
