"""
===============================================================================
                            UMDLattice class tests
===============================================================================
"""

from ..libs.UMDLattice import UMDLattice
from ..libs.UMDAtom import UMDAtom

import pytest
import numpy as np


# %% Unit test for a generic lattice
class Test_UMDLattice_unit:
    """
    The unit tests implemented test an instance of the UMDLattice class
    representing a generic lattice.
    The lattice represented has a triclinic structure with basis vectors:
                a = (2, 0, 0), b = (1, 2, 0), c = (1, 1, 1)
    and it containg 21 atoms of two different types implemented with the
    UMDAtom class:
        15 atoms of type 'X' and with mass 3.00
        6 atoms of type 'Y' and with mass 4.50

    """

    X = UMDAtom(name='X', mass=3.00)
    Y = UMDAtom(name='Y', mass=4.50)
    atoms = {X: 15, Y: 6}

    name = 'LatticeName'
    basis = np.array([[2, 0, 0],
                      [1, 2, 0],
                      [1, 1, 1]])
    inverse_basis = np.linalg.inv(basis)
    lattice = UMDLattice(name, basis, atoms)

    # %% UMDLattice __init__ function tests
    def test_UMDLattice_init_default(self):
        """
        Test the __init__ function default constructor.

        """
        lattice = UMDLattice()
        assert lattice.name == ''
        assert lattice.atoms == {}
        assert np.array_equal(lattice.dirBasis, np.identity(3))
        assert np.array_equal(lattice.invBasis, np.identity(3))

    def test_UMDLattice_init_assignement(self):
        """
        Test the __init__ function assignement operations with a non singular
        matrix of lattice vectors.

        """
        assert self.lattice.name == self.name
        assert self.lattice.atoms == self.atoms
        assert np.array_equal(self.lattice.dirBasis, self.basis)
        assert np.array_equal(self.lattice.invBasis, self.inverse_basis)

    def test_UMDLattice_init_basis_inversion(self):
        """
        Test the __init__ function matrix inversion operation for a non
        singular matrix of lattice vectors. The matrix product between the
        'dirBasis' and 'invBasis' must be equal (or close) to the identical
        matrix.

        """
        identity = self.lattice.dirBasis @ self.lattice.invBasis
        assert np.allclose(identity, np.identity(3))

    def test_UMDLattice_init_basis_inversion_error(self):
        """
        Test the __init__ function matrix inversion operation for a singular
        matrix of lattice vectors. A numpyp.linalg.LinAlgError must be raised.

        """
        singular_basis = np.copy(self.basis)
        singular_basis[0] = 0
        with pytest.raises(np.linalg.LinAlgError):
            UMDLattice(self.name, singular_basis, self.atoms)

    # %% UMDLattice __eq__ function tests
    def test_UMDLattice_eq_true(self):
        """
        Test the __eq__ function to compare two UMDLattice objects representing
        two identical lattices. The value returned must be True, despite they
        can have different names.

        """
        basis2 = self.basis
        atoms2 = self.atoms
        lattice2 = UMDLattice('', basis2, atoms2)
        assert self.lattice == lattice2

    def test_UMDLattice_eq_false_basis(self):
        """
        Test the __eq__ function to compare two UMDLattice objects representing
        two different lattices, with same atoms but different lattice basis.
        The value returned must be False.

        """
        atoms = self.atoms
        basis = self.basis + 1
        lattice2 = UMDLattice('', basis, atoms)
        assert not self.lattice == lattice2

    def test_UMDLattice_eq_false_atoms_types(self):
        """
        Test the __eq__ function to compare two UMDLattice objects representing
        two different lattices, with same lattice basis but different atoms.
        Since the types of atoms are different, the value returned must be
        False.

        """
        atoms2 = {self.X: 15}
        lattice2 = UMDLattice('', self.basis, atoms2)
        assert not self.lattice == lattice2

    def test_UMDLattice_eq_false_atoms_number(self):
        """
        Test the __eq__ function to compare two UMDLattice objects representing
        two different lattices, with same lattice basis but different atoms.
        Since the number of atoms per type is different, the value returned
        must be False.

        """
        atoms2 = {self.X: 15, self.Y: 2}
        lattice2 = UMDLattice('', self.basis, atoms2)
        assert not self.lattice == lattice2

    # %% UMDLattice __str__ function tests
    def test_UMDLattice_str(self):
        """
        Test the __str__ function to convert the UMDLattice information into a
        descriptive and printable string object.

        """
        string  = 'Lattice: LatticeName                   \n'
        string += '       2.000000        0.000000        0.000000\n'
        string += '       1.000000        2.000000        0.000000\n'
        string += '       1.000000        1.000000        1.000000\n'
        string += 'X     Y    \n'
        string += '   15     6'
        print(str(self.lattice))
        print(string)
        assert str(self.lattice) == string

    def test_UMDLattice_str_length(self):
        """
        Test the __str__ function correct length of the string object returned.
        The total length must be:
            + line1 = 9 + 30 + 1
            + line2 = 15 + 1 + 15 + 1 + 15 + 1
            + line3 = 15 + 1 + 15 + 1 + 15 + 1
            + line4 = 15 + 1 + 15 + 1 + 15 + 1
            + line5 = (5 + 1) * number of atom types
            + line6 = (5 + 1) * number of atom types - 1(the last '\n')
                    = 40 + 3*48 + 12*(number of atom types) - 1

        """
        stringlength = 184 + 2*6*len(self.atoms) - 1
        assert len(str(self.lattice)) == stringlength

    # %% UMDLattice natoms function tests
    def test_UMDLattice_natoms(self):
        """
        Test the natoms function. The number of atoms returned must b equal to
        the sum of the number of atoms per each element in the 'atoms'
        dictionary.

        """
        assert self.lattice.natoms() == 21

    # %% UMDLattice mass function tests
    def test_UMDLattice_mass(self):
        """
        Test the mass function. The total mass of the cell must be equal to the
        sum of the masses of all the atoms in the cell.

        """
        assert self.lattice.mass() == 72.0

    # %% UMDLattice volume function tests
    def test_UMDLattice_volume(self):
        """
        Test the volume function. The cell volume must be equal to the mixed
        cross-dot product of the lattice basis vectors.

        """
        assert self.lattice.volume() == 4.0

    # %% UMDLattice density function tests
    def test_UMDLattice_density(self):
        """
            Test the density function. The matter density in the cell must be
            equal to the ratio between the total mass in the unit cell and the
            unit cell volume.

        """
        assert self.lattice.density() == 72.0/4

    # %% UMDLattice reduced function tests
    def test_UMDLattice_reduced_basis(self):
        """
        Test the reduced function to convert a vector in cartesian coordiates
        to reduced coordinates refered to the lattice vector system.
        To test it, we assert that the each basis vector in cartesian
        coordinate must be transformed into a canonical basis vector.
            
        """
        reduced_a = self.lattice.reduced(self.basis[0])
        reduced_b = self.lattice.reduced(self.basis[1])
        reduced_c = self.lattice.reduced(self.basis[2])
        assert np.allclose(reduced_a, np.array([1, 0, 0]))
        assert np.allclose(reduced_b, np.array([0, 1, 0]))
        assert np.allclose(reduced_c, np.array([0, 0, 1]))

    def test_UMDLattice_reduced_allbasis(self):
        """
        Test the reduced function to convert a set of vectors in cartesian
        coordiates to reduced coordinates refered to the lattice vector system.
        To test it, we assert that the matrix made of all the three basis
        vectors in cartesian coordinates must be transformed into a matrix
        made of all the canonical basis vectors.

        """
        reduced = self.lattice.reduced(self.basis)
        assert np.allclose(reduced, np.identity(3))

    def test_UMDLattice_reduced_halfbasis(self):
        """
        Test the reduced function to convert a set of vectors in cartesian
        coordiates to reduced coordinates refered to the lattice vector system.
        To test it, we assert that the matrix made of only the first two basis
        vectors in cartesian coordinates must be transformed into a matrix made
        of only the first two canonical basis vectors.

        """
        reduced = self.lattice.reduced(self.basis[:2])
        assert np.allclose(reduced, np.identity(3)[:2])

    def test_UMDLattice_reduced_from_cartesian(self):
        """
        Test the reduced function to convert a set of vectors in cartesian
        coordiates to reduced coordinates refered to the lattice vector system.
        To test it, we assert that a vector in reduced coordinates must be
        equal (or close) to itself, when it is firts tranformed in cartesian
        coordinates and then back again into reduced coordinates.

        """
        vector = np.array([1, 3, 2])
        cartesian = self.lattice.cartesian(vector)
        reduced = self.lattice.reduced(cartesian)
        assert np.allclose(reduced, vector)

    # %% UMDLattice cartesian function tests
    def test_UMDLattice_cartesian_basis(self):
        """
        Test the cartesian function to convert a vector in reduced coordiates
        refered to the lattice vector system to cartesian coordinates.
        To test it, we assert that each basis vector in the reduced
        coordinates, equal to a canonical basis vector, must be transformed
        into the original cartesian basis vector.

        """
        cartesian_a = self.lattice.cartesian(np.array([1, 0, 0]))
        cartesian_b = self.lattice.cartesian(np.array([0, 1, 0]))
        cartesian_c = self.lattice.cartesian(np.array([0, 0, 1]))
        assert np.allclose(cartesian_a, self.basis[0])
        assert np.allclose(cartesian_b, self.basis[1])
        assert np.allclose(cartesian_c, self.basis[2])

    def test_UMDLattice_cartesian_allbasis(self):
        """
        Test the cartesian function to convert a set of vectors in reduced
        refered to the lattice vector system coordiates to cartesian
        coordinates.
        To test it, we assert that the matrix made of all basis vectors in the
        reduced coordinates, equal to the identity matrix, must be transformed
        into a matrix made of all the original basis vectors.

        """
        cartesian = self.lattice.cartesian(np.identity(3))
        assert np.allclose(cartesian, self.basis)

    def test_UMDLattice_cartesian_halfbasis(self):
        """
        Test the cartesian function to convert a set of vectors in reduced
        refered to the lattice vector system coordiates to cartesian
        coordinates.
        To test it, we assert that the matrix made of only the first two basis
        vectors in the reduced coordinates, equal to the first to canonical
        basis vectors, must be transformed into a matrix made of only the first
        two original basis vectors.

        """
        cartesian = self.lattice.cartesian(np.identity(3)[:2])
        assert np.allclose(cartesian, self.basis[:2])

    def test_UMDLattice_cartesian_from_reduced(self):
        """
        Test the reduced function to convert a set of vectors in cartesian
        coordiates to reduced coordinates refered to the lattice vector system.
        To test it, we assert that a vector in reduced coordinates must be
        equal (or close) to itself, when it is firts tranformed in cartesian
        coordinates and then back again into reduced coordinates.

        """
        vector = np.array([1, 3, 2])
        reduced = self.lattice.reduced(vector)
        cartesian = self.lattice.cartesian(reduced)
        assert np.allclose(cartesian, vector)

    # %% UMDLattice isdefault function tests
    def test_UMDLattice_isdefault_true(self):
        Lattice = UMDLattice()
        assert Lattice.isdefault()

    def test_UMDLattice_isdefault_false_name(self):
        Lattice = UMDLattice(name='Lattice')
        assert not Lattice.isdefault()

    def test_UMDLattice_isdefault_false_basis(self):
        Lattice = UMDLattice(basis=2*np.identity(3))
        assert not Lattice.isdefault()

    def test_UMDLattice_isdefault_false_atoms(self):
        Lattice = UMDLattice(atoms={self.X: 0})
        assert not Lattice.isdefault()


# %% ===================================================================== %% #
# %% hypothesis tests