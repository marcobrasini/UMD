# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:45:55 2022

@author: marco
"""

from UMDSnapThermodynamics import UMDSnapThermodynamics


# %% UMDSnapThermodynamics __init__ function tests
def test_UMDSnapThermodynamics_init_default():
    """
    Test the __init__ function defualt constructor.

    """
    snapthermodynamics = UMDSnapThermodynamics()
    assert snapthermodynamics.temperature == 0.0
    assert snapthermodynamics.pressure == 0.0
    assert snapthermodynamics.energy == 0.0


def test_UMDSnapThermodynamics_init_assignement():
    """
    Test the __init__ function assignement operations.

    """
    temperature = 1400  # in K
    pressure = 20       # in GPa
    energy = -1050      # in eV
    snapthermodynamics = UMDSnapThermodynamics(temperature, pressure, energy)
    assert snapthermodynamics.temperature == temperature
    assert snapthermodynamics.pressure == pressure
    assert snapthermodynamics.energy == energy


test_UMDSnapThermodynamics_init_default()
test_UMDSnapThermodynamics_init_assignement()


# %% UMDSnapThermodynamics __str__ function tests
def test_UMDSnapThermodynamics_init_assignement():
    """
    Test the __str__ function to convert the UMDSnapThermodynamics information
    into a descriptive and printable string object.

    """
    temperature = 1400  # in K
    pressure = 23       # in GPa
    energy = -1050      # in eV
    snapthermodynamics = UMDSnapThermodynamics(temperature, pressure, energy)
    string  = "Temperature =    1400.0000 K\n"
    string += "Pressure    =      23.0000 GPa\n"
    string += "Energy      =   -1050.0000 eV"
    assert str(snapthermodynamics) == string


test_UMDSnapThermodynamics_init_assignement()
