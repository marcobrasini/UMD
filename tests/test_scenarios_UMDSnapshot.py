"""
===============================================================================
                         UMDSnapshot tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDSnapshot class.

Functions
---------
    dataUMDSnapshot
    getUMDSnapshot

See Also
--------
    test_UMDSnapshot
    test_scenarios_UMDLattice
    test_scenarios_UMDSnapDynamics
    test_scenarios_UMDSnapThermodynamics

"""


from ..libs.UMDSnapshot import UMDSnapshot

import hypothesis as hp
import hypothesis.strategies as st

from ..libs.UMDLattice import UMDLattice
from .test_scenarios_UMDLattice import getUMDLattice
from .test_scenarios_UMDSnapDynamics import dataUMDSnapDynamics
from .test_scenarios_UMDSnapThermodynamics import dataUMDSnapThermodynamics


@st.composite
def dataUMDSnapshot(draw, ntypes=1):
    """
    Strategy to generate input data of a UMDSnapshot object.

    """
    snap = draw(st.integers(0, 100000000))
    lattice = draw(getUMDLattice(ntypes))
    data = {"snap": snap, "lattice": lattice}
    return data


@st.composite
def getUMDSnapshot(draw, ntypes=1):
    """
    Strategy to generate a UMDSnapshot object.

    """
    data = draw(dataUMDSnapshot(ntypes))
    natoms = sum(data["lattice"].atoms.values())
    dynamics = draw(dataUMDSnapDynamics(natoms))
    thermodynamics = draw(dataUMDSnapThermodynamics())
    snapshot = UMDSnapshot(**data)
    snapshot.setDynamics(**dynamics)
    snapshot.setThermodynamics(**thermodynamics)
    return snapshot


# %% Strategies generator tests
@hp.given(data=st.data(), natoms=st.integers(1, 10))
def test_dataUMDSnapshot(data, natoms):
    """
    Test dataUMDSnapshot generator function.

    """
    data = data.draw(dataUMDSnapshot(natoms))
    assert isinstance(data['snap'], int)
    assert data['snap'] >= 0
    assert isinstance(data['lattice'], UMDLattice)


@hp.given(data=st.data(), ntypes=st.integers(1, 10))
def test_getUMDSnapshot(data, ntypes):
    """
    Test getUMDSnapshot generator function.

    """
    snapshot = data.draw(getUMDSnapshot(ntypes))
    assert isinstance(snapshot, UMDSnapshot)
    assert len(snapshot.position) == snapshot.natoms
    assert len(snapshot.velocity) == snapshot.natoms
    assert len(snapshot.force) == snapshot.natoms
