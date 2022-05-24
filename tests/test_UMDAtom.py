"""
===============================================================================
                              UMDAtom class tests                              
===============================================================================
"""

from ..UMDAtom import UMDAtom

import pytest
import hypothesis as hp
import hypothesis.strategies as st
from .generate_scenarios import generateUMDAtom


# %% unit tests for O atom 
class Test_UMDAtom_unit:
    """
    The unit tests implemented test an instance of the UMDAtom class
    representing an oxigen atom.

    """

    atom1 = UMDAtom(Z=8, name='O', mass=16.00, valence=6)

    # %% UMDAtom __init__ function tests
    def test_UMDAtom_init_default(self):
        """
        Test the __init__ function defualt constructor.

        """
        atom = UMDAtom()
        assert atom.name == ''
        assert atom.Z == 0
        assert atom.mass == 0
        assert atom.valence == 0

    def test_UMDAtom_init_assignement(self):
        """
        Test the __init__ function assignement operations.

        """
        assert self.atom1.name == 'O'
        assert self.atom1.Z == 8
        assert self.atom1.mass == 16.00
        assert self.atom1.valence == 6

    # %% UMDAtom __eq__ function tests
    def test_UMDAtom_eq_true(self):
        """
        Test the __eq__ function to compare two UMDAtom objects representing
        two identical atoms. The value returned must be True.

        """
        atom2 = UMDAtom(Z=8, name='O', mass=16.00, valence=6)
        assert self.atom1 == atom2

    def test_UMDAtom_eq_false_Z(self):
        """
        Test the __eq__ function to compare two UMDAtom objects representing
        two atoms with different Z. The value returned must be False.

        """
        atom2 = UMDAtom(Z=0, name='O', mass=16.00, valence=6)
        assert not self.atom1 == atom2

    def test_UMDAtom_eq_false_name(self):
        """
        Test the __eq__ function to compare two UMDAtom objects representing
        two atoms with different names. The value returned must be False.

        """
        atom2 = UMDAtom(Z=8, name='o', mass=16.00, valence=6)
        assert not self.atom1 == atom2

    def test_UMDAtom_eq_false_mass(self):
        """
        Test the __eq__ function to compare two UMDAtom objects representing
        two atoms with different masses. The value returned must be False.

        """
        atom2 = UMDAtom(Z=8, name='O', mass=00.00, valence=6)
        assert not self.atom1 == atom2

    def test_UMDAtom_eq_false_valence(self):
        """
        Test the __eq__ function to compare two UMDAtom objects representing
        two atoms with different valences. The value returned must be False.

        """
        atom2 = UMDAtom(Z=8, name='O', mass=16.00, valence=8)
        assert not self.atom1 == atom2

    # %% UMDAtom __hash__ function tests
    def test_UMDAtom_hash_eq_dict(self):
        """
        Test the __hash__ function to compare two dictionaries with a UMDAtom
        object as key. For two equal UMDAtom keys, the value returned by two
        dictionary comparison must be True.

        """
        atom2 = UMDAtom(Z=8, name='O', mass=16.00, valence=6)
        dict1 = {self.atom1: 1}
        dict2 = {atom2: 1}
        assert dict1 == dict2

    def test_UMDAtom_hash_noteq_dict(self):
        """
        Test the __hash__ function to compare two dictionaries with a UMDAtom
        object as key. For two different UMDAtom keys, the value returned by
        two dictionary comparison must be False.

        """
        atom2 = UMDAtom(Z=8, name='o', mass=16.00, valence=6)
        dict1 = {self.atom1: 1}
        dict2 = {atom2: 1}
        assert not dict1 == dict2

    # %% UMDAtom __str__ function tests
    def test_UMDAtom_str(self):
        """
        Test the __str__ function to convert the UMDAtom information into a
        string object correspondent with its atomic symbol.

        """
        assert str(self.atom1) == 'O'


# %% ===================================================================== %% #
# %% hypotesis tests
@hp.given(data=st.data())
def test_UMDAtom_init_assignement(data):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(generateUMDAtom())
    atom = UMDAtom(**data)
    assert atom.Z == data['Z']
    assert atom.name == data['name']
    assert atom.mass == data['mass']
    assert atom.valence == data['valence']


@hp.given(data1=st.data(), data2=st.data())
def test_UMDAtom_eq(data1, data2):
    """
    Test the __eq__ function to compare two UMDAtom objects. If they represent
    two identical atoms the value returned must be True, otherwise False.

    """
    data1 = data1.draw(generateUMDAtom())
    data2 = data2.draw(generateUMDAtom())
    atom1 = UMDAtom(**data1)
    atom2 = UMDAtom(**data2)
    assert (atom1 == atom2) == (data1 == data2)


@hp.given(data1=st.data(), data2=st.data())
def test_UMDAtom_hash(data1, data2):
    """
    Test the __hash__ function to compare two dictionaries with a UMDAtom
    object as key. For two equal UMDAtom keys, the value returned by two
    dictionary comparison must be True, otherwise False.

    """
    data1 = data1.draw(generateUMDAtom())
    data2 = data2.draw(generateUMDAtom())
    atom1 = UMDAtom(**data1)
    atom2 = UMDAtom(**data2)
    assert ({atom1: 1} == {atom2: 1}) == (data1 == data2)


@hp.given(data=st.data())
def test_UMDAtom_str(data):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(generateUMDAtom())
    atom = UMDAtom(**data)
    assert str(atom) == data['name']
