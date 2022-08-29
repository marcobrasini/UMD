# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:28:41 2022

@author: marco
"""

import numpy as np
from .UMDLattice import UMDLattice
from .UMDSnapDynamics import UMDSnapDynamics
from .UMDSnapThermodynamics import UMDSnapThermodynamics


class UMDSnapshot(UMDSnapThermodynamics, UMDSnapDynamics):
    """
    Class UMDSnapshot to contain the data of a single MD simulation snapshot.

    The snapshot data are grouped in two categories:
        - Thermodynamic data (like volume, temperature, pressure, energy...)
        - Dynamic data (like atoms position, velocity, force)

    """

    def __init__(self, snap, lattice):
        """
        Construct a UMDSnapshot object.

        Parameters
        ----------
        snap : int
            The snapshot index.
        lattice : UMDLattice
            The lattice informations.

        Returns
        -------
        None.

        """
        self.snap = snap
        self.lattice = lattice
        self.natoms = lattice.natoms()
        UMDSnapThermodynamics.__init__(self)
        UMDSnapDynamics.__init__(self)

    def setThermodynamics(self, temperature=0.0, pressure=0.0, energy=0.0):
        """
        Initialize the thermodynamics parameters of the snapshot.

        Parameters
        ----------
        temperature : float, optional
            Snapshot temperature in K. The default is 0.0.
        pressure : TYPE, optional
            Snapshot pressure in GPa. The default is 0.0.
        energy : TYPE, optional
            Snapshot energy in eV. The default is 0.0.

        Returns
        -------
        None.

        """
        UMDSnapThermodynamics.__init__(self, temperature, pressure, energy)

    def setDynamics(self, time=0, position=[], velocity=[], force=[]):
        """
        Initialize the dynamics parameters of the snapshot.

        Parameters
        ----------
        time : float, optional
            Snapshot time duration in fs. The default is 0.
        position : array, optional
            Array of the atoms positions. The default is [].
        velocity : array, optional
            Array of the atoms velocities. The default is [].
        force : TYPE, optional
            Array of the atoms forces. The default is [].

        Returns
        -------
        None.

        """
        if len(position) != self.natoms:
            position = np.zeros((self.natoms, 3), dtype=float)
        if len(velocity) != self.natoms:
            velocity = np.zeros((self.natoms, 3), dtype=float)
        if len(force) != self.natoms:
            force = np.zeros((self.natoms, 3), dtype=float)
        UMDSnapDynamics.__init__(self, time, position, velocity, force)

    def __str__(self):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the UMDSnapshot information.

        """
        string  = "Snapshot: {:10}\n".format(self.snap)
        string += UMDSnapThermodynamics.__str__(self) + '\n'
        string += UMDSnapDynamics.__str__(self)
        return string

    def save(self, outfile):
        """
        Print on file the UMDSnapshot data.

        Parameters
        ----------
        outfile : output file
            The output file where to print the UMDSnapshot.

        Returns
        -------
        None.

        """
        outfile.write("Snapshot: " + str(self.snapStep) + '\n')
        UMDSnapThermodynamics.save(self, outfile)
        UMDSnapDynamics.save(self, outfile)
        outfile.write('\n')
