# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:40:29 2022

@author: marco
"""


class UMDSnapThermodynamics:
    """
    Class UMDSnapThermodynamics to contain the thermodynamic data of a single
    molecular dynamics simulation snapshot.

    """

    def __init__(self, temperature=0.0, pressure=0.0, energy=0.0):
        """
        Construct UMDSnapThermodynamics object.

        Parameters
        ----------
        temperature : float, optional
            System temperature. The default is 0.0.
        pressure : float, optional
            System pressure. The default is 0.0.
        energy : float, optional
            System energy. The default is 0.0.

        Returns
        -------
        UMDSnapThermodynamics object.

        """
        self.temperature = temperature
        self.pressure = pressure
        self.energy = energy

    def __str__(self):
        """
        Overload of the __str__ function.

        Returns
        -------
        string : string
            Report of the thermodynamics values of the snapshot.

        """
        string  = "Temperature = {:12.4f} K\n" .format(self.temperature)
        string += "Pressure    = {:12.4f} GPa\n".format(self.pressure)
        string += "Energy      = {:12.4f} eV".format(self.energy)
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
