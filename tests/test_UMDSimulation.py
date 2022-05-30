"""
===============================================================================
                            UMDSimulation class tests                              
===============================================================================
"""

from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun
from ..libs.UMDLattice import UMDLattice

import pytest
import hypothesis as hp
import hypothesis.strategies as st

from .test_scenarios_UMDSimulation import dataUMDSimulation, getUMDSimulation
from .test_scenarios_UMDSimulationRun import getUMDSimulationRun


# %% UMDSimulation unit tests
class TestUMDSimulation:
    """
    The unit tests implemented test an instance of the UMDSimulation class
    given by two simulation runs. The runs characteristics are:
        - run cycle=0, steps=1000 and steptime=0.5 fs (500 fs in total).
        - run cycle=1, steps=2000 and steptime=0.4 fs (800 fs in total).
    So the total number of iterations performed in the simulation is 3000 steps
    and the amount of time simulated is 1300 fs.
    """

    name = "SimulationName"
    lattice = UMDLattice(atoms={'X': 1})
    run0 = UMDSimulationRun(0, 1000, 0.5)
    run1 = UMDSimulationRun(1, 2000, 0.4)

    # %% UMDSimulation __init__ function tests
    def test_UMDSimulation_init_no_run(self):
        """
        Test the __init__ function default constructor.

        """
        simulation = UMDSimulation()
        assert simulation.name == ""
        assert simulation.lattice == UMDLattice()
        assert simulation.runs == []

    def test_UMDSimulation_init(self):
        """
        Test the __init__ constructor assignement operations.

        """
        simulation = UMDSimulation(name=self.name, lattice=self.lattice,
                                   runs=[self.run0, self.run1])
        assert simulation.name == self.name
        assert simulation.lattice == self.lattice
        assert simulation.runs[0] == self.run0
        assert simulation.runs[1] == self.run1

    # %% UMDSimulation __eq__ function tests
    def test_UMDSimulation_eq_true(self):
        """
        Test the __eq__ function to compare two UMDSimulation objects refering
        to the same simulation. The value returned must be True.

        """
        simulation1 = UMDSimulation(name=self.name, lattice=self.lattice,
                                   runs=[self.run0, self.run1])
        simulation2 = UMDSimulation(name=self.name, lattice=self.lattice,
                                   runs=[self.run0, self.run1])
        assert simulation1 == simulation2

    def test_UMDSimulation_eq_false_lattice(self):
        """
        Test the __eq__ function to compare two UMDSimulation objects refering
        to simulation on different lattices. The value returned must be False.

        """
        simulation1 = UMDSimulation(lattice=self.lattice, runs=[self.run0])
        simulation2 = UMDSimulation(lattice=UMDLattice(), runs=[self.run0])
        assert not simulation1 == simulation2

    def test_UMDSimulation_eq_false_run_type(self):
        """
        Test the __eq__ function to compare two UMDSimulation objects refering
        to simulation with different runs. The value returned must be False.

        """
        simulation1 = UMDSimulation(runs=[self.run0])
        simulation2 = UMDSimulation(runs=[self.run1])
        assert not simulation1 == simulation2

    def test_UMDSimulation_eq_false_run_number(self):
        """
        Test the __eq__ function to compare two UMDSimulation objects refering
        to simulation with different cycles. The value returned must be False.

        """
        simulation1 = UMDSimulation(runs=[self.run0, self.run1])
        simulation2 = UMDSimulation(runs=[self.run1])
        assert not simulation1 == simulation2

    # %% UMDSimulation __str__ function tests
    def test_UMDSimulation_str(self):
        """
        Test the __str__ function to convert the UMDSimulation information into
        a descriptive and printable string object.

        """
        string  = 'Simulation: SimulationName                \n'
        string += '  Total cycles =            2\n'
        string += '  Total steps  =         3000\n'
        string += '  Total time   =     1300.000 fs'
        simulation = UMDSimulation(name=self.name, lattice=self.lattice,
                                   runs=[self.run0, self.run1])
        assert str(simulation) == string

    def test_UMDSimulation_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.

        """
        stringlength = 43+30+30+32
        simulation = UMDSimulation(name=self.name, lattice=self.lattice,
                                   runs=[self.run0, self.run1])
        assert len(str(simulation)) == stringlength

    # %% UMDSimulation cycle function tests
    def test_UMDSimulation_cycle(self):
        """
        Test the cycle function. The value returned must be equal to the number
        of runs concatenated.

        """
        simulation = UMDSimulation(runs=[self.run0, self.run1])
        assert simulation.cycle() == 2

    # %% UMDSimulation steps function tests
    def test_UMDSimulation_steps(self):
        """
        Test the steps function. The value returned must be equal to the sum of
        all the number of iterations performed during each simulation run.

        """
        simulation = UMDSimulation(runs=[self.run0, self.run1])
        assert simulation.steps() == 3000

    # %% UMDSimulation time function tests
    def test_UMDSimulation_time(self):
        """
        Test the time function. The value returned must be equal to the sum of
        all the amounts of time simulated during each simulation run.

        """
        simulation = UMDSimulation(runs=[self.run0, self.run1])
        assert simulation.time() == 1300.00

    # %% UMDSimulation add function tests
    def test_UMDSimulation_add(self):
        """
        Test the add function when a new good UMDSimulation run is added. The
        updated UMDSimulation object must contain the new run in the last
        position of the 'runs' list and the number of cycles must have been
        increased by one.

        """
        simulation = UMDSimulation(lattice=self.lattice, runs=[self.run0])
        simulation.add(self.run1)
        assert simulation.cycle() == 2
        assert simulation.runs[-1] == self.run1

    def test_UMDSimulation_add_error(self):
        """
        Test the add function when a new bad UMDSimulation run is added. The
        add function must raise an AttributeError.

        """
        simulation = UMDSimulation(lattice=self.lattice, runs=[self.run0])
        with pytest.raises(AttributeError):
            self.simulation.add(self.run0)


# %% ===================================================================== %% #
# %% UMDSimulation hypothesis tests
@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_init(data, n):
    """
    Test __init__ function assignement operations.

    """
    data = data.draw(dataUMDSimulation(n))
    simulation = UMDSimulation(**data)
    assert simulation.name == data['name']
    assert simulation.lattice == data['lattice']
    assert simulation.runs == data['runs']


@hp.given(data1=st.data(), data2=st.data(),
          n1=st.integers(0, 100), n2=st.integers(0, 100))
def test_UMDSimulation_eq(data1, data2, n1, n2):
    """
    Test the __eq__ function.

    """
    data1 = data1.draw(dataUMDSimulation(n1))
    data2 = data2.draw(dataUMDSimulation(n2))
    equal = (data1['lattice'] == data2['lattice']
             and data1['runs'] == data2['runs'])
    simulation1 = UMDSimulation(**data1)
    simulation2 = UMDSimulation(**data2)
    assert (simulation1 == simulation2) == equal


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_str_length(data, n):
    """
    Test the __str__ function. The length of the returned string is constant.

    """
    simulation = data.draw(getUMDSimulation(n))
    assert len(str(simulation)) == 135


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_cycle(data, n):
    """
    Test the cycle function.

    """
    simulation = data.draw(getUMDSimulation(n))
    assert simulation.cycle() == n


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_steps(data, n):
    """
    Test the steps function.

    """
    data = data.draw(dataUMDSimulation(n))
    simulation = UMDSimulation(**data)
    steps = 0
    for run in data['runs']:
        steps += run.steps
    assert simulation.steps() == steps


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_time(data, n):
    """
    Test the time function.

    """
    data = data.draw(dataUMDSimulation(n))
    simulation = UMDSimulation(**data)
    time = 0
    for run in data['runs']:
        time += run.time()
    assert simulation.time() == time


@hp.given(data=st.data(), n=st.integers(0, 100))
def test_UMDSimulation_add(data, n):
    """
    Test the add function.

    """
    simulation = data.draw(getUMDSimulation(n))
    run = data.draw(getUMDSimulationRun())
    if run.cycle == n:
        simulation.add(run)
        assert simulation.runs[-1] == run
    else:
        with pytest.raises(AttributeError):
            simulation.add(run)
