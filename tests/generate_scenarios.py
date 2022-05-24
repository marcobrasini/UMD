# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:48:33 2022

@author: marco
"""

import pytest
import hypothesis as hp
import hypothesis.strategies as st

from typing import Any, Dict
from dataclasses import dataclass


# %% Generate UMDAtom data scenarios for testing
@dataclass
class GenerateUMDAtom:
    Z: st.SearchStrategy[int]
    name: st.SearchStrategy[str]
    mass: st.SearchStrategy[float]
    valence: st.SearchStrategy[int]


settingUMDAtom = GenerateUMDAtom(
    Z=st.integers(min_value=1),
    name=st.from_regex(r'[A-Z][a-z]'),
    mass=st.floats(min_value=0.0, allow_nan=False, allow_infinity=False),
    valence=st.integers(min_value=0)
    )


@st.composite
def generateUMDAtom(draw, settings=settingUMDAtom) -> Dict[str, Any]:
    Z = draw(settings.Z)
    name = draw(settings.name)
    mass = draw(settings.mass)
    valence = draw(settings.valence)
    data = {"Z": Z, "name": name, "mass": mass, "valence": valence}
    return data


# %% Generate UMDLattice scenarios for testing


# %% Generate UMDSimulationRun data scenarios for testing
@dataclass
class GenerateUMDSimulationRun:
    cycle: st.SearchStrategy[int]
    steps: st.SearchStrategy[int]
    steptime: st.SearchStrategy[float]


settingUMDSimulationRun = GenerateUMDSimulationRun(
    cycle=st.integers(min_value=0, max_value=10000000),
    steps=st.integers(min_value=0, max_value=1000),
    steptime=st.floats(min_value=0.0, allow_nan=False, allow_infinity=False)
    )


@st.composite
def generateUMDSimulationRun(draw, settings=settingUMDSimulationRun):
    cycle = draw(settings.cycle)
    steps = draw(settings.steps)
    steptime = draw(settings.steptime)
    data = {"cycle": cycle, "steps": steps, "steptime": steptime}
    return data