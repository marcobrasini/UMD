"""
===============================================================================
                              UMDSnapDynamics class
===============================================================================

This module provides the UMDSnapDynamcis class useful to collect the dynamical
quantities of each atoms in a molecular dynamics snapshot.
The UMDSnapDynamics objects are mainly used in UMDSnapshot objects.

Classes
-------
    UMDSnapDynamics

See Also
--------
    UMDSnapshot

"""


import numpy as np

from .UMDSnapshot import UMDSnapshot


class UMDSnapDynamics:
    """
    UMDSnapDynamics class to collect the thermodynamics quantities of each atom
    in a molecular dynamics snapshot.
    
    Parameters
    ----------
    time : float
        Time duration of the snapshot in fs.
    position : array, optional
        Array of all the atoms positions.
    velocity : array, optional
        Array of all the atoms velocities.
    force : array, optional
        Array of all the atoms forces.

    Methods
    -------
    __str__
        Convert a UMDSnapDynamics objects into a string.
    save
        Print the UMDSnapDynamics information on an output stream.
    displacement
        Calculate the atomic displacement between two arrays of positions.

    """

    def __init__(self, time=0, position=[], velocity=[], force=[]):
        """
        Construct the UMDSnapDynamics object.

        Parameters
        ----------
        time : float, optional
            Time duration of the snapshot. The default is 0.0.
        lattice : UMDLattice, optional
            Lattice reference of the snapshot. The default is UMDLattice().
        position : array, optional
            Array of all the atoms positions. The default is [].
        velocity : array, optional
            Array of all the atoms velocities. The default is [].
        force : array, optional
            Array of all the atoms forces. The default is [].

        Returns
        -------
        UMDSnapDynamics object.

        """
        self.time = time
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

    def __str__(self, w=12, f=6):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the atoms dynamical vectors.

        """
        string = 'Dynamics: {:12.3f} fs\n'.format(self.time)
        dynamics = np.hstack((self.position, self.velocity, self.force))
        headerstyle = '{:'+str(3*w)+'}{:'+str(3*w)+'}{:'+str(3*w)+'}'
        string += headerstyle.format('Positions', 'Velocities', 'Forces')
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
        header = 'Dynamics: {:12.3f} fs\n'.format(self.time)
        headerstyle = '{:16}{:16}{:16}'
        header += headerstyle.format('Position_x', 'Position_y', 'Postion_z')
        header += headerstyle.format('Velocity_x', 'Velocity_y', 'Postion_z')
        header += headerstyle.format('Force_x', 'Force_y', 'Force_z')
        outfile.write(header+'\n')
        dynamics = np.hstack((self.position, self.velocity, self.force))
        np.savetxt(outfile, dynamics, fmt='%15.8f', delimiter=' ')
