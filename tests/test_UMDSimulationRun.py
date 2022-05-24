"""
===============================================================================
                        UMDSimulationRun class tests                              
===============================================================================
"""

from ..libs.UMDSimulationRun import UMDSimulationRun


import pytest
import hypothesis as hp
import hypothesis.strategies as st

from .generate_scenarios import generateUMDSimulationRun


# %% UMDSimulationRun unit tests
class TestUMDSimulationRun_unit:
    """
    The unit tests implemented test an instance of the UMDSimulationRun class
    representing a simulation run with the following characteristic:
        - run : cycle=3, steps=12000 and steptime=0.45 fs (5400 fs in total)
    
    """

    cycle = 3
    steps = 12000
    steptime = 0.45

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
        run = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        assert run.cycle == self.cycle
        assert run.steps == self.steps
        assert run.steptime == self.steptime

    # %% UMDSimulationRun __eq__ function tests
    def test_UMDSimulationRun_eq_true(self):
        """
        Test the __eq__ function to compare two UMDSimulationRun objects
        refering to the same simulation run. The value returned must be True.

        """
        run1 = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        run2 = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        assert run1 == run2
    
    def test_UMDSimulationRun_eq_false_cycle(self):
        """
        Test the __eq__ function to compare two UMDSimulationRun objects
        refering to different simulations run cycles. The value returned must
        be False.

        """
        run1 = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        run2 = UMDSimulationRun(self.cycle+1, self.steps, self.steptime)
        assert not run1 == run2
    
    def test_UMDSimulationRun_eq_false_steps(self):
        """
        Test the __eq__ function to compare two UMDSimulationRun objects
        refering to simulations run with different steps. The value returned
        must be False.

        """
        run1 = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        run2 = UMDSimulationRun(self.cycle, self.steps+1, self.steptime)
        assert not run1 == run2
    
    def test_UMDSimulationRun_eq_false_steptime(self):
        """
        Test the __eq__ function to compare two UMDSimulationRun objects
        refering to simulations run with different steptime. The value returned
        must be False.

        """
        run1 = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        run2 = UMDSimulationRun(self.cycle, self.steps, self.steptime+1.0)
        assert not run1 == run2
        
    # %% UMDSimulationRun __str__ function tests
    def test_UMDSimulationRun_str(self):
        """
        Test the __str__ function to convert the UMDSimulationRun information
        into a descriptive and printable string object.

        """
        string  = "Run        3:\n"
        string += "  Steps     =    12000\n"
        string += "  Step time =    0.450 (fs)"
        run = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        assert str(run) == string

    def test_UMDSimulationRun_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.

        """
        stringlength = 14+23+27
        run = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        assert len(str(run)) == stringlength

    # %% UMDSimulationRun time function tests
    def test_UMDSimulationRun_time(self):
        time = self.steps*self.steptime
        run = UMDSimulationRun(self.cycle, self.steps, self.steptime)
        assert run.time() == time


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


@hp.given(data1=st.data(), data2=st.data())
def test_UMDSimulationRun_eq(data1, data2):
    """
    Test the UMDSimulationRun __eq__ function. The value returned must be True
    if the two simulation are the same, otherwise False.

    """
    data1 = data1.draw(generateUMDSimulationRun())
    data2 = data2.draw(generateUMDSimulationRun())
    run1 = UMDSimulationRun(**data1)
    run2 = UMDSimulationRun(**data2)
    assert (run1 == run2) == (data1 == data2)


@hp.given(st.data())
def test_UMDSimulationRun_str_length(data):
    """
    Test the UMDSimulationRun str function. The string returned must have a
    length of exactly 64 characters.

    """
    stringlength = 64
    data = data.draw(generateUMDSimulationRun())
    run = UMDSimulationRun(**data)
    assert len(str(run)) == stringlength


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
