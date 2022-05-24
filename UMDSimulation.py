"""
===============================================================================
                                UMDSimulation
===============================================================================

This module provides the UMDSimulation class useful to collect molecular
dynamics simulation information. A molecular dynamics siulation can be obtained
by multiple simulation runs concatenated, and UMDSimulation objects contains
information of each single run and it is able to get cumulative information on
the number of iterations performed and the total amount of time simulated.

Classes
-------
    UMDSimulation

See Also
--------
    UMDLattice
    UMDSimulationRun

"""


from .UMDLattice import UMDLattice


class UMDSimulation:
    """
    UMDSimulation class to collect all the simulation parameters.

    A UMDSimulation object collects molecular dynamics simulation information.
    A molecular dynamics simulation can be obtained by multiple simulation run
    concatenated, and so it is defined by a UMDLattice object and list of
    UMDSimulationRun objects. The UMDSimulation objects contains information
    of each single run and it is able to get cumulative information on the
    number of iterations performed and the total amount of time simulated.

    Parameters
    ----------
    name : string
        The name of the simulation.
    lattice : UMDLattice
        A UMDLattice object representing the periodic lattice where the
        molecular dynamics simulation takes place.
    *runs : UMDSimulationRun
        A list of UMDSimulationRun objcts each one containing the parameters of
        a single simulation run.

    Methods
    -------
    __str__
        Convert a UMDSimulation objects into a string.
    save
        Print the UMDSimulation information on an output stream.
    steps
        Get the total number of iterations performed during the simulation.
    time
        Get the total amount of time simulated during the simulation.
    add
        Add a new UMDSimulationRun to the UMDSimulation.

    """

    def __init__(self, *runs, name='', lattice=UMDLattice()):
        """
        Construct a UMDSimulation object.

        Parameters
        ----------
        name : string
            The name of the simulation.
        lattice : UMDLattice
            A UMDLattice object representing the periodic lattice where the
            molecular dynamics simulation takes place.
        *runs : UMDSimulationRun
            A list of UMDSimulationRun objcts each one containing the
            parameters of a single simulation run.

        Returns
        -------
        UMDSimulation object.

        """
        self.name = name
        self.lattice = lattice
        self.runs = [*runs]

    def __eq__(self, other):
        eq = isinstance(other, UMDSimulation)
        eq *= (self.lattice == other.lattice)
        eq *= (self.runs == other.runs)
        return eq

    def __str__(self):
        """
        Convert a UMDSimulation objects into a string.

        Returns
        -------
        string : string
            A descriptive string reporting of the simulation parameteres.

        """
        string  = 'Simulation: {:30}\n'.format(self.name)
        string += '  Total cycles = {:12}\n'.format(len(self.runs))
        string += '  Total steps  = {:12}\n'.format(self.steps())
        string += '  Total time   = {:12.3f} fs'.format(self.time())
        return string

    def save(self, outfile):
        """
        Print the UMDSimulation information on an output stream.

        Parameters
        ----------
        outfile : output stream
            The output stream where to print the UMDSimulation.

        Returns
        -------
        None.

        """
        outfile.write(str(self)+'\n\n')
        outfile.write(str(self.lattice)+'\n\n')

    def cycle(self):
        """
        Get the total number of runs in the simulation.

        Returns
        -------
        cycle : float
            The total number of runs in the simulation.

        """
        cycle = len(self.runs)
        return cycle

    def steps(self):
        """
        Get the total number of iterations performed during the simulation.

        Returns
        -------
        steps : int
            The total number of iterations performed during the simulation.

        """
        steps = 0
        for run in self.runs:
            steps += run.steps
        return steps

    def time(self):
        """
        Get the total amount of time simulated during the simulation.

        Returns
        -------
        time : float
            The total amount of time simulated during the simulation.

        """
        time = 0
        for run in self.runs:
            time += run.time()
        return time

    def add(self, run):
        """
        Add a new UMDSimulationRun to the UMDSimulation.

        Parameters
        ----------
        run : UMDSimulationRun
            The new UMDSimulationRun object to add at the UMDSimulation.

        Raises
        ------
        AttributeError
            When rum.cycle if not consistent with the number of simulation runs
            already concatenated.

        Returns
        -------
        None.

        """
        errmsg = ("The next run cycle must be {}".format(self.cycle())
                  + " and not {}.".format(run.cycle))
        if self.cycle() == run.cycle:
            self.runs.append(run)
        else:
            raise AttributeError(errmsg)
