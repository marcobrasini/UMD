"""
===============================================================================
                            UMDAtom tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDAtom class and its
derivatives, like UMDLattice.

Classes
-------
    ScenariosUMDAtom

Functions
---------
    dataUMDAtom
    getUMDAtom
    getUMDAtom_dictionary

See Also
--------
    test_UMDAtom

"""


from ..libs.UMDAtom import UMDAtom

import pytest
import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass


# %% UMDAtom data scenarios for testing
@dataclass
class ScenariosUMDAtom:
    Z: st.SearchStrategy[int]
    name: st.SearchStrategy[str]
    mass: st.SearchStrategy[float]
    valence: st.SearchStrategy[int]


setUMDAtom = ScenariosUMDAtom(
    Z=st.integers(min_value=1),
    name=st.from_regex(r'[A-Z][a-z]'),
    mass=st.floats(min_value=0.0, allow_nan=False, allow_infinity=False),
    valence=st.integers(min_value=0)
    )


# %% Strategies generator functions
@st.composite
def dataUMDAtom(draw):
    """
    Generate the input data for a UMDAtom.

    """
    Z = draw(setUMDAtom.Z)
    name = draw(setUMDAtom.name)
    mass = draw(setUMDAtom.mass)
    valence = draw(setUMDAtom.valence)
    data = {"Z": Z, "name": name, "mass": mass, "valence": valence}
    return data


@st.composite
def getUMDAtom(draw):
    """
    Generate directly a UMDAtom object.

    """
    data = draw(dataUMDAtom())
    atom = UMDAtom(**data)
    return atom


@st.composite
def getUMDAtom_dictionary(draw, ntypes=1):
    atom_key = draw(st.lists(getUMDAtom(),
                             min_size=ntypes, max_size=ntypes, unique=True))
    atom_val = draw(st.lists(st.integers(1, 30),
                             min_size=ntypes, max_size=ntypes))
    atom_dict = dict(zip(atom_key, atom_val))
    return atom_dict


# %% Strategies generator tests
@hp.given(st.data())
def test_dataUMDAtom(data):
    """
    Test dataUMDAtom generator function.

    """
    data = data.draw(dataUMDAtom())
    assert isinstance(data["Z"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["mass"], float)
    assert isinstance(data["valence"], int)


@hp.given(st.data())
def test_getUMDAtom(data):
    """
    Test getUMDAtom generator function.

    """
    atom = data.draw(getUMDAtom())
    assert isinstance(atom, UMDAtom)


@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_getUMDAtom_dictionary(data, ntypes):
    """
    Test getUMDAtom_dictionary generator function.

    """
    atoms = data.draw(getUMDAtom_dictionary(ntypes))
    assert isinstance(atoms, dict)
    assert isinstance(list(atoms.keys())[-1], UMDAtom)
    assert isinstance(list(atoms.values())[-1], int)
