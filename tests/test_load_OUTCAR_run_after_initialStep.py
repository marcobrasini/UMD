"""
===============================================================================
                     Load_OUTCAR._run_after_initialStep tests
===============================================================================
"""


from ..load_OUTCAR import Load_OUTCAR 

import os
import numpy as np
import unittest.mock as mock

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun
from ..libs.UMDSnapshot import UMDSnapshot


class TestLoad_OUTCAR_run_after_initialStep:
    """
    Test the _run_after_initialStep function in the Load_OUTCAR class.

    """
    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    @mock.patch.object(UMDSnapshot, 'save')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    def test_run_after_initialStep_single(self,  mock_null, mock_load,
                                          mock_save):
        """
        Test _run_after_initialStep function executing the UMDSnapshot method
        UMDSnapshot_from_outcar as many times as the number of steps in the
        current simulation run. The usual UMDSnapshot_from_outcar_null is never
        called.
        For an OUTCAR file containing a single simulation run, the function
        call operates over all the simulation steps.

        """
        load_OUTCAR = Load_OUTCAR()
        load_OUTCAR.finalStep = 300
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open('./examples/OUTCAR_single.outcar', 'r') as outcar:
            with open('./examples/OUTCAR_single.umd', 'w') as umd:
                load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == 0
                assert mock_load.call_count == 300
                assert mock_save.call_count == 300
        # After the _simulation_after_initialStep call the number of steps
        # in the last UMDSimulationRun must be 300.
        assert simulation.steps() == 300
        os.remove('./examples/OUTCAR_single.umd')

    @mock.patch.object(UMDSnapshot, 'save')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    def test_run_after_initialStep_multiple(self, mock_null, mock_load,
                                            mock_save):
        """
        Test _run_after_initialStep function executing the UMDSnapshot method
        UMDSnapshot_from_outcar as many times as the number of steps in the
        current simulation run. The usual UMDSnapshot_from_outcar_null is never
        called.
        For an OUTCAR file containing multiple simulation runs concatenated,
        the function call operates only over the last simulation run.

        """
        load_OUTCAR = Load_OUTCAR()
        run0 = UMDSimulationRun(0, 300, 0.5)
        run1 = UMDSimulationRun(1, 600, 0.5)
        run2 = UMDSimulationRun(2, 1000, 0.4)
        simulation = UMDSimulation('', self.lattice)
        with open('./examples/OUTCAR_multiple.outcar', 'r') as outcar:
            with open('./examples/OUTCAR_multiple.umd', 'w') as umd:
                # apply the _simulation_before_initialStep to load the run 0
                simulation.runs.append(run0)
                load_OUTCAR.finalStep = 300
                load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == 0
                assert mock_load.call_count == 300
                assert mock_save.call_count == 300
                assert simulation.runs[0].steps == 300
                # apply the _simulation_before_initialStep to load the run 1
                simulation.runs.append(run1)
                load_OUTCAR.loadedSteps = 300
                load_OUTCAR.finalStep = 900
                load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == 0
                assert mock_load.call_count == 900
                assert mock_save.call_count == 900
                assert simulation.runs[1].steps == 600
                # apply the _simulation_before_initialStep to load the run 2
                simulation.runs.append(run2)
                load_OUTCAR.loadedSteps = 900
                load_OUTCAR.finalStep = 1900
                load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == 0
                assert mock_load.call_count == 1900
                assert mock_save.call_count == 1900
                assert simulation.runs[2].steps == 1000
        # After the multiple _simulation_before_initialStep calls the total
        # number of steps in the total UMDSimulation must be 0.
        assert simulation.steps() == 1900
        os.remove('./examples/OUTCAR_multiple.umd')
