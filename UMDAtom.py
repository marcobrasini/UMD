# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:12:50 2022

@author: marco
"""


class UMDAtom:
    """
    Class to contain the infomration about the atomic elements in the lattice.
    
    """
    def __init__(self, name='', Z=0, mass=0.0, valence=0):
        """
        Construct UMDAtom object.

        Parameters
        ----------
        name : string, optional
            Atomic symbol. The default is ''.
        Z : int, optional
            Atomic number. The default is 0.
        mass : float, optional
            Atomic mass. The default is 0.0.
        valence : int, optional
            Number of valence electrons. The default is 0.

        Returns
        -------
        UMDAtom object.

        """
        self.name = name
        self.Z = Z
        self.mass = mass
        self.valence = valence

    def __eq__(self, other):
        """
        Overload of the == operator.

        Parameters
        ----------
        other : UMDAtom object
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two atoms are identical, otherwise False.

        """
        equal = True
        equal = equal and (self.name == other.name)
        equal = equal and (self.Z == other.Z)
        equal = equal and (self.mass == other.mass)
        equal = equal and (self.valence == other.valence)
        return equal

    def __hash__(self):
        """
        Overload of the __hash__ operator.

        Returns
        -------
        hash_atom : int
            The hash values of the object for dictionary keys comparison.

        """
        hash_atom = hash((self.name, self.Z, self.mass, self.valence))
        return hash_atom
