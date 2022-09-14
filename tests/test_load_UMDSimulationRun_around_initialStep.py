# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 18:29:39 2022

@author: marco
"""


from ..load_UMDSimulationRun import _simulation_around_initialStep
from ..load_UMDSimulationRun import _param_

import os
import numpy as np
import unittest.mock as mock

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun
from ..libs.UMDSnapshot import UMDSnapshot


class Test_simulation_around_initialStep:

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'save')
    def test_simulation_around_initialStep_single(self, mock_save,
                                                  mock_load, mock_null):
        """
        Test _simulation_around_initialStep function executing the UMDSnapshot
        method UMDSnapshot_from_outcar_null as many times as initialStep and
        the usual UMDSnapshot_from_outcar (simulation run steps) - initialStep
        times.
        For an OUTCAR file containing a single simulation run, the function
        call operates over all the simulation steps.

        """
        _param_._initialStep = 100
        _param_._finalStep = 300
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open('./examples/OUTCAR_single.outcar', 'r') as outcar:
            with open('./examples/OUTCAR_single.umd', 'w') as umd:
                _simulation_around_initialStep(outcar, umd, simulation)
                assert mock_save.call_count == 200
                assert mock_load.call_count == 200
                assert mock_null.call_count == 100
                umd.close()
            outcar.close()
        # After the _simulation_before_initialStep call the number of steps
        # in the last UMDSimulationRun must be 0.
        print(simulation)
        assert simulation.steps() == 200
        os.remove('./examples/OUTCAR_single.umd')
