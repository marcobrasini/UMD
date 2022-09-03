"""
===============================================================================
                              UMDSnapshot class
===============================================================================

This module provides the UMDSnapshot class to collect the thermodynamical and dynamical quantities of each atoms in a molecular dynamics snapshot.

Classes
-------
    UMDSnapshot

See Also
--------
    UMDSnapThermodynamics
    UMDSnaoDynamics

"""


import numpy as np
from .UMDLattice import UMDLattice
from .UMDSnapDynamics import UMDSnapDynamics
from .UMDSnapThermodynamics import UMDSnapThermodynamics

    
class UMDSnapshot(UMDSnapThermodynamics, UMDSnapDynamics):
    """
    Class UMDSnapshot to contain the data of a single molecular dynamics
    simulation snapshot.
    The snapshot data are grouped and stored in two categories:
        - Thermodynamic data (like volume, temperature, pressure, energy...)
        - Dynamic data (like atoms position, velocity, force)

    Parameters
    ----------
    snap : int
        The snapshot index.
    lattice : UMDLattice
        The lattice informations.
    natoms : int
        The number of atoms in the snapshot.
    temperature: float
        The snapshot temperature in K.
    pressure: float
        The snapshot pressure in GPa.
    energy: float
        The snapshot energy in eV.
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
        Convert a UMDSnapshot objects into a string.
    setThermodynamics
        Initialize the thermodynamics parameters of the snapshot.
    setDynamics
        Initialize the dynamics parameters of the snapshot.

    """

    def __init__(self, snap, time, lattice):
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
        UMDSnapDynamics.__init__(self, time)

    def isUMDSnapThermodynamics(func):
        def wrap(cls, *args, **kwargs):
            if args:
                thermodynamics = args[0]
                if isinstance(thermodynamics, UMDSnapThermodynamics):
                    temperature = thermodynamics.temperature
                    pressure = thermodynamics.pressure
                    energy = thermodynamics.energy
                    return func(cls, temperature=temperature, 
                                pressure=pressure, energy=energy)
            return func(cls, *args, **kwargs)
        return wrap
    
    def isUMDSnapDynamics(func):
        def wrap(cls, *args, **kwargs):
            if args:
                dynamics = args[0]
                if isinstance(dynamics, UMDSnapDynamics):
                    position = dynamics.position
                    velocity = dynamics.velocity
                    force = dynamics.force
                    time = dynamics.time
                    return func(cls, position=position, 
                                velocity=velocity, force=force, time=time)
            return func(cls, *args, **kwargs)
        return wrap

    @isUMDSnapThermodynamics
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

    @isUMDSnapDynamics
    def setDynamics(self, position=[], velocity=[], force=[], time=0.0):
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
        if not time:
            time = self.time
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
        string = UMDSnapshot.__str__(self)
        outfile.write(string+'\n\n')
