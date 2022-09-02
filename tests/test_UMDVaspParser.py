# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 23:23:54 2022

@author: marco
"""


from ..UMDVaspParser import UMDVaspParser

import os
import numpy as np

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class TestUMDVaspParser:
    
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

    def test_UMDVaspParser_single_nsteps(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of a single simulation run.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one expected.

        """
        simulation = UMDVaspParser('./examples/OUTCAR_single.outcar')
        assert simulation.cycle() == self.simulation_single.cycle()
        assert simulation.steps() == self.simulation_single.steps()
        assert simulation.time() == self.simulation_single.time()
        assert simulation.runs[0] == self.simulation_multiple.runs[0]
        os.remove('./examples/OUTCAR_single.umd')

    def test_UMDVaspParser_multiple_nsteps(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of multiple simulation runs concatenated.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one expected.

        """
        simulation = UMDVaspParser('./examples/OUTCAR_multiple.outcar')
        assert simulation.cycle() == self.simulation_multiple.cycle()
        assert simulation.steps() == self.simulation_multiple.steps()
        assert simulation.time() == self.simulation_multiple.time()
        for i in range(simulation.cycle()):
            assert simulation.runs[i] == self.simulation_multiple.runs[i]
        os.remove('./examples/OUTCAR_multiple.umd')