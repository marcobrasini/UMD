# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:24:26 2022

@author: marco
"""

from UMDLattice import UMDLattice


class UMDSimulation:
    """
    Class to collect the simulation parameters.

    A simulation correspond to the run of a single job.

    """

    def __init__(self, name='', cycle=-1, steps=0, steptime=0.0,
                 lattice=UMDLattice()):
        """
        Construct UMDSimulation object.

        Parameters
        ----------
        cycle : int, optional
            The cycle number of the simulation.
            The default is -1.
        snaps : int, optional
            The number of iterations in the simulation.
            The default is 0.
        snaptime : float, optional
            The time duration of each molecular dynamic iteration in fs.
            The default is 0.
        lattice : UMDLattice, optional
            The lattice over which the simulation is working.
            The default is UMDLattice().

        Returns
        -------
        UMDSimulation object.

        """
        self.name = name
        self.cycle = cycle
        self.steps = steps
        self.steptime = steptime
        self.lattice = lattice

    def time(self):
        """
        Calculate the total time of the simulation.

        The simulation time is calculated as the product of the constant
        time of each snapshot, 'snapTime', and the number of snapshots in the
        current simulation, Snaps.

        Returns
        -------
        time : float
            Simulation time in ps.

        """
        time = self.steps * self.steptime * 0.001
        return time

    def __eq__(self, other):
        """
        Overload of the == operator.

        Parameters
        ----------
        other : UMDSimulation object
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two simulations are identical, otherwise
            False.

        """
        eq = isinstance(other, UMDSimulation)
        eq *= (self.name == other.name)
        eq *= (self.cycle == other.cycle)
        eq *= (self.steps == other.steps)
        eq *= (self.steptime == other.steptime)
        eq *= (self.lattice == other.lattice)
        return eq

    def __str__(self):
        """
        Overload of the str function.

        Returns
        -------
        string : string
            Report of the simulation parameteres.

        """
        string = 'Simulation: ' + self.name + '\n'
        string += 'Total cycles = {:10}\n'.format(self.cycle)
        string += 'Total steps  = {:10}\n'.format(self.steps)
        string += 'Total time   = {:10.3f} ps'.format(self.time())
        return string
