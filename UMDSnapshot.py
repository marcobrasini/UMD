# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:28:41 2022

@author: marco
"""

import numpy as np
from UMDLattice import UMDLattice


class UMDSnapshot:
    """
    Class UMDSnapshot to contain the data of a single MD simulation snapshot.

    The snapshot data are grouped in two categories:
        - Thermodynamic data (like volume, temperature, pressure, energy...)
        - Dynamic data (like atoms position, velocity, force)

    """
    snaptime = 0.0 
    lattice = UMDLattice()
    natoms = 0

    @staticmethod
    def reset(snaptime=0.0, lattice=UMDLattice()):
        """
        Reset the static commmon values of the UMDSnapshot class.

        Parameters
        ----------
        snaptime : float, optional
            Snapshot time duration. The default is 0.0.
        lattice : UMDLattice, optional
            UMDLattice object. The default is UMDLattice().

        Returns
        -------
        None.

        """
        UMDSnapshot.snaptime = snaptime
        UMDSnapshot.lattice = lattice
        UMDSnapshot.natoms = lattice.natoms()

    def __init__(self, snapstep, snapThermodynamics, snapDynamics):
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
        self.snapStep = snapstep
        self.snapThermodynamics = snapThermodynamics
        self.snapDynamics = snapDynamics

    def __str__(self):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the UMDSnapshot information.

        """
        string  = "Snapshot: {:10}\n".format(self.snapStep)
        string += str(self.snapThermodynamics) + '\n'
        string += str(self.snapDynamics)
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
        self.snapThermodynamics.save(outfile)
        self.snapDynamics.save(outfile)
        outfile.write('\n')
