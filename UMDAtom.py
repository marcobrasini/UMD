"""
===============================================================================
                                    UMDAtom
===============================================================================

This module provides the UMDAtom class useful to represent chemical elements.
The UMDAtom objects are mainly used to initialize the 'atoms' parameter of a
UMDLattice object, in which they represent the key of the 'atoms' dictionary.

Classes
-------
    UMDAtom

See Also
--------
    UMDLattice
"""


class UMDAtom:
    """
    UMDAtom class to represent atomic elements.

    Parameters
    ----------
    name : string, optional
        The atomic symbol.
        The default is ''.
    Z : int, optional
        The atomic number.
        The default is 0.
    mass : float, optional
        The atomic mass.
        The default is 0.0.
    valence : int, optional
        The number of valence electrons.
        The default is 0.

    Methods
    -------
    __eq__
        Compare two UMDAtom objects.
    __str__
        Convert a UMDAtoms objects into a string.
    """

    def __init__(self, Z=0, name='', mass=0.0, valence=0):
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
        self.Z = Z
        self.name = name
        self.mass = mass
        self.valence = valence

    def __eq__(self, other):
        """
        Compare two UMDAtom objects.

        Parameters
        ----------
        other : UMDAtom object
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two atoms are identical, otherwise False.

        """
        equal = isinstance(other, UMDAtom)
        equal *= (self.Z == other.Z)
        equal *= (self.name == other.name)
        equal *= (self.mass == other.mass)
        equal *= (self.valence == other.valence)
        return equal

    def __hash__(self):
        """
        Get the hash value for dictionary keys comparison.

        Returns
        -------
        hash_atom : int
            The hash values of the object.

        """
        hash_atom = hash((self.Z, self.name, self.mass, self.valence))
        return hash_atom

    def __str__(self):
        """
        Convert a UMDAtom object into a string.

        Returns
        -------
        string : string
            The atomic symbol.

        """
        string = self.name
        return string
