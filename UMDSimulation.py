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


from UMDLattice import UMDLattice
from UMDSimulationRun import UMDSimulationRun


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

    def __init__(self, name, lattice: UMDLattice, *runs: UMDSimulationRun):
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
        self.runs = [runs]

    def __str__(self):
        """
        Convert a UMDSimulation objects into a string.

        Returns
        -------
        string : string
            A descriptive string reporting of the simulation parameteres.

        """
        string  = 'Simulation: {:30}\n'.format(self.name)
        string += 'Total cycles = {:10}\n'.format(len(self.runs))
        string += 'Total steps  = {:10}\n'.format(self.steps())
        string += 'Total time   = {:10.4f} fs'.format(self.time())
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
            the total amount of time simulated during the simulation.

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

        Returns
        -------
        None.

        """
        self.runs.append(run)
