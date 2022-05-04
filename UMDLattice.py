# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:24:02 2022

@author: marco
"""

import numpy as np


NULL_Basis = np.zeros((3, 3), dtype=float)


class UMDLattice:
    """
    Class to contain the information about the simulation lattice.

    The UMDLattice class is defined by three 3-dim lattice vectors defining
    the lattice unit cell and a set of atoms populating the cell.
    """

    def __init__(self, name='', basis=NULL_Basis, atoms={}):
        """
        Construct UMDLattice object.

        Parameters
        ----------
        name : string, optional
            The name of the lattice.
            The default is ''.
        basis : numpy array (3,3), optional
            Matrix made of lattice vectors.
            The default is np.zeros((3, 3)).
        atoms : dict, optional
            Dictionary of atoms with their number into the lattice.
            The default is {}.

        Returns
        -------
        UMDLattice object

        """
        self.name = name
        self.atoms = atoms
        self.dirBasis = basis

        # If possible, we initialize the inverse basis matrix.
        # The inverse basis matrix is necessary to move from cartesian to
        # reduced coordinate system.
        self.invBasis = NULL_Basis
        try:
            self.invBasis = np.linalg.inv(basis)
        except np.linalg.LinAlgError:
            self.invBasis[:] = np.nan

    def natoms(self):
        """
        Get the number of atoms of any type in the lattice.

        Returns
        -------
        n : int
            Total number of atoms in the lattice.

        """
        n = sum(self.atoms.values())
        return n

    def reduced(self, cartesian):
        """
        Convert cartesian vectors in reduced coordinates.

        Parameters
        ----------
        cartesian : array(N,3)
            Array of N 3-dim vectors in cartesian coordinates.

        Returns
        -------
        reduced : array(N,3)
            Array of N 3-dim vectors in reduced coordinates.

        """
        reduced = (self.invBasis.T @ cartesian.T).T
        return reduced

    def cartesian(self, reduced):
        """
        Convert reduced vectors in cartesian coordinates.

        Parameters
        ----------
        reduced : array(N,3)
            Array of N 3-dim vectors in reduced coordinates.

        Returns
        -------
        cartesian : array(N,3)
            Array of N 3-dim vectors in cartesian coordinates.

        """
        cartesian = self.dirBasis.T @ reduced
        return cartesian.T
