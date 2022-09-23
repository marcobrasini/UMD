# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 01:06:36 2022

@author: marco
"""

from ..UMDVaspParser import UMDVaspParser
from ..load_UMDSimulation_from_outcar import load_UMDSimulation_from_outcar
from ..load_UMDSimulation_from_umd import load_UMDSimulation_from_umd

import os
import numpy as np

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSnapshot import UMDSnapshot
from ..libs.UMDSimulation import UMDSimulation


class Test_UMD_from_OUTCAR:
    """
    Test UMDVaspParser function when it reads data from the OUTCAR file
    containing a single simulation run.

    """

    file_single = './examples/OUTCAR_single'

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    # %% UMD-OUTCAR simualtion conversion tests by UMDVaspParser
    def test_UMD_from_OUTCAR_UMDSimulation_single_with_UMDVaspParser(self):
        """
        Test UMDVaspParser function loading all snapshots from an OUTCAR file
        containing a single simulation run. The UMDVaspParser must return a
        UMDSimulation object identical to the one read back by the
        UMDSimulation_from_umd function from the UMD file generated.

        """
        simulationOUTCAR = UMDVaspParser('./examples/OUTCAR_single.outcar')
        with open('./examples/OUTCAR_single.umd', 'r') as umd:
            simulationUMD = load_UMDSimulation_from_umd(umd)
            assert simulationOUTCAR == simulationUMD
            umd.close()
        os.remove('./examples/OUTCAR_single.umd')

    def test_UMD_from_OUTCAR_UMDSimulation_multiple_with_UMDVaspParser(self):
        """
        Test UMDVaspParser function loading all snapshots from an OUTCAR file
        containing multiple simulation runs concatenated. The UMDVaspParser
        must return a UMDSimulation object identical to the one read back by
        the UMDSimulation_from_umd function from the UMD file generated.

        """
        simulationOUTCAR = UMDVaspParser('./examples/OUTCAR_multiple.outcar')
        with open('./examples/OUTCAR_multiple.umd', 'r') as umd:
            simulationUMD = load_UMDSimulation_from_umd(umd)
            assert simulationOUTCAR == simulationUMD
            umd.close()
        os.remove('./examples/OUTCAR_multiple.umd')

    def test_UMD_from_OUTCAR_UMDSimulation_single(self):
        """
        Test UMDSimulation_from_outcar and UMDSimulation_from_umd functions
        when they extract the simulation parameter from an OUTCAR file 
        containing a single simulation run and its corrspondent UMD file.
        The simulation returned by the two functions must be equal.

        """
        with open('./examples/OUTCAR_single.outcar', 'r') as outcar:
            simulation = UMDSimulation('OUTCAR_single', self.lattice)
            try:
                while True:
                    simualtion = load_UMDSimulation_from_outcar(outcar,
                                                                simulation)
            except(EOFError):
                pass
            with open('./examples/UMD_single.umd', 'r') as umd:
                simulationUMD = load_UMDSimulation_from_umd(umd)
                assert simulation == simulationUMD

    def test_UMD_from_OUTCAR_UMDSimulation_multiple(self):
        """
        Test UMDSimulation_from_outcar and UMDSimulation_from_umd functions
        when they extract the simulation parameter from an OUTCAR file 
        containing a single simulation run and its corrspondent UMD file.
        The simulation returned by the two functions must be equal.

        """
        with open('./examples/OUTCAR_multiple.outcar', 'r') as outcar:
            simulation = UMDSimulation('OUTCAR_multiple', self.lattice)
            try:
                while True:
                    simualtion = load_UMDSimulation_from_outcar(outcar,
                                                                simulation)
            except(EOFError):
                pass
            with open('./examples/UMD_multiple.umd', 'r') as umd:
                simulationUMD = load_UMDSimulation_from_umd(umd)
                assert simulation == simulationUMD
        
    # %% UMD-OUTCAR snapshot conversion tests
    def test_UMD_from_OUTCAR_UMDSnapshot_single(self):
        """
        Test UMDSnapshot_from_outcar and UMDSnapshot_from_umd functions when
        they read respectively all the snapshots from an OUTCAR file containing
        a single simulation run and its corrspondent UMD file.
        At each iteration, the snapshots returned by the two functions must
        be equal.

        """
        snap = 0
        with open('./examples/OUTCAR_single.outcar', 'r') as outcar:
            with open('./examples/UMD_single.umd', 'r') as umd:
                try:
                    while True:
                        snapOUTCAR = UMDSnapshot(snap, 0.5, self.lattice)
                        snapOUTCAR.UMDSnapshot_from_outcar(outcar)
                        snapUMD = UMDSnapshot(lattice=self.lattice)
                        snapUMD.UMDSnapshot_from_umd(umd)
                        assert snapOUTCAR == snapUMD
                        snap += 1
                except(EOFError):
                    pass
                umd.close()
            outcar.close()

    def test_UMD_from_OUTCAR_UMDSnapshot_multiple(self):
        """
        Test UMDSnapshot_from_outcar and UMDSnapshot_from_umd functions when
        they read respectively all the snapshots from an OUTCAR file containing
        multiple simulation runs concatenated and its corrspondent UMD file.
        At each iteration, the snapshots returned by the two functions must
        be equal.

        """
        snap = 0
        with open('./examples/OUTCAR_multiple.outcar', 'r') as outcar:
            with open('./examples/UMD_multiple.umd', 'r') as umd:
                try:
                    while True:
                        snapOUTCAR = UMDSnapshot(snap, lattice=self.lattice)
                        if snap < 900:
                            snapOUTCAR.time = 0.5
                        else:
                            snapOUTCAR.time = 0.4
                        snapOUTCAR.UMDSnapshot_from_outcar(outcar)
                        snapUMD = UMDSnapshot(lattice=self.lattice)
                        snapUMD.UMDSnapshot_from_umd(umd)
                        assert snapOUTCAR == snapUMD
                        snap += 1
                except(EOFError):
                    pass
                umd.close()
            outcar.close()
