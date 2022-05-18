# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:40:14 2022

@author: marco
"""

from UMDSnapshot_from_umd import UMDSnapThermodynamics_from_umd


UMDfile_mag = 'tests/mag5.70a1800T.umd'


# %% UMDSnapThermodynamics_from_umd  function tests
def test_UMDSnapThermodynamics_from_umd():
    """
    Test UMDSnapThermodynamics_from_umd function initializing a
    UMDSnapThermodynamics object from an umd file.

    """
    with open(UMDfile_mag, 'r') as umd:
        snapThermodynamics = UMDSnapThermodynamics_from_umd(umd)
        assert snapThermodynamics.temperature == 1804.3700
        assert snapThermodynamics.pressure == 24.6525
        assert snapThermodynamics.energy == -192.7077
        umd.close()


def test_UMDSnapThermodynamics_from_umd_None():
    """
    Test the UMDSnapThermodynamics_from_umd function initializing no
    UMDSnapThermodynamics object from an umd file without any UMDSnapshot.

    """
    with open('tests/test_file_empty.umd', 'r') as umd:
        snapThermodynamics = UMDSnapThermodynamics_from_umd(umd)
        assert snapThermodynamics is None


test_UMDSnapThermodynamics_from_umd()
test_UMDSnapThermodynamics_from_umd_None()
