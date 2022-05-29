"""
===============================================================================
                        UMDSimulationRun tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDSimulationRun class and
its derivatives, like UMDSimulation.

Classes
-------
    ScenariosUMDSimulationRun

Functions
---------
    dataUMDSimulationRun
    getUMDSimulationRun

See Also
--------
    test_UMDSimulationRun

"""


from ..libs.UMDSimulationRun import UMDSimulationRun

import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass


@dataclass
class GenerateUMDSimulationRun:
    cycle: st.SearchStrategy[int]
    steps: st.SearchStrategy[int]
    steptime: st.SearchStrategy[float]


setUMDSimulationRun = GenerateUMDSimulationRun(
    cycle=st.integers(min_value=0, max_value=100),
    steps=st.integers(min_value=0, max_value=100000),
    steptime=st.floats(min_value=0.0, max_value=10.0,
                       allow_nan=False, allow_infinity=False)
    )


# %% Strategies generator functions
@st.composite
def dataUMDSimulationRun(draw):
    """
    Strategy to generate input data of a UMDSimulationRun object.

    """
    cycle = draw(setUMDSimulationRun.cycle)
    steps = draw(setUMDSimulationRun.steps)
    steptime = draw(setUMDSimulationRun.steptime)
    data = {"cycle": cycle, "steps": steps, "steptime": steptime}
    return data


@st.composite
def getUMDSimulationRun(draw):
    """
    Strategy to generate a UMDSimulationRun object.

    """
    data = draw(dataUMDSimulationRun())
    run = UMDSimulationRun(**data)
    return run


# %% Strategies generator tests
@hp.given(st.data())
def test_dataUMDSimulationRun(data):
    data = data.draw(dataUMDSimulationRun())
    assert isinstance(data['cycle'], int)
    assert data['cycle'] >= 0
    assert isinstance(data['steps'], int)
    assert data['steps'] >= 0
    assert isinstance(data['steptime'], float)
    assert data['steptime'] >= 0


@hp.given(st.data())
def test_getUMDSimulationRun(data):
    run = data.draw(getUMDSimulationRun())
    assert isinstance(run, UMDSimulationRun)
