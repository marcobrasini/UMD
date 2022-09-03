"""
===============================================================================
                            UMDLattice class tests
===============================================================================
"""

from ..libs.UMDLattice import UMDLattice
from ..libs.UMDAtom import UMDAtom

import pytest
import numpy as np
import hypothesis as hp
import hypothesis.strategies as st

from .test_scenarios import getNumpyArray
from .test_scenarios_UMDLattice import dataUMDLattice, getUMDLattice


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

    X = UMDAtom(name='X', mass=3.00, valence=2.0)
    Y = UMDAtom(name='Y', mass=4.50, valence=3.0)
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
        string += 'X         Y        \n'
        string += '      3.0       4.5\n'
        string += '      2.0       3.0\n'
        string += '       15         6'
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
            + line5 = (9 + 1) * number of atom types
            + line5 = (9 + 1) * number of atom types
            + line5 = (9 + 1) * number of atom types
            + line6 = (9 + 1) * number of atom types - 1(the last '\n')
                    = 40 + 3*48 + 12*(number of atom types) - 1

        """
        stringlength = 184 + 4*10*len(self.atoms) - 1
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
        Test the cartesian function to convert a set of vectors in reduced
        coordiates refered to the lattice vector system to cartesian
        coordinates.
        To test it, we assert that a vector in cartesian coordinates must be
        equal (or close) to itself, when it is firts tranformed in reduced
        coordinates and then back again into cartesian coordinates.

        """
        vector = np.array([1, 3, 2])
        reduced = self.lattice.reduced(vector)
        cartesian = self.lattice.cartesian(reduced)
        assert np.allclose(cartesian, vector)


# %% ===================================================================== %% #
# %% hypothesis tests
@hp.given(data=st.data(), ntypes=st.integers(1, 50))
def test_UMDLattice_init(data, ntypes):
    """
    Test the __init__ function assignement operations.

    """
    data = data.draw(dataUMDLattice(ntypes))
    lattice = UMDLattice(**data)
    assert lattice.name == data['name']
    assert lattice.atoms == data['atoms']
    assert np.array_equal(lattice.dirBasis, data['basis'])
    assert np.array_equal(lattice.invBasis, np.linalg.inv(data['basis']))


@hp.given(data1=st.data(), data2=st.data())
def test_UMDLattice_eq(data1, data2):
    """
    Test the __eq__ function.

    """
    data1 = data1.draw(dataUMDLattice())
    data2 = data2.draw(dataUMDLattice())
    equal = (data1['atoms'] == data2['atoms']
             and np.array_equal(data1['basis'], data2['basis']))
    lattice1 = UMDLattice(**data1)
    lattice2 = UMDLattice(**data2)
    assert (lattice1 == lattice2) == equal


