"""
===============================================================================
                           UMDLattice tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDLattice class and its
derivatives, like UMDSimulation.

Classes
-------
    ScenariosUMDLattice

Functions
---------
    dataUMDLattice
    getUMDLattice

See Also
--------
    test_UMDLattice

"""


from ..libs.UMDLattice import UMDLattice
from ..libs.UMDAtom import UMDAtom


import numpy as np
import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass
from .test_scenarios import getNumpyArray
from .test_scenarios_UMDAtom import getUMDAtom_dictionary


# %% UMDAtom data scenarios for testing
@dataclass
class ScenariosUMDLattice:
    name: st.SearchStrategy[str]
    basis: st.SearchStrategy[list]
    atoms: st.SearchStrategy[dict]


setUMDLattice = ScenariosUMDLattice(
    name=st.text(max_size=30),
    basis=getNumpyArray(3, 3),
    atoms=getUMDAtom_dictionary
    )


# %% Strategies generator functions
@st.composite
def dataUMDLattice(draw, ntypes=1):
    """
    Generate the input data for a UMDLattice.

    """
    name = draw(setUMDLattice.name)
    basis = draw(setUMDLattice.basis) + np.identity(3)
    atoms = draw(setUMDLattice.atoms(ntypes))
    data = {"name": name, "basis": basis, "atoms": atoms}
    return data


@st.composite
def getUMDLattice(draw, ntypes=1):
    """
    Generate directly a UMDLattice object.

    """
    data = draw(dataUMDLattice(ntypes))
    lattice = UMDLattice(**data)
    return lattice


# %% Strategies generator tests
@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_dataUMDLattice(data, ntypes):
    """
    Test dataUMDLattice generator function.

    """
    data = data.draw(dataUMDLattice(ntypes))
    assert isinstance(data["name"], str)
    assert len(data["name"]) <= 30

    assert isinstance(data["basis"], type(np.array([])))
    assert data["basis"].shape == (3, 3)

    assert isinstance(data["atoms"], dict)
    assert isinstance(list(data["atoms"].keys())[0], type(UMDAtom()))
    assert isinstance(list(data["atoms"].values())[0], int)
    assert len(data["atoms"]) == ntypes


@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_getUMDLattice(data, ntypes):
    """
    Test getUMDLattice generator function.

    """
    lattice = data.draw(getUMDLattice(ntypes))
    assert isinstance(lattice, UMDLattice)
