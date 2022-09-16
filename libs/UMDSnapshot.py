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
from ..load_UMDSnapshot_from_outcar import load_UMDSnapshot_from_outcar
from ..load_UMDSnapshot_from_umd import load_UMDSnapshot_from_umd
# from ..load_UMDSnapshot_from_umd import load_UMDSnapDynamics_from_umd
# from ..load_UMDSnapshot_from_umd import load_UMDSnapThermodynamics_from_umd

    
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
    __eq__
        Compare two UMDSnapshot objects.
    __str__
        Convert a UMDSnapshot objects into a string.
    setThermodynamics
        Initialize the thermodynamics parameters of the snapshot.
    setDynamics
        Initialize the dynamics parameters of the snapshot.
    save
        Print the UMDSnapshot data in an output file.

    """

    def __init__(self, snap=-1, time=0.0, lattice=UMDLattice()):
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
        """
        Decorate a method casting the arguments with the UMDSnapThermodynamics.

        """
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
        """
        Decorate a method casting the arguments with the UMDSnapDynamics.

        """
        def wrap(cls, *args, **kwargs):
            if args:
                dynamics = args[0]
                if isinstance(dynamics, UMDSnapDynamics):
                    position = dynamics.position
                    velocity = dynamics.velocity
                    force = dynamics.force
                    time = dynamics.time
                    return func(cls, position=position, velocity=velocity,
                                force=force, time=time)
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

    def __eq__(self, other):
        """
        Compare two UMDSnapshot objects.

        Parameters
        ----------
        other : UMDSnapshot object
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two snapshot represented are identical,
            otherwise False.

        """
        equal  = isinstance(other, UMDSnapshot)
        equal *= (self.snap == other.snap)
        equal *= (self.lattice == other.lattice)
        equal *= UMDSnapThermodynamics.__eq__(self, other)
        equal *= UMDSnapDynamics.__eq__(self, other)
        return bool(equal)

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
        Print the UMDSnapshot data in an output file.

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

    def UMDSnapshot_from_outcar(self, outcar, load=True):
        """
        Initialize a UMDSnapshot object from an OUTCAR file.

        It reads the OUTCAR file looking for the data to initialize the X
        snapshot. The data are reported after reaching the convergence.
        It scroll all the lines group related to the convergence of the X step
        (-------------------------- Iteration X( y) --------------------------)
        to arrive to the final section where the all the step information are
        collected. The final section start is marked by the header line:
        ---------------- aborting loop because EDIFF is reached ---------------

        Parameters
        ----------
        outcar : input file
            The OUTCAR file.
        simulation : simulation object
            A simulation object with information about the lattice.
        step : int
            The identificative step number.

        Returns
        -------
        snapshot : UMDSnapshot object
            A snapshot object with information about the TD qunatities and
            the atoms dynamics.

        """
        line = outcar.readline()
        while line:
            if ("aborting loop because EDIFF is reached" in line or
                "aborting loop EDIFF was not reached (unconverged)" in line):
                snapshot = load_UMDSnapshot_from_outcar(outcar, self)
                return snapshot
            line = outcar.readline()
        raise(EOFError('OUTCAR file ended but the simulation is uncomplete.'))

    @staticmethod
    def UMDSnapshot_from_outcar_null(outcar):
        """
        Scroll an OUTCAR file without initializing any UMDSnapshot object.

        It work like UMDSnapshot_from_outcar function but it doesn not read any
        data and return None. It is used to accelerate the scrolling of the
        OUTCAR file for useless snapshots.

        Parameters
        ----------
        outcar : input file
            The OUTCAR file.

        Returns
        -------
        None.

        """
        line = outcar.readline()
        while line:
            if ("aborting loop because EDIFF is reached" in line or
                "aborting loop EDIFF was not reached (unconverged)" in line):
                return
            line = outcar.readline()
        raise(EOFError('OUTCAR file ended but the simulation is uncomplete.'))

    def UMDSnapshot_from_umd(self, umd):
        line = umd.readline()
        while line:
            if 'Snapshot:' in line:
                self.snap = int(line.replace('Snapshot:', '').strip())
                snapshot = load_UMDSnapshot_from_umd(umd, self)
                return snapshot
            line = umd.readline()
        raise(EOFError('UMD file ended but the simulation is uncomplete.'))
        