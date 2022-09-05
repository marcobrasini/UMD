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
    thermodynamics = UMDSnapThermodynamics(temperature=temperature,
                                           pressure=pressure, energy=energy)

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
        assert self.thermodynamics.temperature == self.temperature
        assert self.thermodynamics.pressure == self.pressure
        assert self.thermodynamics.energy == self.energy

    # %% UMDSnapThermodynamics __eq__ function tests
    def test_UMDSnapThermodynamics_eq_true(self):
        """
        Test the __eq__ function to compare two UMDSnapThermodynamics objects
        storing the thermodynamics quantities of two identical snapshots.
        The returned value must be True.

        """
        thermodynamics = UMDSnapThermodynamics(temperature=self.temperature,
                                               pressure=self.pressure, 
                                               energy=self.energy)
        assert thermodynamics == self.thermodynamics
    
    def test_UMDSnapThermodynamics_eq_false_temperature(self):
        """
        Test the __eq__ function to compare two UMDSnapThermodynamics objects
        storing the thermodynamics quantities of two snapshots, with different
        temperature.
        The returned value must be False.

        """
        thermodynamics = UMDSnapThermodynamics(temperature=0.0,
                                               pressure=self.pressure, 
                                               energy=self.energy)
        assert not thermodynamics == self.thermodynamics
    
    def test_UMDSnapThermodynamics_eq_false_pressure(self):
        """
        Test the __eq__ function to compare two UMDSnapThermodynamics objects
        storing the thermodynamics quantities of two snapshots, with different
        pressure.
        The returned value must be False.

        """
        thermodynamics = UMDSnapThermodynamics(temperature=self.temperature,
                                               pressure=0.0, 
                                               energy=self.energy)
        assert not thermodynamics == self.thermodynamics
    
    def test_UMDSnapThermodynamics_eq_false_energy(self):
        """
        Test the __eq__ function to compare two UMDSnapThermodynamics objects
        storing the thermodynamics quantities of two snapshots, with different
        energy.
        The returned value must be False.

        """
        thermodynamics = UMDSnapThermodynamics(temperature=self.temperature,
                                               pressure=self.pressure, 
                                               energy=0.0)
        assert not thermodynamics == self.thermodynamics
        

    # %% UMDSnapThermodynamics __str__ function tests
    def test_UMDSnapThermodynamics_str(self):
        """
        Test the __str__ function to convert the UMDSnapThermodynamics
        quantities into a descriptive and printable string object.

        """
        string  = "Thermodynamics:\n"
        string += "  Temperature =    1400.000000 K\n"
        string += "  Pressure    =      23.000000 GPa\n"
        string += "  Energy      =   -1050.000000 eV"
        assert str(self.thermodynamics) == string

    def test_UMDSnapThermodynamics_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        Its length is constant and must be equal to 111 characters.

        """
        stringlength = 16 + (2+14+14+3) + (2+14+14+5) + (2+14+14+3)
        assert len(str(self.thermodynamics)) == stringlength


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


@hp.given(data1=st.data(), data2=st.data())
def test_UMDSnapThermodynamics_eq(data1, data2):
    """
    Test the __eq__ function to compare two UMDSnapThermodynamics objects
    storing the thermodynamics quantities of two snapshots.

    """
    data1 = data1.draw(dataUMDSnapThermodynamics())
    data2 = data2.draw(dataUMDSnapThermodynamics())
    thermodynamics1 = UMDSnapThermodynamics(**data1)
    thermodynamics2 = UMDSnapThermodynamics(**data2)
    assert bool(thermodynamics1 == thermodynamics2) is (data1 == data2)


@hp.given(st.data())
def test_UMDSnapThermodynamics_str_length(data):
    """
    Test the UMDSnapThermodynamics __str__ function. The string returned must
    have a length of exactly 117 characters.

    """
    data = data.draw(dataUMDSnapThermodynamics())
    snapthermodynamics = UMDSnapThermodynamics(**data)
    print(len(str(snapthermodynamics)))
    assert len(str(snapthermodynamics)) == 117
