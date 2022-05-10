# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:28:41 2022

@author: marco
"""

import numpy as np


class UMDSnapshot:
    """
    Class UMDSnapshot to contain the data of a single MD simulation snapshot.

    The snapshot data are grouped in two categories:
        - Thermodynamic data (like volume, temperature, pressure, energy...)
        - Dynamic data (like atoms position, velocity, force)

    """

    def __init__(self, snapiter, snapThermodynamics, snapDynamics):
        self.snapIter = snapiter
        self.snapThermodynamics = snapThermodynamics
        self.snapDynamics = snapDynamics

    def __str__(self):
        string  = "Snapshot: " + str(self.snapIter) + '\n'
        string += str(self.snapThermodynamics) + '\n'
        string += str(self.snapDynamics)
        return string

    def save(self, outfile):
        outfile.write("Snapshot: " + str(self.snapIter) + '\n')
        self.snapThermodynamics.save(outfile)
        self.snapDynamics.save(outfile)
