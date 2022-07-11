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
    getUMDSimulationRun_list

See Also
--------
    test_UMDSimulationRun
    test_scenarios_UMDSimulation

"""


from ..libs.UMDSimulationRun import UMDSimulationRun

import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass


@dataclass
class ScenariosUMDSimulationRun:
    cycle: st.SearchStrategy[int]
    steps: st.SearchStrategy[int]
    steptime: st.SearchStrategy[float]


setUMDSimulationRun = ScenariosUMDSimulationRun(
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


@st.composite
def getUMDSimulationRun_list(draw, n=1):
    """
    Strategy to generate a list of n UMDSimulationRun objects.

    """
    runs = draw(st.lists(getUMDSimulationRun(), min_size=n, max_size=n))
    for i in range(n):
        runs[i].cycle = i
    return runs


# %% Strategies generator tests
@hp.given(st.data())
def test_dataUMDSimulationRun(data):
    """
    Test dataUMDSimulationRun generator function.
    
    """
    data = data.draw(dataUMDSimulationRun())
    assert isinstance(data['cycle'], int)
    assert data['cycle'] >= 0
    assert isinstance(data['steps'], int)
    assert data['steps'] >= 0
    assert isinstance(data['steptime'], float)
    assert data['steptime'] >= 0


@hp.given(st.data())
def test_getUMDSimulationRun(data):
    """
    Test getUMDSimulationRun generator function.
    
    """
    run = data.draw(getUMDSimulationRun())
    assert isinstance(run, UMDSimulationRun)


@hp.given(data=st.data(), n=st.integers(1, 100))
def test_getUMDSimulationRun_list(data, n):
    """
    Test getUMDSimulationRun_listt generator function.
    
    """
    runs = data.draw(getUMDSimulationRun_list(n))
    assert len(runs) == n
    for i in range(n):
        assert isinstance(runs[i], UMDSimulationRun)
        assert runs[i].cycle == i
    