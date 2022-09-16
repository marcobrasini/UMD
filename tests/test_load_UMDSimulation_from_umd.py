"""
==============================================================================
                      UMDSimulation_from_outcar tests
==============================================================================

To test UMDSimulation_from_umd we use two examples of UMD files:
 - the example/UMD_single.umd:
   It contains a single simulation run with 300 snapshots of 0.5 fs duration.
 - the example/UMD_multiple.umd:
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


from ..load_UMDSimulation_from_umd import load_UMDSimulation_from_umd
from ..load_UMDSimulation_from_umd import load_UMDLattice_from_umd

import pytest
import numpy as np

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class Test_load_UMDSimulation_from_umd:

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    run0 = UMDSimulationRun(0, 300, 0.5)
    run1 = UMDSimulationRun(1, 600, 0.5)
    run2 = UMDSimulationRun(2, 1000, 0.4)

    simulation_single = UMDSimulation('', lattice, [run0])
    simulation_multiple = UMDSimulation('', lattice, [run0, run1, run2])

    def test_load_UMDLattice_from_umd(self):
        """
        Test the UMDLattice_from_umd function reading the lattice informations
        from a UMD file.

        """
        with open('./examples/UMD_single.umd', 'r') as umd:
            lattice = load_UMDLattice_from_umd(umd)
            assert lattice == self.lattice

    def test_UMDSimulation_from_umd_single(self):
        """
        Test the UMDSimulation_from_umd function for an UMD file containing
        a single simulation run.

        """
        with open('./examples/UMD_single.umd', 'r') as umd:
            simulation = load_UMDSimulation_from_umd(umd)
            assert simulation == self.simulation_single

    def test_UMDSimulation_from_umd_multiple(self):
        """
        Test the UMDSimulation_from_umd function for an UMD file containing
        multiple simulation runs concatenated.

        """
        with open('./examples/UMD_multiple.umd', 'r') as umd:
            simulation = load_UMDSimulation_from_umd(umd)
            assert simulation == self.simulation_multiple
