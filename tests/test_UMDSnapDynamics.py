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
        snapdynamics = UMDSnapDynamics(self.time, self.position,
                                       self.velocity, self.force)
        assert snapdynamics.time == self.time
        assert np.array_equal(snapdynamics.position, self.position)
        assert np.array_equal(snapdynamics.velocity, self.velocity)
        assert np.array_equal(snapdynamics.force, self.force)

    # %% UMDSnapDynamics __str__ function tests
    def test_UMDSnapDynamics_str(self):
        """
        Test the __str__ function to convert the UMDSnapDynamics data into a
        descriptive and printable string object.

        """
        snapdynamics = UMDSnapDynamics(self.time, self.position,
                                       self.velocity, self.force)
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
        print(str(snapdynamics), len(str(snapdynamics)))
        print(string, len(string))
        assert str(snapdynamics) == string

    def test_UMDSnapDynamics_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        The header lines length is 170 = (25+1) + (3*16)+(3*16)+(3*16), while
        the dynamics line length for each atom is 145 = (9*16) + 1.
        So for two atoms the total length is 460 = 170 + 2*145.

        """
        snapdynamics = UMDSnapDynamics(self.time, self.position,
                                       self.velocity, self.force)
        assert len(str(snapdynamics)) == 460


# %% ===================================================================== %% #
# %% UMDSnapDynamics hypothesis tests
@hp.given(data=st.data(), natoms=st.integers(1, 100))
def test_UMDSnapDynamics_init(data, natoms):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(dataUMDSnapDynamics(natoms))
    snapdynamics = UMDSnapDynamics(**data)
    assert snapdynamics.time == data['time']
    assert np.array_equal(snapdynamics.position, data['position'])
    assert np.array_equal(snapdynamics.velocity, data['velocity'])
    assert np.array_equal(snapdynamics.force, data['force'])


@hp.given(data=st.data(), natoms=st.integers(1, 100))
def test_UMDSnapDynamics_str_length(data, natoms):
    """
    Test the __str__ function correct length of the string object returned.
    The header lines length is 170 = (25+1) + (3*16)+(3*16)+(3*16), while
    the dynamics line length for each atom is 145 = (9*16) + 1.
    So for n atoms the total length is 170 + 145*n.

    """
    data = data.draw(dataUMDSnapDynamics(natoms))
    snapdynamics = UMDSnapDynamics(**data)
    assert len(str(snapdynamics)) == 170 + 145*natoms
