"""
==============================================================================
                      UMDSimulation_from_outcar tests
==============================================================================
To test UMDSimulation_from_outcar we use two examples of OUTCAR file:
 - the example/OUTCAR_single.outcar:
   It contains a single simulation run with 300 snapshots of 0.5 fs duration.
 - the example/OUTCAR_multiple.outcar:
   It containes three concatenated runs:
       - run0 with 300 snapshots of 0.5 fs duration.
       - run1 with 600 snapshots of 0.5 fs duration.
       - run2 with 1000 snapshots of 0.4 fs duration.

Both simulation is performed on the same lattice structure:
 - the matrix of basis vectors is:
       5.70     0.00     0.00
       0.00     5.70     0.00
       0.00     0.00     5.70
 - the contained atoms are:
     - O: 15 atoms,
     - H: 28 atoms,
     - Fe: 1 atom.

"""


from ..UMDSimulation_from_outcar import UMDSimulation_from_outcar

import numpy as np

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class TestUMDSimulation_from_outcar:
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
    runs = [run0, run1, run2]

    def test_UMDSimulation_from_outcar_single(self):
        """
        Test the UMDSimualtion_from_outcar when it reads the OUTCAR file of a
        single VASP simulation run (saved in the example/OUTCAR_single.outcar 
        file).

        """
        simulation = UMDSimulation()
        with open('examples/OUTCAR_single.outcar', 'r') as outcar:
            simulation = UMDSimulation_from_outcar(outcar, simulation)
            outcar.close()
        assert simulation.lattice == self.lattice
        assert simulation.runs[0] == self.run0
        assert simulation.cycle() == 1
        assert simulation.steps() == 300
        assert simulation.time() == 150

    def test_UMDSimulation_from_outcar_multiple(self):
        """
        Test the UMDSimualtion_from_outcar when it reads the OUTCAR file of
        multiple VASP simulation runs concatenated (saved in the 
        example/OUTCAR_multiple.outcar file).

        """
        total_simulation = UMDSimulation(lattice=self.lattice, runs=self.runs)
        simulation = UMDSimulation()
        with open('examples/OUTCAR_multiple.outcar', 'r') as outcar:
            while True:
                cycle = simulation.cycle()
                simulation = UMDSimulation_from_outcar(outcar, simulation)
                if simulation.cycle() == cycle:
                    break
            outcar.close()
        assert simulation == total_simulation
        assert simulation.lattice == self.lattice
        assert simulation.runs == self.runs
        assert simulation.cycle() == 3
        assert simulation.steps() == 1900
        assert simulation.time() == 850
