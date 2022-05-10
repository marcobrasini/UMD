# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:40:29 2022

@author: marco
"""


class UMDSnapThermodynamics:
    """
    Class UMDSnapThermodynamics to contain the thermodynamic data of a single
    MD simulation snapshot.

    """

    def __init__(self, temperature, pressure, energy):
        self.temperature = temperature
        self.pressure = pressure
        self.energy = energy

    def __str__(self):
        string  = "Temperature = " + str(self.temperature) + ' K\n'
        string += "Pressure = " + str(self.pressure) + ' GPa\n'
        string += "Energy = " + str(self.energy) + ' eV'
        return string

    def save(self, outfile):
        outfile.write(str(self)+'\n')
