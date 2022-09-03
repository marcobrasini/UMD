# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 23:23:54 2022

@author: marco
"""


from ..UMDVaspParser import UMDVaspParser
from ..UMDSimulation_from_umd import UMDSimulation_from_umd

import os
import numpy as np

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class TestUMDVaspParser:
    
    file_single = './examples/OUTCAR_single'
    file_multiple = './examples/OUTCAR_multiple'
    
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
        simulation = UMDVaspParser(self.file_single+'.outcar')
        assert simulation == self.simulation_single
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_multiple_nsteps(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of a single simulation run.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one expected.

        """
        simulation = UMDVaspParser(self.file_multiple+'.outcar')
        assert simulation == self.simulation_multiple
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_single_simulation_from_umd(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of multiple simulation runs concatenated.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one read back from the UMD file.

        """
        simulation = UMDVaspParser(self.file_single+'.outcar')
        with open(self.file_single+'.umd', 'r') as umd:
            simulation_umd = UMDSimulation_from_umd(umd)
            assert simulation == simulation_umd
            umd.close()
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_multiple_simulation_from_umd(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of multiple simulation runs concatenated.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one read back from the UMD file.

        """
        simulation = UMDVaspParser(self.file_multiple+'.outcar')
        with open(self.file_multiple+'.umd', 'r') as umd:
            simulation_umd = UMDSimulation_from_umd(umd)
            assert simulation == simulation_umd
            umd.close()
        os.remove(self.file_multiple+'.umd')
