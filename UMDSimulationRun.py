"""
===============================================================================
                               UMDSimulationRun
===============================================================================

This module provides the UMDSimulationRun class useful to collect information
about single molecular dynamics simulation runs. A total molecular dynamics
simulation (implemented by the UMDSimulation class) can be obtained by multiple
simulation runs concatenated. The UMDSimulationRun objects contain parameters
which characterize the single run and whose values are fixed for all the run,
like the number of iterations performed and the ionic relaxation time of each
iteration.

Classes
-------
    UMDSimulationRun

See Also
--------
    UMDSimulation

"""


class UMDSimulationRun:
    """
    UMDSimulationRun class to collect the single run simulation parameters.

    A UMDSimulationRun object collect molecular dynamics information related
    to a single run. A UMDSimulationRun objects is defined by some parameters
    which characterize the simulation run and whose values are fixed, like the
    number of iterations performed and the ionic relaxation time of each
    iteration.

    Parameters
    ----------
    cycle : int
        An index identifying the simulation run.
    steps : int
        The number of iterations performed during the simulation run.
    steptime : float
        The ionic relaxation time in fs.

    Methods
    -------
    __str__
        Convert a UMDSimulationRun objects into a string.
    time
        Get the total amount of time simulated by the simulation run.

    """

    def __init__(self, cycle=-1, steps=0, steptime=0.0):
        """
        Construct UMDSimulationRun object.

        Parameters
        ----------
        cycle : int, optional
            An index identifying the simulation run.
            The default is -1.
        steps : int, optional
            The number of iterations performed during the simulation run.
            The default is 0.
        steptime : float, optional
            The ionic relaxation time in fs.
            The default is 0.0.

        Returns
        -------
        UMDSimulation object.

        """
        self.cycle = cycle
        self.steps = steps
        self.steptime = steptime

    def __str__(self):
        """
        Convert a UMDSimulationRun objects into a string.

        Returns
        -------
        string : string
            A descriptive string reporting of the simulation run parameteres.

        """
        string  = 'Run {:8}:\n'.format(self.cycle)
        string += '  Steps     = {:8}\n'.format(self.steps)
        string += '  Step time = {:8.3f} (fs)'.format(self.steptime)
        return string

    def time(self):
        """
        Get the total amount of time simulated by the simulation run.

        Returns
        -------
        time : float
            The total amount of time simulated by the simulation run in fs.

        """
        time = self.steps * self.steptime
        return time
