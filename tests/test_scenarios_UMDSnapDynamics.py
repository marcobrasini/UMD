"""
===============================================================================
                        UMDSnapDynamics tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDSnapDynamics class and
its derivatives, like UMDSnapshot.

Classes
-------
    ScenariosUMDSnapDynamics

Functions
---------
    dataUMDSnapDynamics
    getUMDSnapDynamics

See Also
--------
    test_UMDSnapDynamics

"""


from ..libs.UMDSnapDynamics import UMDSnapDynamics

import numpy as np
import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass
from .test_scenarios import getNumpyArray


@dataclass
class ScenariosUMDSnapDynamics:
    time: st.SearchStrategy[float]
    position: st.SearchStrategy[list]
    velocity: st.SearchStrategy[list]
    force: st.SearchStrategy[list]


setUMDSnapDynamics = ScenariosUMDSnapDynamics(
    time=st.floats(min_value=0.0, max_value=1000.0, allow_nan=False,
                   allow_infinity=False),
    position=getNumpyArray,
    velocity=getNumpyArray,
    force=getNumpyArray
    )


# %% Strategies generator functions
@st.composite
def dataUMDSnapDynamics(draw, natoms=1):
    """
    Strategy to generate input data of a UMDSnapDynamics object.

    """
    time = draw(setUMDSnapDynamics.time)
    position = draw(setUMDSnapDynamics.position(natoms, 3))
    velocity = draw(setUMDSnapDynamics.velocity(natoms, 3))
    force = draw(setUMDSnapDynamics.force(natoms, 3))
    data = {"time": time, "position": position, "velocity": velocity,
            "force": force}
    return data


@st.composite
def getUMDSnapDynamics(draw, natoms=1):
    """
    Strategy to generate input data of a UMDSnapDynamics object.

    """
    data = draw(dataUMDSnapDynamics(natoms))
    snapdynamics = UMDSnapDynamics(**data)
    return snapdynamics


# %% Strategies generator tests
@hp.given(data=st.data(), natoms=st.integers(min_value=1, max_value=30))
def test_dataUMDSnapDynamics(data, natoms):
    """
    Test dataUMDSnapDynamics generator function.

    """
    data = data.draw(dataUMDSnapDynamics(natoms))
    assert isinstance(data['time'], float)
    assert data['time'] >= 0
    assert isinstance(data['position'], type(np.array([])))
    assert data['position'].shape == (natoms, 3)
    assert isinstance(data['velocity'], type(np.array([])))
    assert data['velocity'].shape == (natoms, 3)
    assert isinstance(data['force'], type(np.array([])))
    assert data['force'].shape == (natoms, 3)


@hp.given(data=st.data(), natoms=st.integers(min_value=1, max_value=30))
def test_getUMDSnapDynamics(data, natoms):
    """
    Test getUMDSnapDynamics generator function.

    """
    snapdynamics = data.draw(getUMDSnapDynamics(natoms))
    assert isinstance(snapdynamics, UMDSnapDynamics)
