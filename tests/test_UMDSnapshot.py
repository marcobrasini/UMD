"""
===============================================================================
                          UMDSnapshot class tests
===============================================================================
"""

from ..libs.UMDSnapshot import UMDSnapshot

import numpy as np
import pytest
import hypothesis as hp
import hypothesis.strategies as st

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSnapDynamics import UMDSnapDynamics
from ..libs.UMDSnapThermodynamics import UMDSnapThermodynamics
from .test_scenarios_UMDSnapshot import dataUMDSnapshot
from .test_scenarios_UMDSnapDynamics import dataUMDSnapDynamics
from .test_scenarios_UMDSnapThermodynamics import dataUMDSnapThermodynamics


class Test_UMDSnapshot_unit:

    snap = 1129
    time = 0.5
    natoms = 2
    lattice = UMDLattice(atoms={UMDAtom(): natoms})

    # Thermodynamics parameters
    temperature = 1400  # in K
    pressure = 23       # in GPa
    energy = -1050      # in eV

    # Dynamics parameters
    time = 0.5
    position = np.array([[+0.47557534, +0.75247622, +0.26707477],
                         [+0.65057722, +0.82406818, +0.51003144]])
    velocity = np.array([[-0.96234100, +0.41585581, -0.33492285],
                         [+0.29512520, +0.29288268, -0.75090549]])
    force = np.array([[-0.80722157, -0.47571638, +0.23693435],
                      [+0.37777898, -0.20037447, -0.03918817]])

    # %% __init__ function tests
    def test_UMDSnapshot_init(self):
        """
        Test UMDSnapshot __init__ function assignement operation.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        assert snapshot.snap == self.snap
        assert snapshot.time == self.time
        assert snapshot.natoms == self.natoms
        assert snapshot.lattice == self.lattice

    # %% setThermodynamics and isUMDSnapThermodynamics function tests
    def test_UMDSnapshot_setThermodynamics(self):
        """
        Test UMDSnapshot setThermodynamics function from reference
        thermodynamics data.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        snapshot.setThermodynamics(self.temperature, self.pressure,
                                   self.energy)
        assert snapshot.temperature == self.temperature
        assert snapshot.pressure == self.pressure
        assert snapshot.energy == self.energy

    def test_UMDSnapshot_setThermodynamics_from_UMDSnapThermodynamics(self):
        """
        Test UMDSnapshot setThermodynamics function from UMDSnapThermodynamics
        object with the reference thermodynamics data.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        thermodynamics = UMDSnapThermodynamics(self.temperature, self.pressure,
                                               self.energy)
        snapshot.setThermodynamics(thermodynamics)
        assert snapshot.temperature == self.temperature
        assert snapshot.pressure == self.pressure
        assert snapshot.energy == self.energy

    def test_UMDSnapshot_setThermodynamics_from_UMDSnapThermodynamics_0(self):
        """
        Test UMDSnapshot setThermodynamics function from UMDSnapThermodynamics
        default object.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        thermodynamics = UMDSnapThermodynamics()
        snapshot.setThermodynamics(thermodynamics)
        assert snapshot.temperature == 0.0
        assert snapshot.pressure == 0.0
        assert snapshot.energy == 0.0

    def test_UMDSnapshot_setThermodynamics_TypeError(self):
        """
        Test UMDSnapsshot setThermodynamics function with wrong attributes.
        A TypeError is raised.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        with pytest.raises(TypeError):
            snapshot.setThermodynamics(keyword=1)

    # %% setDynamics and isUMDSnapDynamics functions tests
    def test_UMDSnapshot_setDynamics(self):
        """
        Test UMDSnapshot setDynamics function from reference dynamics data.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        snapshot.setDynamics(self.position, self.velocity, self.force)
        assert snapshot.time == self.time
        assert np.array_equal(snapshot.position, self.position)
        assert np.array_equal(snapshot.velocity, self.velocity)
        assert np.array_equal(snapshot.force, self.force)

    def test_UMDSnapshot_setDynamics_from_UMDSnapDynamics(self):
        """
        Test UMDSnapshot setDynamics function from UMDSnapDynamics object with
        the reference dynamics data.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        dynamics = UMDSnapDynamics(self.time, self.position, self.velocity,
                                   self.force)
        snapshot.setDynamics(dynamics)
        assert snapshot.time == self.time
        assert np.array_equal(snapshot.position, self.position)
        assert np.array_equal(snapshot.velocity, self.velocity)
        assert np.array_equal(snapshot.force, self.force)

    def test_UMDSnapshot_setDynamics_from_UMDSnapDynamics_0(self):
        """
        Test UMDSnapshot setDynamics function from UMDSnapDynamics default
        object.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        dynamics = UMDSnapDynamics(time=1.0)
        snapshot.setDynamics(dynamics)
        assert snapshot.time == 1.0
        assert np.array_equal(snapshot.position, np.zeros((2, 3), dtype=float))
        assert np.array_equal(snapshot.velocity, np.zeros((2, 3), dtype=float))
        assert np.array_equal(snapshot.force, np.zeros((2, 3), dtype=float))

    def test_UMDSnapshot_setDynamics_TypeError(self):
        """
        Test UMDSnapshot setDynamics function with wrong attributes.
        A TypeError is raised.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        with pytest.raises(TypeError):
            snapshot.setDynamics(keyword=1.0)

    # %% __str__ function tests
    def test_UMDSnapshot_str_length(self):
        """
        Test UMDSnapshot __str__ function length:
            - 20+1, the snapshot header length (+ '\n'),
            - 111+1, the snapshot thermodynamics string length (+ '\n'),
            - 460, the the snapshot dynamics string length for 2 atoms.

        """
        snapshot = UMDSnapshot(self.snap, self.time, self.lattice)
        snapshot.setDynamics(self.position, self.velocity, self.force)
        assert len(str(snapshot)) == (20+1) + (111+1) + 460


# %% ===================================================================== %% #
# %% hypothesis tests
@hp.given(data=st.data(), natoms=st.integers(1, 10))
def test_UMDSnapshot_init(data, natoms):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(dataUMDSnapshot(natoms))
    snapshot = UMDSnapshot(**data)
    assert snapshot.snap == data['snap']
    assert snapshot.time == data['time']
    assert snapshot.lattice == data['lattice']


@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_UMDSnapshot_setDynamics(data, ntypes):
    """
    Test the setDynamics function assignement operations.

    """
    snap = data.draw(dataUMDSnapshot(ntypes))
    snapshot = UMDSnapshot(**snap)
    dynamics = data.draw(dataUMDSnapDynamics(snapshot.natoms, time=0))
    snapshot.setDynamics(**dynamics)
    assert snapshot.time == snap['time']
    assert np.array_equal(snapshot.position, dynamics['position'])
    assert np.array_equal(snapshot.velocity, dynamics['velocity'])
    assert np.array_equal(snapshot.force, dynamics['force'])


@hp.given(data=st.data())
def test_UMDSnapshot_setThermodynamics(data):
    """
    Test the setThermodynamics function assignement operations.

    """
    snap = data.draw(dataUMDSnapshot())
    snapshot = UMDSnapshot(**snap)
    thermodynamics = data.draw(dataUMDSnapThermodynamics())
    snapshot.setThermodynamics(**thermodynamics)
    assert snapshot.energy == thermodynamics['energy']
    assert snapshot.pressure == thermodynamics['pressure']
    assert snapshot.temperature == thermodynamics['temperature']


@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_UMDSnapshot_str_length(data, ntypes):
    """
    Test the __str__ function correct length of the string object returned.
    The header line length is 20+1, the UMDSnapThermodynamics string length is
    111+1 and the UMDSnapDynamics string length for n atoms is 170+n*145.

    """
    snap = data.draw(dataUMDSnapshot(ntypes))
    snapshot = UMDSnapshot(**snap)
    natoms = snapshot.natoms
    dynamics = data.draw(dataUMDSnapDynamics(natoms, time=0))
    thermodynamics = data.draw(dataUMDSnapThermodynamics())
    snapshot.setDynamics(**dynamics)
    snapshot.setThermodynamics(**thermodynamics)
    assert len(str(snapshot)) == (20+1) + (111+1) + (170 + natoms*145)
