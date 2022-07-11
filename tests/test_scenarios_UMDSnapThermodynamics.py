"""
===============================================================================
                      UMDSnapThermodynamics tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDSnapThermodynamics class
and its derivatives, like UMDSnapshot.

Classes
-------
    ScenariosUMDSnapThermodynamics

Functions
---------
    dataUMDSnapThermodynamics
    getUMDSnapThermodynamics

See Also
--------
    test_dataUMDSnapThermodynamics
    test_getUMDSnapThermodynamics

"""


from ..libs.UMDSnapThermodynamics import UMDSnapThermodynamics

import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass


@dataclass
class ScenariosUMDSnapThermodynamics:
    temperature: st.SearchStrategy[float]
    pressure: st.SearchStrategy[float]
    energy: st.SearchStrategy[float]


setUMDSnapThermodynamics = ScenariosUMDSnapThermodynamics(
    temperature=st.floats(min_value=0.0, max_value=1e6, allow_nan=False,
                          allow_infinity=False),
    pressure=st.floats(min_value=0.0, max_value=1e6, allow_nan=False,
                       allow_infinity=False),
    energy=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False,
                     allow_infinity=False)
    )


# %% Strategies generator functions
@st.composite
def dataUMDSnapThermodynamics(draw):
    """
    Strategy to generate input data of a UMDSnapThermodynamics object.

    """
    temperature = draw(setUMDSnapThermodynamics.temperature)
    pressure = draw(setUMDSnapThermodynamics.pressure)
    energy = draw(setUMDSnapThermodynamics.energy)
    data = {"temperature": temperature, "pressure": pressure, "energy": energy}
    return data


@st.composite
def getUMDSnapThermodynamics(draw):
    """
    Strategy to generate a UMDSnapThermodynamics object.

    """
    data = draw(dataUMDSnapThermodynamics())
    snapthermodynamics = UMDSnapThermodynamics(**data)
    return snapthermodynamics


# %% Strategies generator tests
@hp.given(st.data())
def test_dataUMDSnapThermodynamics(data):
    """
    Test dataUMDSnapThermodynamics generator function.

    """
    data = data.draw(dataUMDSnapThermodynamics())
    assert isinstance(data['temperature'], float)
    assert data['temperature'] >= 0
    assert isinstance(data['pressure'], float)
    assert data['pressure'] >= 0
    assert isinstance(data['energy'], float)


@hp.given(st.data())
def test_getUMDSnapThermodynamics(data):
    """
    Test getUMDSnapThermodynamics generator function.

    """
    snapthermodynamics = data.draw(getUMDSnapThermodynamics())
    assert isinstance(snapthermodynamics, UMDSnapThermodynamics)
