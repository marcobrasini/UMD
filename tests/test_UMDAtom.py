# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:17:32 2022

@author: marco
"""

from ..UMDAtom import UMDAtom


atom1 = UMDAtom(name='O', Z=8, mass=16.00, valence=6)


# %%  UMDAtom __init__ function tests
def test_UMDAtom_init_default():
    """
    Test the __init__ function defualt constructor.

    """
    atom = UMDAtom()
    assert atom.name == ''
    assert atom.Z == 0
    assert atom.mass == 0
    assert atom.valence == 0


def test_UMDAtom_init_assignement():
    """
    Test the __init__ function assignement operations.

    """
    assert atom1.name == 'O'
    assert atom1.Z == 8
    assert atom1.mass == 16.00
    assert atom1.valence == 6


# %% UMDAtom __eq__ function tests
def test_UMDAtom_eq_true():
    """
    Test the __eq__ function to compare two UMDAtom objects representing
    two identical atoms. The value returned must be True.

    """
    atom2 = UMDAtom(name='O', Z=8, mass=16.00, valence=6)
    assert atom1 == atom2


def test_UMDAtom_eq_false_name():
    """
    Test the __eq__ function to compare two UMDAtom objects representing
    two atoms with different names. The value returned must be False.

    """
    atom2 = UMDAtom(name='', Z=8, mass=16.00, valence=6)
    assert not atom1 == atom2


def test_UMDAtom_eq_false_Z():
    """
    Test the __eq__ function to compare two UMDAtom objects representing
    two atoms with different Z. The value returned must be False.

    """
    atom2 = UMDAtom(name='O', Z=0, mass=16.00, valence=6)
    assert not atom1 == atom2


def test_UMDAtom_eq_false_mass():
    """
    Test the __eq__ function to compare two UMDAtom objects representing
    two atoms with different masses. The value returned must be False.

    """
    atom2 = UMDAtom(name='O', Z=8, mass=00.00, valence=6)
    assert not atom1 == atom2


def test_UMDAtom_eq_false_valence():
    """
    Test the __eq__ function to compare two UMDAtom objects representing
    two atoms with different valences. The value returned must be False.

    """
    atom2 = UMDAtom(name='O', Z=8, mass=16.00, valence=0)
    assert not atom1 == atom2


# %% UMDAtom __hash__ function tests
def test_UMDAtom_hash_eq_dict():
    """
    Test the __hash__ function to compare two dictionaries with a UMDAtom
    object as key. For two equal UMDAtom keys, the value returned by two
    dictionary comparison must be True.

    """
    atom2 = UMDAtom(name='O', Z=8, mass=16.00, valence=6)
    dict1 = {atom1: 1}
    dict2 = {atom2: 1}
    assert dict1 == dict2


def test_UMDAtom_hash_noteq_dict():
    """
    Test the __hash__ function to compare two dictionaries with a UMDAtom
    object as key. For two different UMDAtom keys, the value returned by two
    dictionary comparison must be False.

    """
    atom2 = UMDAtom(name='o', Z=8, mass=16.00, valence=6)
    dict1 = {atom1: 1}
    dict2 = {atom2: 1}
    assert not dict1 == dict2


# %% UMDAtom __str__ function tests
def test_UMDAtom_str():
    """
    Test the __str__ function to convert the UMDAtom information into a
    string object correspondent with its atomic symbol.

    """
    assert str(atom1) == 'O'