@hp.given(lattice=st.data(), vectors=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_reduced_shape(lattice, vectors, natoms):
    """
    Test the reduced function to convert vectors in cartesian coordinates to
    reduced coordiates refered to the lattice vector system.
    The set of vectors in reduced coordinates must conserve the shape.

    """
    lattice = lattice.draw(getUMDLattice())
    vectors = vectors.draw(getNumpyArray(natoms, 3))
    reduced = lattice.reduced(vectors)
    assert reduced.shape == vectors.shape


@hp.given(lattice=st.data(), vectors=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_cartesian_shape(lattice, vectors, natoms):
    """
    Test the cartesian function to convert vectors in cartesian coordiates
    to reduced coordinates refered to the lattice vector system.
    The set of vectors in cartesian coordinates must conserve the shape.

    """
    lattice = lattice.draw(getUMDLattice())
    vectors = vectors.draw(getNumpyArray(natoms, 3))
    cartesian = lattice.cartesian(vectors)
    assert cartesian.shape == vectors.shape


@hp.given(lattice=st.data())
def test_UMDLattice_reduced_basis(lattice):
    """
    Test the reduced function to convert vectors in cartesian coordiates to
    reduced coordinates refered to the lattice vector system.
    To test it, we assert that a matrix of basis vectors in cartesian
    coordinates must be equal to the identical matrix in reduced coordinates.

    """
    lattice = lattice.draw(getUMDLattice())
    reduced = lattice.reduced(lattice.dirBasis)
    assert np.allclose(reduced, np.identity(3))


@hp.given(lattice=st.data())
def test_UMDLattice_cartesian_basis(lattice):
    """
    Test the cartesian function to convert vectors in reduced coordinates
    refered to the lattice vector system to cartesian coordiates.
    To test it, we assert that an identical matrix in reduced coordinates
    must be equal to the matrix of basis vectors in cartesian coordinates.

    """
    lattice = lattice.draw(getUMDLattice())
    cartesian = lattice.cartesian(np.identity(3))
    assert np.allclose(cartesian, lattice.dirBasis)


@hp.given(lattice=st.data(), vectors=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_reduced_from_cartesian(lattice, vectors, natoms):
    """
    Test the reduced function to convert a set of vectors in cartesian
    coordiates to reduced coordinates refered to the lattice vector system.
    To test it, we assert that a vector in reduced coordinates must be
    equal (or close) to itself, when it is firts tranformed in cartesian
    coordinates and then back again into reduced coordinates.

    """
    lattice = lattice.draw(getUMDLattice())
    vectors = vectors.draw(getNumpyArray(natoms, 3))
    cartesian = lattice.cartesian(vectors)
    reduced = lattice.reduced(cartesian)
    assert np.allclose(reduced, vectors)


@hp.given(lattice=st.data(), vectors=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_cartesian_from_reduced(lattice, vectors, natoms):
    """
    Test the cartesian function to convert a set of vectors in reduced
    coordiates refered to the lattice vector system to cartesian
    coordinates.
    To test it, we assert that a vector in cartesian coordinates must be
    equal (or close) to itself, when it is firts tranformed in reduced
    coordinates and then back again into cartesian coordinates.

    """
    lattice = lattice.draw(getUMDLattice())
    vectors = vectors.draw(getNumpyArray(natoms, 3))
    reduced = lattice.reduced(vectors)
    cartesian = lattice.cartesian(reduced)
    assert np.allclose(cartesian, vectors)


@hp.given(lattice=st.data(), variations=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_periodic_shape(lattice, variations, natoms):
    """
    Test the periodic function to modify vector values according to the
    periodic boundary conditions.
    The periodic function must conserve the vector's shape.

    """
    lattice = lattice.draw(getUMDLattice())
    variations = variations.draw(getNumpyArray(natoms, 3))
    variations = lattice.periodic(variations)
    assert variations.shape == (natoms, 3)


@hp.given(lattice=st.data(), variations=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_periodic_value_reduced(lattice, variations, natoms):
    """
    Test the periodic function to modify vector values according to the
    periodic boundary conditions.
    If the values of the input vector are expressed in reduced coordinates,
    after the periodic function application, the array values must be all
    smaller than 0.5.

    """
    lattice = lattice.draw(getUMDLattice())
    variations = variations.draw(getNumpyArray(natoms, 3))
    variations = lattice.periodic(variations, False)
    assert np.all(np.abs(variations) <= 0.5)


@hp.given(lattice=st.data(), variations=st.data(), natoms=st.integers(1, 100))
def test_UMDLattice_periodic_value_cartesian(lattice, variations, natoms):
    """
    Test the periodic function to modify vector values according to the
    periodic boundary conditions.
    If the values of the input vector are expressed in cartesian coordinates,
    after the periodic function application, each array coordinate must be
    smaller than half of the sum of the basis vectors coordinates.

    """
    lattice = lattice.draw(getUMDLattice())
    variations = variations.draw(getNumpyArray(natoms, 3))
    variations = lattice.cartesian(variations)
    variations = lattice.periodic(variations, True)
    variations_limit = np.abs(np.sum(lattice.dirBasis, axis=0))
    for i in range(3):
        assert np.all(np.abs(variations[:, i]) <= 0.5*variations_limit[i])
