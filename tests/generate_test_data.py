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
