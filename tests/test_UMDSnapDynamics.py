"""
===============================================================================
                         UMDSnapDynamics class tests
===============================================================================
"""


from ..libs.UMDSnapDynamics import UMDSnapDynamics

import numpy as np
import hypothesis as hp
import hypothesis.strategies as st

from .test_scenarios_UMDSnapDynamics import dataUMDSnapDynamics


# %% UMDSnapThermodynamics unit tests
class TestUMDSnapDynamics:
    """
    The unit tests implemented test an instance of the UMDSnapDynamics class
    representing a snapshot with the following atomic dynamic quantities:
        - snap : natoms = 10

    """
    time = 0.5
    position = np.array([[+0.47557534, +0.75247622, +0.26707477],
                         [+0.65057722, +0.82406818, +0.51003144]])
    velocity = np.array([[-0.96234100, +0.41585581, -0.33492285],
                         [+0.29512520, +0.29288268, -0.75090549]])
    force = np.array([[-0.80722157, -0.47571638, +0.23693435],
                      [+0.37777898, -0.20037447, -0.03918817]])
    dynamics = UMDSnapDynamics(time=time, position=position, velocity=velocity,
                               force=force)

    # %% UMDSnapDynamics __init__ function tests
    def test_UMDSnapDynamics_init_default(self):
        """
        Test the __init__ function defualt constructor.

        """
        snapdynamics = UMDSnapDynamics()
        assert snapdynamics.time == 0.0
        assert snapdynamics.position == []
        assert snapdynamics.velocity == []
        assert snapdynamics.force == []

    def test_UMDSnapDynamics_init_assignement(self):
        """
        Test the __init__ function assignement operations.

        """
        assert self.dynamics.time == self.time
        assert np.array_equal(self.dynamics.position, self.position)
        assert np.array_equal(self.dynamics.velocity, self.velocity)
        assert np.array_equal(self.dynamics.force, self.force)

    # %% UMDSnapDynamics __eq__ function tests
    def test_UMDSnapDynamics_eq_true(self):
        """
        Test the __eq__ function to compare two UMDSnapDynamics objects storing
        the dynamic quantities of two identical snapshots.
        The returned value must be True.

        """
        dynamics = UMDSnapDynamics(time=self.time, position=self.position, 
                                   velocity=self.velocity, force=self.force)
        assert dynamics == self.dynamics

    def test_UMDSnapDynamics_eq_false_time(self):
        """
        Test the __eq__ function to compare two UMDSnapDynamics objects storing
        the dynamic quantities of two snapshots, with different time duration.
        The returned value must be False.

        """
        dynamics = UMDSnapDynamics(time=0.0, position=self.position, 
                                   velocity=self.velocity, force=self.force)
        assert not dynamics == self.dynamics

    def test_UMDSnapDynamics_eq_false_position(self):
        """
        Test the __eq__ function to compare two UMDSnapDynamics objects storing
        the dynamic quantities of two snapshots, with different atoms position.
        The returned value must be False.

        """
        dynamics = UMDSnapDynamics(time=self.time, position=0.0, 
                                   velocity=self.velocity, force=self.force)
        assert not dynamics == self.dynamics

    def test_UMDSnapDynamics_eq_false_velocity(self):
        """
        Test the __eq__ function to compare two UMDSnapDynamics objects storing
        the dynamic quantities of two snapshots, with different atoms velocity.
        The returned value must be False.

        """
        dynamics = UMDSnapDynamics(time=self.time, position=self.position, 
                                   velocity=0.0, force=self.force)
        assert not dynamics == self.dynamics

    def test_UMDSnapDynamics_eq_false_force(self):
        """
        Test the __eq__ function to compare two UMDSnapDynamics objects storing
        the dynamic quantities of two snapshots, with different atoms force.
        The returned value must be False.

        """
        dynamics = UMDSnapDynamics(time=self.time, position=self.position, 
                                   velocity=self.velocity, force=0.0)
        assert not dynamics == self.dynamics

    # %% UMDSnapDynamics __str__ function tests
    def test_UMDSnapDynamics_str(self):
        """
        Test the __str__ function to convert the UMDSnapDynamics data into a
        descriptive and printable string object.

        """
        string  = "Dynamics:        0.500 fs\n"
        string += "Position_x      Position_y      Position_z      "
        string += "Velocity_x      Velocity_y      Velocity_z      "
        string += "Force_x         Force_y         Force_z         \n"
        string += "      0.47557534      0.75247622      0.26707477"
        string += "     -0.96234100      0.41585581     -0.33492285"
        string += "     -0.80722157     -0.47571638      0.23693435\n"
        string += "      0.65057722      0.82406818      0.51003144"
        string += "      0.29512520      0.29288268     -0.75090549"
        string += "      0.37777898     -0.20037447     -0.03918817"
        assert str(self.dynamics) == string

    def test_UMDSnapDynamics_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        The header lines length is 170 = (25+1) + (3*16)+(3*16)+(3*16), while
        the dynamics line length for each atom is 145 = (9*16) + 1.
        So for two atoms the total length is 460 = 170 + 2*145.

        """
        assert len(str(self.dynamics)) == 460


# %% ===================================================================== %% #
# %% UMDSnapDynamics hypothesis tests
@hp.given(data=st.data(), natoms=st.integers(1, 100))
def test_UMDSnapDynamics_init(data, natoms):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(dataUMDSnapDynamics(natoms))
    dynamics = UMDSnapDynamics(**data)
    assert dynamics.time == data['time']
    assert np.array_equal(dynamics.position, data['position'])
    assert np.array_equal(dynamics.velocity, data['velocity'])
    assert np.array_equal(dynamics.force, data['force'])


@hp.given(data1=st.data(), data2=st.data())
def test_UMDSnapDynamics_eq(data1, data2):
    """
    Test the __eq__ function to compare two UMDSnapDynamics objects storing
    the dynamic quantities of two snapshots.

    """
    data1 = data1.draw(dataUMDSnapDynamics())
    data2 = data2.draw(dataUMDSnapDynamics())
    dynamics1 = UMDSnapDynamics(**data1)
    dynamics2 = UMDSnapDynamics(**data2)
    equal  = (data1['time'] == data2['time'])
    equal *= np.array_equal(data1['position'], data2['position'])
    equal *= np.array_equal(data1['velocity'], data2['velocity'])
    equal *= np.array_equal(data1['force'], data2['force'])
    assert bool(dynamics1 == dynamics2) is bool(equal)


@hp.given(data=st.data(), natoms=st.integers(1, 100))
def test_UMDSnapDynamics_str_length(data, natoms):
    """
    Test the __str__ function correct length of the string object returned.
    The header lines length is 170 = (25+1) + (3*16)+(3*16)+(3*16), while
    the dynamics line length for each atom is 145 = (9*16) + 1.
    So for n atoms the total length is 170 + 145*n.

    """
    data = data.draw(dataUMDSnapDynamics(natoms))
    dynamics = UMDSnapDynamics(**data)
    assert len(str(dynamics)) == 170 + 145*natoms
