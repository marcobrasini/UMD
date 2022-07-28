"""
===============================================================================
                                   UMDLattice
===============================================================================

This module provides the UMDLattice class useful to represent a lattice
structure. The UMDLattice objects are mainly used to describe the environment
in which the UMDSimulation take place but not only, also to perform dynamics
calculations on the atoms.

Classes
-------
    UMDLattice

See Also
--------
    UMDSimulation
"""

import numpy as np
import itertools as it


DEFAULT_basis = np.identity(3, dtype=float)


class UMDLattice:
    """
    UMDLattice class to represent a braivais crystal lattice.

    The UMDLattice objects are defined by three 3-dim lattice vectors defining
    the lattice unit cell and the periodic structure, but also by a set of
    atoms populating the cell.

    Parameters
    ----------
    name : string, optional
        The name of the lattice.
    basis : numpy array (3,3), optional
        A matrix composed by the three lattice vectors 'a', 'b' and 'c'.
        The matrix strucure is the following:
            basis = np.array([[ax, ay, az], [bx, by, bz], [cx, cy, cz]])
    atoms : dict, optional
        A dictionary made of atomic species coupled with their respective
        number of copies present into the unit cell. Typically the single item
        has the structure {UMDAtom: number_of_atoms}.

    Methods
    -------
    __eq__
        Compare two UMDLattice objects.
    __str__
        Convert a UMDLattice objects into a string.
    save
        Print the UMDLattice information on an output stream.
    natoms
        Get the total number of atoms of any type in the unit cell.
    mass
        Get the total mass of all the atoms into the unit cell.
    volume
        Get the volume of the unit cell.
    density
        Get the mass density into the unit cell.
    cartesian
        Convert 3-dim vectors from reduced to cartesian coordinates.
    reduced
        Convert 3-dim vectors from cartesian to reduced coordinates.

    """

    def __init__(self, name='', basis=DEFAULT_basis, atoms={}):
        """
        Construct UMDLattice object.

        Parameters
        ----------
        name : string, optional
            The name of the lattice.
            The default is ''.
        basis : numpy array (3,3), optional
            A matrix composed by the three lattice vectors 'a', 'b' and 'c'.
            The matrix strucure is the following:
                basis = np.array([[ax, ay, az], [bx, by, bz], [cx, cy, cz]])
            The default is np.identity(3).
        atoms : dict, optional
            A dictionary made of atomic species coupled with their respective
            number of copies present into the unit cell. Typically, the single
            item has the structure {UMDAtom: number_of_atoms}.
            The default is {}.

        Returns
        -------
        UMDLattice object.

        """
        self.name = name
        self.atoms = atoms
        self.dirBasis = np.copy(basis)
        self.invBasis = np.copy(np.linalg.inv(basis))

    def __eq__(self, other):
        """
        Compare two UMDLattice objects.

        Parameters
        ----------
        other : UMDLattice object
            The second term of the comparison.

        Returns
        -------
        equal : bool
            It returns True if the two lattices represented are identical,
            otherwise False.

        """
        equal = isinstance(other, UMDLattice)
        equal *= (self.atoms == other.atoms)
        equal *= np.array_equal(self.dirBasis, other.dirBasis)
        equal *= np.array_equal(self.invBasis, other.invBasis, True)
        return equal

    def __str__(self):
        """
        Convert a UMDLattice objects into a string.

        Returns
        -------
        string : string
            A descriptive string reporting the UMDLattice values.

        """
        string = 'Lattice: {:30}\n'.format(self.name)
        for vector in self.dirBasis:
            string += ' '.join(['{:15.6f}'.format(x) for x in vector])+'\n'
        atoms_name = self.atoms.keys()
        atoms_val = self.atoms.values()
        string += ' '.join(['{:5}'.format(str(n)) for n in atoms_name])+'\n'
        string += ' '.join(['{:5}'.format(n) for n in atoms_val])
        return string

    def save(self, outfile):
        """
        Print the UMDLattice information on an output stream.

        Parameters
        ----------
        outfile : output stream
            The output stream where to print the UMDLattice.

        Returns
        -------
        None.

        """
        outfile.write(str(self)+'\n\n')

    def natoms(self):
        """
        Get the total number of atoms of any type in the unit cell.

        Returns
        -------
        natoms : int
            The total number of atoms in the unit cell.

        """
        natoms = sum(self.atoms.values())
        return natoms

    def mass(self):
        """
        Get the total mass of all the atoms into the unit cell.

        Returns
        -------
        mass : float
            The unit cell total mass.

        """
        mass = 0
        for atom, n in self.atoms.items():
            mass += n*atom.mass
        return mass

    def volume(self):
        """
        Get the volume of the unit cell.

        Returns
        -------
        volume : float
            The unit cell volume.

        """
        volume = np.cross(self.dirBasis[0], self.dirBasis[1])
        volume = abs(np.dot(volume, self.dirBasis[2]))
        return volume

    def density(self):
        """
        Get the mass density into the unit cell.

        Returns
        -------
        density : float
            The unit cell mass.

        """
        density = self.mass()/self.volume()
        return density

    def reduced(self, cartesian):
        """
        Convert cartesian vectors in reduced coordinates.

        Parameters
        ----------
        cartesian : array(N,3)
            An array of N 3-dim vectors in cartesian coordinates.

        Returns
        -------
        reduced : array(N,3)
            An array of N 3-dim vectors in reduced coordinates.

        """
        reduced = cartesian @ self.invBasis
        return reduced

    def cartesian(self, reduced):
        """
        Convert reduced vectors in cartesian coordinates.

        Parameters
        ----------
        reduced : array(N,3)
            An array of N 3-dim vectors in reduced coordinates.

        Returns
        -------
        cartesian : array(N,3)
            An array of N 3-dim vectors in cartesian coordinates.

        """
        cartesian = reduced @ self.dirBasis
        return cartesian

    def bonds(self):
        bonds = list(it.product(self.atoms.keys(), repeat=2))
        return bonds
    
    def atomslice(self, atom):
        offset = 0
        for at,n in self.atoms.items():
            if at == atom:
                return slice(offset, offset+n)
            offset += n

    def periodic(self, variation, cartesian=True):
        if cartesian:
            variation = self.reduced(variation)
        variation = np.where(variation > +0.5, variation-1, variation)
        variation = np.where(variation < -0.5, variation+1, variation)
        if cartesian:
            variation = self.cartesian(variation)
        return variation