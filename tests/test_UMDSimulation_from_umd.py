"""
===============================================================================
                        UMDSimulation_from_umd tests
===============================================================================

To test UMDSimulation_from_umd we use three examples of UMD files:
 - the example/UMD_single.umd:
   It contains a single simulation run with 300 snapshots of 0.5 fs duration.
 - the example/UMD_multiple.umd:
   It containes three concatenated runs:
       - run0 with 300 snapshots of 0.5 fs duration.
       - run1 with 600 snapshots of 0.5 fs duration.
       - run2 with 1000 snapshots of 0.4 fs duration.
 - the examples/UMD_empty.umd:
   It contains no snapshot.

All simulations are performed on the same lattice structure:
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
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class Test_UMDSimulation_from_umd:
    # According to the lattice structure, we initialize the UMDLattice object
    # that we will use as reference for the test ...
    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)
    # ... and the UMDSimulationRun representing the simulation runs which are
    # concatenated in the OUTCAR file.
    run0 = UMDSimulationRun(0, 300, 0.5)
    run1 = UMDSimulationRun(1, 600, 0.5)
    run2 = UMDSimulationRun(2, 1000, 0.4)
    simulation_single = UMDSimulation('OUTCAR_single', lattice, [run0])
    simulation_multiple = UMDSimulation('OUTCAR_multiple', lattice,
                                        [run0, run1, run2])

    def test_UMDSimulation_from_umd_single(self):
        """
        Test the UMDSimualtion_from_umd loading the simulation from an OUTCAR
        file containing a single simulation run.

        """
        with open('examples/UMD_single.umd', 'r') as umd:
            simulation = UMDSimulation.UMDSimulation_from_umd(umd)
        assert simulation == self.simulation_single

    def test_UMDSimulation_from_umd_multiple(self):
        """
        Test the UMDSimualtion_from_umd loading the simualtion from an OUTCAR
        file containing multiple simulation runs concatenated.

        """
        with open('examples/UMD_multiple.umd', 'r') as umd:
            simulation = UMDSimulation.UMDSimulation_from_umd(umd)
        assert simulation == self.simulation_multiple

    def test_UMDSimulation_from_umd_eof(self):
        """
        Test the UMDSimualtion_from_umd when it reads an empty OUTCAR file.
        The function must return None.

        """
        with open('examples/UMD_empty.umd', 'r') as umd:
            simulation = UMDSimulation.UMDSimulation_from_umd(umd)
            assert simulation is None
