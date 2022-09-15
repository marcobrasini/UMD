"""
===============================================================================
                    UMDSnapshot.UMDSnapshot_from_outcar tests
==============================================================================

To test UMDSnapshot_from_outcar methods we use two examples of OUTCAR files:
 - the example/OUTCAR_single.outcar:
   It contains a single simulation run with 300 snapshots of 0.5 fs duration.
 - the example/OUTCAR_multiple.outcar:
   It containes three concatenated runs:
       - run0 with 300 snapshots of 0.5 fs duration.
       - run1 with 600 snapshots of 0.5 fs duration.
       - run2 with 1000 snapshots of 0.4 fs duration.

Both simulations are performed on the same lattice structure:
 - the matrix of basis vectors is:
       5.70     0.00     0.00
       0.00     5.70     0.00
       0.00     0.00     5.70
 - the contained atoms are:
     - O: 15 atoms,
     - H: 28 atoms,
     - Fe: 1 atom.
"""


import numpy as np
import pytest

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSnapshot import UMDSnapshot


class TestUMDSnapshot_from_outcar:
    # According to the lattice structure, we initialize the UMDLattice object
    # that we will use as reference for the test ...
    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    def test_UMDSnapshot_from_outcar_snapshot(self):
        """
        Test UMDSnapshot_from_outcar function loading a snapshot from an OUTCAR
        file containing a single snapshot. The load_UMDSnapshot_from_outcar
        must return the same UMDSnapshot updated.

        """
        with open('examples/OUTCAR_snapshot.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            snapshot = snapshot.UMDSnapshot_from_outcar(outcar)
            assert isinstance(snapshot, UMDSnapshot)
            outcar.close()

    def test_UMDSnapshot_from_outcar_null_snapshot(self):
        """
        Test UMDSnapshot_from_outcar_null function loading a snapshot from an
        OUTCAR file containing a single snapshot. The
        load_UMDSnapshot_from_outcar_null must return None.

        """
        with open('examples/OUTCAR_snapshot.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            snapshot = snapshot.UMDSnapshot_from_outcar_null(outcar)
            assert snapshot is None
            outcar.close()

    def test_UMDSnapshot_from_outcar_single(self):
        """
        Test UMDSnapshot_from_outcar function looking for a snapshot and then
        loading the snapshot from an OUTCAR file containing a single simulation
        run. The total number of snapshot call over all the OUTCAR file must be
        equal to the total simulation number of steps.

        """
        nsnapshots = 0
        with open('examples/OUTCAR_single.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            try:
                while True:
                    snapshot = snapshot.UMDSnapshot_from_outcar(outcar)
                    assert isinstance(snapshot, UMDSnapshot)
                    nsnapshots += 1
            except(EOFError):
                pass
            outcar.close()
        assert nsnapshots == 300

    def test_UMDSnapshot_from_outcar_null_single(self):
        """
        Test UMDSnapshot_from_outcar_null function looking for a snapshot and
        then loading the snapshot from an OUTCAR file containing a single
        simulation run. The total number of snapshot call over all the OUTCAR
        file must be equal to the total simulation number of steps.

        """
        nsnapshot = 0
        with open('examples/OUTCAR_single.outcar', 'r') as outcar:
            try:
                while True:
                    snapshot = UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
                    assert snapshot is None
                    nsnapshot += 1
            except(EOFError):
                pass
            outcar.close()
        assert nsnapshot == 300

    def test_UMDSnapshot_from_outcar_multiple(self):
        """
        Test UMDSnapshot_from_outcar function looking for a snapshot and then
        loading the snapshot from an OUTCAR file containing multiple simulation
        runs concatenated. The total number of snapshot loaded over all the
        OUTCAR file must be equal to the total simulation number of steps.

        """
        nsnapshots = 0
        with open('examples/OUTCAR_multiple.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            try:
                while True:
                    snapshot = snapshot.UMDSnapshot_from_outcar(outcar)
                    assert isinstance(snapshot, UMDSnapshot)
                    nsnapshots += 1
            except(EOFError):
                pass
            outcar.close()
        assert nsnapshots == 1900

    def test_UMDSnapshot_from_outcar_null_multiple(self):
        """
        Test UMDSnapshot_from_outcar_null function looking for a snapshot and
        then loading the snapshot from an OUTCAR file containing multiple
        simulation runs concatenated. The total number of snapshot loaded over
        all the OUTCAR file must be equal to the total simulation number of
        steps.

        """
        nsnapshots = 0
        with open('examples/OUTCAR_multiple.outcar', 'r') as outcar:
            try:
                while True:
                    snapshot = UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
                    assert snapshot is None
                    nsnapshots += 1
            except(EOFError):
                pass
            outcar.close()
        assert nsnapshots == 1900

    def test_load_UMDSnapshot_from_outcar_eof(self):
        """
        Test the UMDSnapshot_from_outcar when it reads an empty OUTCAR file.
        An EOFError is raised.

        """
        with open('examples/OUTCAR_empty.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.0, self.lattice)
            with pytest.raises(EOFError):
                snapshot = snapshot.UMDSnapshot_from_outcar(outcar, snapshot)
