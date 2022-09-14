# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:19:32 2022

@author: marco
"""


from ..load_UMDSimulationRun import _simulation_before_initialStep

import os
import numpy as np
import unittest.mock as mock

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun
from ..libs.UMDSnapshot import UMDSnapshot


class Test_simulation_before_initialStep:

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    def test_simulation_before_initialStep_single(self, mock, mock_null):
        """
        Test _simulation_before_initialStep function executing the UMDSnapshot
        method UMDSnapshot_from_outcar_null as many times as the number of
        steps in the current simulation run. The usual UMDSnapshot_from_outcar
        is never called.
        For an OUTCAR file containing a single simulation run, the function
        call operates over all the simulation steps.

        """
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open('./examples/OUTCAR_single.outcar') as outcar:
            _simulation_before_initialStep(outcar, simulation)
            assert mock.call_count == 0
            assert mock_null.call_count == 300
            outcar.close()
        # After the _simulation_before_initialStep call the number of steps
        # in the last UMDSimulationRun must be 0.
        assert simulation.steps() == 0

    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    def test_simulation_before_initialStep_multiple(self, mock, mock_null):
        """
        Test _simulation_before_initialStep function executing the UMDSnapshot
        method UMDSnapshot_from_outcar_null as many times as the number of
        steps in the current simulation run. The usual UMDSnapshot_from_outcar
        is never called.
        For an OUTCAR file containing multiple simulation runs concatenated,
        the function call operates only over the last simulation run.

        """
        run0 = UMDSimulationRun(0, 300, 0.5)
        run1 = UMDSimulationRun(1, 600, 0.5)
        run2 = UMDSimulationRun(2, 1000, 0.4)
        simulation = UMDSimulation('', self.lattice)
        with open('./examples/OUTCAR_multiple.outcar') as outcar:
            # apply the _simulation_before_initialStep to load the run 0
            simulation.runs.append(run0)
            _simulation_before_initialStep(outcar, simulation)
            assert mock.call_count == 0
            assert mock_null.call_count == 300
            assert simulation.runs[0].steps == 0
            # apply the _simulation_before_initialStep to load the run 1
            simulation.runs.append(run1)
            _simulation_before_initialStep(outcar, simulation)
            assert mock.call_count == 0
            assert mock_null.call_count == 900
            assert simulation.runs[1].steps == 0
            # apply the _simulation_before_initialStep to load the run 2
            simulation.runs.append(run2)
            _simulation_before_initialStep(outcar, simulation)
            assert mock.call_count == 0
            assert mock_null.call_count == 1900
            assert simulation.runs[2].steps == 0
            outcar.close()
        # After the multiple _simulation_before_initialStep calls the total
        # number of steps in the total UMDSimulation must be 0.
        assert simulation.steps() == 0


