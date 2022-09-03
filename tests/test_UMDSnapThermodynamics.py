"""
===============================================================================
                    UMDSnapThermodynamics class tests
===============================================================================
"""


from ..libs.UMDSnapThermodynamics import UMDSnapThermodynamics

import pytest
import hypothesis as hp
import hypothesis.strategies as st

from .test_scenarios_UMDSnapThermodynamics import dataUMDSnapThermodynamics
from .test_scenarios_UMDSnapThermodynamics import getUMDSnapThermodynamics


# %% UMDSnapThermodynamics unit tests
class TestUMDSnapThermodynamics:
    """
    The unit tests implemented test an instance of the UMDSnapThermodynamics
    class representing a snapshot with the following thermodynamics quantities:
        - snap : temperature=1400 K, pressure=23 GPa, energy=-1050 eV

    """
    temperature = 1400  # in K
    pressure = 23       # in GPa
    energy = -1050      # in eV

    # %% UMDSnapThermodynamics __init__ function tests
    def test_UMDSnapThermodynamics_init_default(self):
        """
        Test the __init__ function defualt constructor.

        """
        snapthermodynamics = UMDSnapThermodynamics()
        assert snapthermodynamics.temperature == 0.0
        assert snapthermodynamics.pressure == 0.0
        assert snapthermodynamics.energy == 0.0

    def test_UMDSnapThermodynamics_init_assignement(self):
        """
        Test the __init__ function assignement operations.

        """
        snapthermodynamics = UMDSnapThermodynamics(self.temperature,
                                                   self.pressure, self.energy)
        assert snapthermodynamics.temperature == self.temperature
        assert snapthermodynamics.pressure == self.pressure
        assert snapthermodynamics.energy == self.energy

    # %% UMDSnapThermodynamics __str__ function tests
    def test_UMDSnapThermodynamics_str(self):
        """
        Test the __str__ function to convert the UMDSnapThermodynamics
        quantities into a descriptive and printable string object.

        """
        snapthermodynamics = UMDSnapThermodynamics(self.temperature,
                                                   self.pressure, self.energy)
        string  = "Thermodynamics:\n"
        string += "  Temperature =    1400.0000 K\n"
        string += "  Pressure    =      23.0000 GPa\n"
        string += "  Energy      =   -1050.0000 eV"
        print(string)
        assert str(snapthermodynamics) == string

    def test_UMDSnapThermodynamics_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        Its length is constant and must be equal to 111 characters.

        """
        snapthermodynamics = UMDSnapThermodynamics(self.temperature,
                                                   self.pressure, self.energy)
        stringlength = 16 + (2+14+12+3) + (2+14+12+5) + (2+14+12+3)
        assert len(str(snapthermodynamics)) == stringlength


# %% ===================================================================== %% #
# %% UMDSnapThermodynamics hypothesis tests
@hp.given(st.data())
def test_UMDSnapThermodynamics_init(data):
    """
    Test UMDSnapThermodynamics __init__ function assignement operations.

    """
    data = data.draw(dataUMDSnapThermodynamics())
    snapthermodynamics = UMDSnapThermodynamics(**data)
    assert snapthermodynamics.temperature == data['temperature']
    assert snapthermodynamics.pressure == data['pressure']
    assert snapthermodynamics.energy == data['energy']


@hp.given(st.data())
def test_UMDSnapThermodynamics_str_length(data):
    """
    Test the UMDSimulationRun str function. The string returned must have a
    length of exactly 111 characters.

    """
    data = data.draw(dataUMDSnapThermodynamics())
    snapthermodynamics = UMDSnapThermodynamics(**data)
    print(len(str(snapthermodynamics)))
    assert len(str(snapthermodynamics)) == 111
