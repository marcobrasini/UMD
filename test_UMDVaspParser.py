# -*- coding: utf-8 -*-
"""
Created on Mon May 16 15:00:37 2022

@author: marco
"""
"""
To test UMDSimulation_from_outcar we use an examples of OUTCARfile:
 - the OUTCAR_mag,   /tests/mag5.70a1800T.outcar

The simulation saved in the OUTCAR file has the following structure:
 + the simulation is divided in three cycles:
     - cycle 0:  300 steps and 0.5 snap duration
     - cycle 1:  600 steps and 0.5 snap duration
     - cycle 2: 1000 steps and 0.4 snap duration
"""

from UMDVaspParser import UMDVaspParser

import numpy as np
import hypothesis as hp
from hypothesis import strategies as st 


testOUTCAR_nomag = 'tests/mag5.70a1800T.outcar'
testOUTCAR_mag = 'tests/mag5.70a1800T.outcar'
testOUTCAR_magpU = 'tests/mag5.70a1800T.outcar'


allSteptime = [0.5, 0.5, 0.4]
allSteps = [300, 600, 1000]
allTime = [0.150, 0.300, 0.400]


# %% UMDVaspParser tests for nSteps
def test_UMDVaspParser_nsteps_all():
    """
    Test UMDSimulation_from_outcar function when it reads all the snapshots
    from the OUTCAR file. The UMDVaspParser must return a UMDSimulation object
    whose steps attribute is equal to the sum of all the steps in each cycle
    and whose time attribute is equal to the cumulative time of each cycle.

    """
    simulation = UMDVaspParser(testOUTCAR_mag)
    assert simulation.steps == sum(allSteps)
    assert simulation.time == sum(allTime)


def test_UMDVaspParser_nsteps_cyc0(step0=106):
    """
    Test UMDSimulation_from_outcar function when it reads only a limited
    number of snapshots from the OUTCAR file, in the first cycle only. The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the number of steps set, and the time must be consistent with it.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, nsteps=step0)
    totSteps = step0
    totTime = step0*allSteptime[0]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


def test_UMDVaspParser_nsteps_cyc1(step1=412):
    """
    Test UMDSimulation_from_outcar function when it reads only a limited
    number of snapshots from the OUTCAR file, in the first two cycles. The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the number of steps set, and the time must be consistent with it.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, nsteps=step1)
    totSteps = step1
    totTime = sum(allTime[:1]) + (step1-sum(allSteps[:1]))*allSteptime[1]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


def test_UMDVaspParser_nsteps_cyc2(step2=1217):
    """
    Test UMDSimulation_from_outcar function when it reads only a limited
    number of snapshots from the OUTCAR file, in the all the three cycles.The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the number of steps set, and the time must be consistent with it.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, nsteps=step2)
    totSteps = step2
    totTime = sum(allTime[:2]) + (step2-sum(allSteps[:2]))*allSteptime[2]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


test_UMDVaspParser_nsteps_all()
test_UMDVaspParser_nsteps_cyc0()
test_UMDVaspParser_nsteps_cyc1()
test_UMDVaspParser_nsteps_cyc2()


# %% UMDVaspParser tests for initialStep
def test_UMDVaspParser_initial_cyc0(step0=106):
    """
    Test UMDSimulation_from_outcar function when it reads all the snapshots
    from the OUTCAR file after an initial step in the first cycle. The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the sum of all the steps in each cycle minus the number of steps
    skipped, and the time must be consistent with it as well.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, step0=step0)
    totSteps = sum(allSteps) - step0
    totTime = sum(allTime) - step0*allSteptime[0]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


def test_UMDVaspParser_initial_cyc1(step1=412):
    """
    Test UMDSimulation_from_outcar function when it reads all the snapshots
    from the OUTCAR file after an initial step in the second cycle. The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the sum of all the steps in each cycle minus the number of steps
    skipped, and the time must be consistent with it as well.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, step0=step1)
    totSteps = sum(allSteps) - step1
    totTime = sum(allTime[1:]) - (step1-sum(allSteps[:1]))*allSteptime[1]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


def test_UMDVaspParser_initial_cyc2(step2=1217):
    """
    Test UMDSimulation_from_outcar function when it reads all the snapshots
    from the OUTCAR file after an initial step in the third cycle. The
    UMDVaspParser must return a UMDSimulation object whose steps attribute is
    equal to the sum of all the steps in each cycle minus the number of steps
    skipped, and the time must be consistent with it as well.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, step0=step2)
    totSteps = sum(allSteps) - step2
    totTime = sum(allTime[2:]) - (step2-sum(allSteps[:2]))*allSteptime[2]/1000
    assert simulation.steps == totSteps
    assert np.isclose(simulation.time, totTime)


def test_UMDVaspParser_initial_over(step=1900):
    """
    Test UMDSimulation_from_outcar function when it skips all the snapshots
    from the OUTCAR file. The UMDVaspParser must return a UMDSimulation object
    whose steps attribute is zero as well as the time attribute.

    """
    simulation = UMDVaspParser(testOUTCAR_mag, step0=step)
    assert simulation.steps == 0
    assert np.isclose(simulation.time, 0.0)


test_UMDVaspParser_initial_cyc0()
test_UMDVaspParser_initial_cyc1()
test_UMDVaspParser_initial_cyc2()
test_UMDVaspParser_initial_over()
