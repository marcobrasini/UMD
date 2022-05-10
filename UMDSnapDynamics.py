# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:40:28 2022

@author: marco
"""

import numpy as np
from UMDLattice import UMDLattice


class UMDSnapDynamics:
    """
    Class UMDSnapDynamics to contain the dynamic data of a single molecular
    dynamics simulation snapshot.

    """

    def __init__(self, snaptime=0.0, lattice=UMDLattice(),
                 position=[], displacement=[], velocity=[], force=[]):
        """
        Construct the UMDSnapDynamics object.

        Parameters
        ----------
        snaptime : float, optional
            Time duration of the snapshot. The default is 0.0.
        lattice : UMDLattice, optional
            Lattice reference of the snapshot. The default is UMDLattice().
        position : array, optional
            Array of all the atoms positions. The default is [].
        displacement : array, optional
            Array of all the atoms displacements. The default is [].
        velocity : array, optional
            Array of all the atoms velocities. The default is [].
        force : array, optional
            Array of all the atoms forces. The default is [].

        Returns
        -------
        UMDSnapDynamics object.

        """
        # We default initialize the attributes.
        self.snaptime = snaptime
        self.lattice = lattice
        self.natoms = lattice.natoms()
        self.position = np.zeros((self.natoms, 3), dtype=float)
        self.displacement = np.zeros((self.natoms, 3), dtype=float)
        self.velocity = np.zeros((self.natoms, 3), dtype=float)
        self.force = np.zeros((self.natoms, 3), dtype=float)
        # If position, displacement, velocity, force are given and are correct,
        # then the corresponding attibutes are set equal to them.
        if len(position) == self.natoms:
            self.position = position
        if len(displacement) == self.natoms:
            self.displacement = displacement
        if len(velocity) == self.natoms:
            self.velocity = velocity
        if len(force) == self.natoms:
            self.force = force

    def get_displacement(self, position0):
        """
        Calculate the atom displacement with respect to some initial positions.

        Parameters
        ----------
        position0 : array
            Initial atoms positions took as reference.

        Returns
        -------
        displacement : array
            Array of all the atoms displacements.

        """
        self.displacement = self.position - position0
        reduced_displacement = self.lattice.reduced(self.displacement)
        for i in range(3):
            delta = reduced_displacement[:, i]
            delta = np.where(delta > +0.5, delta-1, delta)
            delta = np.where(delta < -0.5, delta+1, delta)
            reduced_displacement[:, i] = delta
        self.displacement = self.lattice.cartesian(reduced_displacement)
        displacement = self.displacement
        return displacement

    def velocity(self):
        """
        Calculate the atom velocity from the atom displacement.

        Returns
        -------
        velocity : array
            Array of all the atoms velocities.

        """
        self.velocity = self.displacement/self.snaptime
        velocity = self.velocity
        return velocity

    def __str__(self, w=12, f=6):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the atoms dynamical vectors.

        """
        dynamics = np.hstack((self.position, self.velocity, self.force))
        headerstyle = '{:'+str(3*w)+'}{:'+str(3*w)+'}{:'+str(3*w)+'}'
        string = headerstyle.format('Positions', 'Velocities', 'Forces')
        style = '{:'+str(w-1)+'.'+str(f)+'f}'
        for atom in dynamics:
            string += '\n ' + ' '.join([style.format(x) for x in atom])
        return string

    def save(self, outfile):
        """
        Print on file the UMDSnapDynamics data.

        Parameters
        ----------
        outfile : output file
            The output file where to print the UMDSnapDynamics.

        Returns
        -------
        None.

        """
        dynamics = np.hstack((self.position, self.velocity, self.force))
        np.savetxt(outfile, dynamics, fmt='%.8f', delimiter='\t')
