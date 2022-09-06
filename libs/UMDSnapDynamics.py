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
    __eq__
        Compare two UMDSnapDynamics objects.
    __str__
        Convert a UMDSnapDynamics objects into a string.
    save
        Print the UMDSnapDynamics information on an output stream.

    """

    def __init__(self, time=0, position=[], velocity=[], force=[]):
        """
        Construct the UMDSnapDynamics object.

        Parameters
        ----------
        time : float, optional
            Time duration of the snapshot. The default is 0.0.
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
        self.position = position
        self.velocity = velocity
        self.force = force

    def __eq__(self, other):
        """
        Compare two UMDSnapDynamics objects.

        Parameters
        ----------
        other : UMDSnapDynamics
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two set of dynamics quantities saved
            in the snapshots are identical, otherwise False.

        """
        equal  = isinstance(other, UMDSnapDynamics)
        equal *= (self.time == other.time)
        equal *= np.array_equal(self.position, other.position)
        equal *= np.array_equal(self.velocity, other.velocity)
        equal *= np.array_equal(self.force, other.force)
        return equal

    def __str__(self):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the atoms dynamical vectors.

        """
        string = 'Dynamics: {:12.3f} fs\n'.format(self.time)
        dynamics = np.hstack((self.position, self.velocity, self.force))
        string += '{:16}{:16}{:16}'.format('Position_x', 'Position_y',
                                           'Position_z')
        string += '{:16}{:16}{:16}'.format('Velocity_x', 'Velocity_y',
                                           'Velocity_z')
        string += '{:16}{:16}{:16}'.format('Force_x', 'Force_y', 'Force_z')
        for atom in dynamics:
            string += '\n ' + ' '.join(['{:15.8f}'.format(x) for x in atom])
        return string
