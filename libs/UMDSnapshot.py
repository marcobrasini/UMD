# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:28:41 2022

@author: marco
"""

import numpy as np
from .UMDLattice import UMDLattice
from .UMDSnapDynamics import UMDSnapDynamics
from .UMDSnapThermodynamics import UMDSnapThermodynamics


class UMDSnapshot(SnapThermodynamics, SnapDynamics):
    """
    Class UMDSnapshot to contain the data of a single MD simulation snapshot.

    The snapshot data are grouped in two categories:
        - Thermodynamic data (like volume, temperature, pressure, energy...)
        - Dynamic data (like atoms position, velocity, force)

    """

    def __init__(self, snap, lattice):
        """
        Construct the UMDSnapshot object.

        Parameters
        ----------
        snapstep : int
            Snapshot index.
        snapThermodynamics : UMDSnapThermodynamics
            A UMDSnapThermodynamics object with the thermodynamics quantities.
        snapDynamics : UMDSnapDynamics
            A UMDSnapDynamics object with the dynamics quantities.

        Returns
        -------
        UMDSnapshot object.

        """
        self.snap = snap
        self.lattice = lattice
        self.natoms = lattice.natoms()
        UMDSnapThermodynamics.__init__(self)
        UMDSnapDynamics.__init__(self, self.natoms)

    def setThermodynamics(self, temperature=0.0, pressure=0.0, energy=0.0):
        UMDSnapThermodynamics.__init__(self, temperature, pressure, energy)

    def setDynamics(self, time=0, position=[], velocity=[], force=[]):
        if len(position) != self.natom:
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
        """"
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
