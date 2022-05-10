# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:40:28 2022

@author: marco
"""

import numpy as np
from UMDLattice import UMDLattice

class UMDSnapDynamics:
    """
    Class UMDSnapDynamics to contain the dynamic data of a single MD simulation
    snapshot.

    """

    def __init__(self, snaptime=0.0, lattice=UMDLattice(), 
                 position=[], displacement=[], velocity=[], force=[]):
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

    def displacement(self, position0):
        self.displacement = self.position - position0
        reduced_displacement = self.lattice.reduce(self.displacement)
        for i in range(3):
            delta = reduced_displacement.T[i]
            delta = np.where(delta > +0.5, delta-1, delta)
            delta = np.where(delta > -0.5, delta+1, delta)
            reduced_displacement.T[i] = delta
        self.displacement = self.lattice.direct(reduced_displacement)
        return self.displacement

    def velocity(self):
        self.velocity = self.displacement/self.snaptime
        return self.velocity

    def __str__(self):
        dynamics = np.hstack((self.position, self.velocity, self.force))
        string = str(dynamics)
        return string

    def save(self, outfile):
        dynamics = np.hstack((self.position, self.velocity, self.force))
        np.savetxt(outfile, dynamics, fmt='%.8f', delimiter='\t')
