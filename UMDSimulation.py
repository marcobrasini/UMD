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

    def __init__(self, name='', cycle=-1, snaps=0, snaptime=0.0,
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
        self.Cycle = cycle
        self.Snaps = snaps
        self.snapTime = snaptime
        self.Lattice = lattice

    def time(self):
        """
        Calculate the total time of the simulation.

        The simulation time is calculated as the product of the constant
        time of each snapshot, 'snapTime', and the number of snapshots in the
        current simulation, Snaps.

        Returns
        -------
        simtime : float
            Simulation time in ps.

        """
        simtime = self.Snaps * self.snapTime * 0.001
        return simtime

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
        eq = True
        eq = eq and (self.name == other.name)
        eq = eq and (self.Cycle == other.Cycle)
        eq = eq and (self.Snaps == other.Snaps)
        eq = eq and (self.snapTime == other.snapTime)
        eq = eq and (self.Lattice == other.Lattice)
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
        string += 'Total cycles = ' + str(self.Cycle) + '\n'
        string += 'Total steps = ' + str(self.Snaps) + '\n'
        string += 'Total time = ' + str(self.time()) + ' ps'
        return string
