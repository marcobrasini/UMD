# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:40:28 2022

@author: marco
"""

import numpy as np

from UMDSnapshot import UMDSnapshot


class UMDSnapDynamics:
    """
    Class UMDSnapDynamics to contain the dynamic data of a single molecular
    dynamics simulation snapshot.

    """

    def __init__(self, position=[], velocity=[], force=[]):
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
        self.position = np.zeros((UMDSnapshot.natoms, 3), dtype=float)
        self.velocity = np.zeros((UMDSnapshot.natoms, 3), dtype=float)
        self.force = np.zeros((UMDSnapshot.natoms, 3), dtype=float)
        # If position, velocity, force are given and have correct shape,
        # then the corresponding attibutes are set equal to them.
        if len(position) == UMDSnapshot.natoms:
            self.position = position
        if len(velocity) == UMDSnapshot.natoms:
            self.velocity = velocity
        if len(force) == UMDSnapshot.natoms:
            self.force = force

    @staticmethod
    def displacement(position1, position0):
        """
        Calculate the atom displacement with respect to some initial positions.

        Parameters
        ----------
        position1 : array
            Final atoms positions.
        position0 : array
            Initial atoms positions took as reference.

        Returns
        -------
        displacement : array
            Array of all the atoms displacements.

        """
        displacement = position1 - position0
        disp = UMDSnapshot.lattice.reduced(displacement)
        disp = np.where(disp > +0.5, disp-1, disp)
        disp = np.where(disp < -0.5, disp+1, disp)
        displacement = UMDSnapshot.lattice.cartesian(disp)
        return displacement

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
        headerstyle = '{:16}{:16}{:16}'
        header  = headerstyle.format('Position_x', 'Position_y', 'Postion_z')
        header += headerstyle.format('Velocity_x', 'Velocity_y', 'Postion_z')
        header += headerstyle.format('Force_x', 'Force_y', 'Force_z') + '\n'
        outfile.write(header)
        dynamics = np.hstack((self.position, self.velocity, self.force))
        np.savetxt(outfile, dynamics, fmt='%15.8f', delimiter=' ')
