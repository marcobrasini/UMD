"""
===============================================================================
                            UMDSimulation class tests                              
===============================================================================
"""

from ..UMDSimulation import UMDSimulation
from ..UMDSimulationRun import UMDSimulationRun
from ..UMDLattice import UMDLattice

import pytest


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

    name = ""
    lattice = UMDLattice()
    run0 = UMDSimulationRun(0, 1000, 0.5)
    run1 = UMDSimulationRun(1, 2000, 0.4)

    # %% UMDSimulation __init__ function tests
    def test_UMDSimulation_init_norun(self):
        """
        Test the __init__ function default constructor.

        """
        simulation = UMDSimulation(name=self.name, lattice=self.lattice)
        assert simulation.name == self.name
        assert simulation.lattice == self.lattice
        assert simulation.runs == []

    def test_UMDSimulation_init(self):
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert simulation.name == self.name
        assert simulation.lattice == self.lattice
        assert simulation.runs[0] == self.run0
        assert simulation.runs[1] == self.run1

    # %% UMDSimulation __str__ function tests
    def test_UMDSimulation_str(self):
        """
        Test the __str__ function to convert the UMDSimulation information into
        a descriptive and printable string object.

        """
        string  = 'Simulation:                               \n'
        string += '  Total cycles =            2\n'
        string += '  Total steps  =         3000\n'
        string += '  Total time   =     1300.000 fs'
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert str(simulation) == string

    def test_UMDSimulation_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.

        """
        stringlength = 43+30+30+32
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert len(str(simulation)) == stringlength

    # %% UMDSimulation cycle function tests
    def test_UMDSimulation_cycle(self):
        """
        Test the cycle function. The value returned must be equal to the number
        of runs concatenated.

        """
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert simulation.cycle() == 2

    # %% UMDSimulation steps function tests
    def test_UMDSimulation_steps(self):
        """
        Test the steps function. The value returned must be equal to the sum of
        all the number of iterations performed during each simulation run.

        """
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert simulation.steps() == 3000

    # %% UMDSimulation time function tests
    def test_UMDSimulation_time(self):
        """
        Test the time function. The value returned must be equal to the sum of
        all the amounts of time simulated during each simulation run.

        """
        simulation = UMDSimulation(self.name, self.lattice, self.run0, self.run1)
        assert simulation.time() == 1300.00

    # %% UMDSimulation time function tests
    def test_UMDSimulation_add(self):
        """
        Test the add function when a new good UMDSimulation run is added. The
        updated UMDSimulation object must contain the new run in the last
        position of the 'runs' list and the number of cycles must have been
        increased by one.

        """
        simulation = UMDSimulation(self.name, self.lattice, self.run0)
        simulation.add(self.run1)
        assert simulation.cycle() == 2
        assert simulation.runs[-1] == self.run1

    def test_UMDSimulation_add_error(self):
        """
        Test the add function when a new bad UMDSimulation run is added. The
        add function must raise an AttributeError.

        """
        simulation = UMDSimulation(self.name, self.lattice, self.run0)
        with pytest.raises(AttributeError):
            self.simulation.add(self.run0)
