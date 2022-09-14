"""
==============================================================================
                        UMDSnapshot_from_outcar tests
==============================================================================

To test UMDSnapshot_from_outcar we use two examples of OUTCAR files:
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
import hypothesis as hp

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

    def test_UMDSnapshot_from_outcar_single(self):
        nsnapshot = 0
        with open('examples/OUTCAR_single.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            while True:
                snapshot = snapshot.UMDSnapshot_from_outcar(outcar)
                print(snapshot)
                if snapshot is None:
                    break
                nsnapshot += 1
            outcar.close()
        assert nsnapshot == 300

    def test_UMDSnapshot_from_outcar_multiple(self):
        nsnapshot = 0
        with open('examples/OUTCAR_multiple.outcar', 'r') as outcar:
            snapshot = UMDSnapshot(0, 0.5, self.lattice)
            while True:
                snapshot = snapshot.UMDSnapshot_from_outcar(outcar)
                if snapshot is None:
                    break
                nsnapshot += 1
            outcar.close()
        assert nsnapshot == 1900
