"""
===============================================================================
                        UMDSimulationRun class tests                              
===============================================================================
"""

from ..UMDSimulationRun import UMDSimulationRun


import pytest
import hypothesis as hp
import hypothesis.strategies as st

from .generate_scenarios import generateUMDSimulationRun


# %% UMDSimulationRun unit tests
class TestUMDSimulationRun_unit:

    cycle = 3
    steps = 12000
    steptime = 0.45
    run = UMDSimulationRun(cycle, steps, steptime)

    # %% UMDSimulationRun __init__ function tests
    def test_UMDSimulationRun_init_default(self):
        """
        Test the __init__ function defualt constructor.

        """
        run = UMDSimulationRun()
        assert run.cycle == -1
        assert run.steps == 0
        assert run.steptime == 0.0

    def test_UMDSimulationRun_init_assignement(self):
        """
        Test the __init__ function assignement operations.

        """
        assert self.run.cycle == self.cycle
        assert self.run.steps == self.steps
        assert self.run.steptime == self.steptime

    # %% UMDSimulationRun __str__ function tests
    def test_UMDSimulationRun_str(self):
        """
        Test the __str__ function to convert the UMDSimulationRun information
        into a descriptive and printable string object.

        """
        string  = "Run        3:\n"
        string += "  Steps     =    12000\n"
        string += "  Step time =    0.450 (fs)"
        assert str(self.run) == string

    def test_UMDSimulationRun_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        
        """
        stringlength = 14+23+27
        assert len(str(self.run)) == stringlength
    
    # %% UMDSimulationRun time function tests
    def test_UMDSimulationRun_time(self):
        time = self.steps*self.steptime
        assert self.run.time() == time


# %% ===================================================================== %% #
# %% UMDSimulationRun hypothesis tests
@hp.given(st.data())
def test_UMDSimulationRun_init_assignement(data):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(generateUMDSimulationRun())
    run = UMDSimulationRun(**data)
    assert run.cycle == data["cycle"]
    assert run.steps == data["steps"]
    assert run.steptime == data["steptime"]


@hp.given(st.data())
def test_UMDSimulationRun_time(data):
    """
    Test the UMDSimulationRun time function. The simulated time returned must
    be equal to the product of the number of iterations, 'steps', and the ionic
    relaxation time of each iteration, 'steptime'.

    """
    data = data.draw(generateUMDSimulationRun())
    run = UMDSimulationRun(**data)
    assert run.time() == data["steps"]*data["steptime"]
