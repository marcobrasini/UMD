"""
===============================================================================
                        UMDSimulation tests scenarios
===============================================================================

This module provides usefule scenarios to test the UMDSimulation class.

Classes
-------
    ScenariosUMDSimulation

Functions
---------
    dataUMDSimulation
    getUMDSimulation

See Also
--------
    test_UMDSimulation

"""

from ..libs.UMDSimulation import UMDSimulation

import hypothesis as hp
import hypothesis.strategies as st

from dataclasses import dataclass
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulationRun import UMDSimulationRun
from .test_scenarios_UMDLattice import getUMDLattice
from .test_scenarios_UMDSimulationRun import getUMDSimulationRun_list


@dataclass
class ScenariosUMDSimulation:
    name: st.SearchStrategy[str]
    lattice: st.SearchStrategy[UMDLattice]
    runs: st.SearchStrategy[list]


setUMDSimulation = ScenariosUMDSimulation(
    name=st.text(max_size=30),
    lattice=getUMDLattice(),
    runs=getUMDSimulationRun_list
    )


# %%
@st.composite
def dataUMDSimulation(draw, n=1):
    name = draw(setUMDSimulation.name)
    lattice = draw(setUMDSimulation.lattice)
    runs = draw(setUMDSimulation.runs(n))
    data = {'name': name, 'lattice': lattice, 'runs': runs}
    return data


@st.composite
def getUMDSimulation(draw, n=1):
    data = draw(dataUMDSimulation(n))
    simulation = UMDSimulation(**data)
    return simulation


# %% Strategies generator tests
@hp.given(data=st.data(), n=st.integers(0, 100))
def test_dataUMDSimulation(data, n):
    data = data.draw(dataUMDSimulation(n))
    assert isinstance(data['name'], str)
    assert isinstance(data['lattice'], UMDLattice)
    assert isinstance(data['runs'], list)
    for run in data['runs']:
        assert isinstance(run, UMDSimulationRun)


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_getUMDSimulation(data, n):
    simulation = data.draw(getUMDSimulation(n))
    assert isinstance(simulation, UMDSimulation)
