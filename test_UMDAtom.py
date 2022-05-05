# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:17:32 2022

@author: marco
"""

from UMDAtom import UMDAtom


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
    atom = UMDAtom(name='O', Z=8, mass=16.00, valence=6)
    assert atom.name == 'O'
    assert atom.Z == 8
    assert atom.mass == 16.00
    assert atom.valence == 6


test_UMDAtom_init_default()
test_UMDAtom_init_assignement()
