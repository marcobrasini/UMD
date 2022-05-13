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

    def __init__(self, name='', lattice=UMDLattice(), cycle=-1, steps=0,
                 steptime=0.0, time=0.0):
        """
        Construct UMDSimulation object.

        Parameters
        ----------
        lattice : UMDLattice, optional
            The lattice over which the simulation is working.
            The default is UMDLattice().
        cycle : int, optional
            The cycle number of the simulation.
            The default is -1.
        snaps : int, optional
            The number of iterations in the simulation.
            The default is 0.
        snaptime : float, optional
            The time duration of each molecular dynamic iteration in fs.
            The default is 0.
        time : float, optional
            The time accumulated during all the simulation.
            The default is 0

        Returns
        -------
        UMDSimulation object.

        """
        self.name = name
        self.lattice = lattice
        self.cycle = cycle
        self.steps = steps
        self.steptime = steptime
        self.time = time

    def simtime(self):
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
        time = self.time
        if time == 0.0:
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
        eq *= (self.time) == other.time
        return eq

    def __str__(self):
        """
        Overload of the str function.

        Returns
        -------
        string : string
            Report of the simulation parameteres.

        """
        string  = 'Simulation: {:30}\n'.format(self.name)
        string += 'Total cycles = {:10}\n'.format(self.cycle)
        string += 'Total steps  = {:10}\n'.format(self.steps)
        string += 'Total time   = {:10.4f} ps'.format(self.simtime())
        return string

    def save(self, outfile):
        """
        Print on file the UMDSimulation data.

        Parameters
        ----------
        outfile : output file
            The output file where to print the UMDSimulation.

        Returns
        -------
        None.

        """
        outfile.write(str(self)+'\n\n')
