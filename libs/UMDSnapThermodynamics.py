"""
===============================================================================
                         UMDSnapThermodynamics class
===============================================================================

This module provides the UMDSnapThermodynamcis class useful to collect the 
thermodynamics quantities of a molecular dynnamics snapshot. 
The UMDSnapThermodynamics objects are mainly used in UMDSnapshot objects.

Classes
-------
    UMDSnapThermodynamics

See Also
--------
    UMDSnapshot

"""


class UMDSnapThermodynamics:
    """
    UMDSnapThermodynamics class to collect the thermodynamic quantities of a
    single molecular dynamics simulation snapshot.

    Parameters
    ----------
    temperature : float
        The system temperature in K.
    pressure : float
        The system pressure in GPa.
    energy : float
        The system energy in eV.

    Methods
    -------
    __eq__
        Compare two UMDSnapThermodynamics objects.
    __str__
        Convert a UMDSnapThermodynamics objects into a string.
    save
        Print the UMDSnapThermodynamics information on an output stream.

    """

    def __init__(self, temperature=0.0, pressure=0.0, energy=0.0):
        """
        Construct UMDSnapThermodynamics object.

        Parameters
        ----------
        temperature : float, optional
            The system temperature in K. The default is 0.0.
        pressure : float, optional
            The system pressure in GPa. The default is 0.0.
        energy : float, optional
            The system energy in eV. The default is 0.0.

        Returns
        -------
        UMDSnapThermodynamics object.

        """
        self.temperature = temperature
        self.pressure = pressure
        self.energy = energy

    def __eq__(self, other):
        """
        Compare two UMDSnapThermodynamics objects.

        Parameters
        ----------
        other : UMDSnapshot
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two set of thermodynamics quantities saved
            in the snapshots are identical, otherwise False.

        """
        equal  = isinstance(other, UMDSnapThermodynamics)
        equal *= (self.temperature == other.temperature)
        equal *= (self.pressure == other.pressure)
        equal *= (self.energy == other.energy)
        return equal

    def __str__(self):
        """
        Convert a UMDSnapThermodynamics objects into a string.

        Returns
        -------
        string : string
            A descriptive string reporting the thermodynamics quantities of the
            snapshot.

        """
        string  = "Thermodynamics:\n"
        string += "  Temperature = {:14.6f} K\n" .format(self.temperature)
        string += "  Pressure    = {:14.6f} GPa\n".format(self.pressure)
        string += "  Energy      = {:14.6f} eV".format(self.energy)
        return string

    def save(self, outfile):
        """
        Print on file the UMDSnapThermodynamics informations.

        Parameters
        ----------
        outfile : output file
            The output file where to print the UMDSnapThermodynamics.

        Returns
        -------
        None.

        """
        outfile.write(str(self)+'\n')
