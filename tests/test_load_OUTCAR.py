"""
===============================================================================
                               Load_OUTCAR tests
===============================================================================
"""

from ..load_OUTCAR import Load_OUTCAR

import os
import numpy as np
import unittest.mock as mock
import hypothesis as hp
import hypothesis.strategies as st

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun
from ..libs.UMDSnapshot import UMDSnapshot


class TestLoad_OUTCAR:

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)

    outcar_single = './examples/OUTCAR_single'
    outcar_multiple = './exampler/OUTCAR_multiple'

    @hp.given(loaded=st.integers(0), initial=st.integers(0),
              final=st.integers(0), n=st.integers(0))
    def test_Load_OUTCAR_reset(self, loaded, initial, final, n):
        """
        Test reset function to reset all the Load_OUTCAR parameters to their
        default value.

        """
        Load_OUTCAR.loadedSteps == loaded
        Load_OUTCAR.initialStep == initial
        Load_OUTCAR.finalStep == final
        Load_OUTCAR.nSteps = n
        Load_OUTCAR.reset()
        assert Load_OUTCAR.loadedSteps == 0
        assert Load_OUTCAR.initialStep == 0
        assert Load_OUTCAR.finalStep == 0
        assert Load_OUTCAR.nSteps == np.infty

    # %% _run_before_initialStep tests
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    def test_run_before_initialStep(self, mock_null, mock_load):
        """
        Test _run_before_initialStep function loading all the snapshots from a
        Vasp OUTCAR file containing a single simulation run.
        It must execute the UMDSnapshot method UMDSnapshot_from_outcar_null as
        many times as the total number of steps in the current
        UMDSimulationRun. The usual UMDSnapshot_from_outcar is never called.

        """
        Load_OUTCAR.reset()
        Load_OUTCAR.finalStep = 300
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open(self.outcar_single+'.outcar', 'r') as outcar:
            Load_OUTCAR._run_before_initialStep(outcar, simulation)
            assert mock_null.call_count == 300
            assert mock_load.call_count == 0
        # After the _run_before_initialStep call, the number of steps in the
        # last UMDSimulationRun must be 0.
        assert simulation.steps() == 0

    # %% _run_around_initialStep tests
    @mock.patch.object(UMDSnapshot, 'save')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    @hp.given(initialStep=st.integers(0, 300))
    def test_run_around_initialStep(self, initialStep, mock_null, mock_load,
                                    mock_save):
        """
        Test _run_around_initialStep function loading all the snapshots from a
        Vasp OUTCAR file containing a single simulation run.
        It must execute the UMDSnapshot method UMDSnapshot_from_outcar_null as
        many times as the initialStep and the usual UMDSnapshot_from_outcar
        ((UMDSimulationRun.steps)-initialStep) times.

        """
        Load_OUTCAR.reset()
        Load_OUTCAR.initialStep = initialStep
        Load_OUTCAR.finalStep = 300
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open(self.outcar_single+'.outcar', 'r') as outcar:
            with open(self.outcar_single+'.umd', 'w') as umd:
                Load_OUTCAR._run_around_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == initialStep
                assert mock_load.call_count == 300 - initialStep
                assert mock_save.call_count == 300 - initialStep
        # After the _run_around_initialStep call, the number of steps in the
        # last UMDSimulationRun must be ((UMDSimulationRun.steps)-initialStep).
        assert simulation.steps() == 300 - initialStep
        mock_null.reset_mock()
        mock_load.reset_mock()
        mock_save.reset_mock()
        os.remove(self.outcar_single+'.umd')

    # %% _run_after_initialStep tests
    @mock.patch.object(UMDSnapshot, 'save')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar')
    @mock.patch.object(UMDSnapshot, 'UMDSnapshot_from_outcar_null')
    def test_run_after_initialStep(self,  mock_null, mock_load,
                                          mock_save):
        """
        Test _run_after_initialStep function loading all the snapshots from a
        Vasp OUTCAR file containing a single simulation run.
        It must execute the UMDSnapshot method UMDSnapshot_from_outcar as many
        times as the total number of steps in the current UMDSimulationRun.
        The usual UMDSnapshot_from_outcar_null is never called.

        """
        Load_OUTCAR.reset()
        Load_OUTCAR.finalStep = 300
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open(self.outcar_single+'.outcar', 'r') as outcar:
            with open(self.outcar_single+'.umd', 'w') as umd:
                Load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
                assert mock_null.call_count == 0
                assert mock_load.call_count == 300
                assert mock_save.call_count == 300
        # After the _run_after_initialStep call, the number of steps in the
        # last UMDSimulationRun must be UMDSimulationRun.steps.
        assert simulation.steps() == 300
        os.remove('./examples/OUTCAR_single.umd')

    # %% UMDSnapshot_from_outcar tests
    @mock.patch.object(Load_OUTCAR, '_run_after_initialStep')
    @mock.patch.object(Load_OUTCAR, '_run_around_initialStep')
    @mock.patch.object(Load_OUTCAR, '_run_before_initialStep')
    @hp.given(initialStep=st.integers(0, 500))
    def test_UMDSnapshot_from_outcar_single(self, initialStep, mock_before,
                                            mock_around, mock_after):
        """
        Test _run_after_initialStep function loading all the snapshots from a
        Vasp OUTCAR file containing a single simulation run.
        It must call only one function among the _run_before_initialStep,
        _run_around_initialStep and _run_after_initialStep in agreement with
        the initialStep parameter.

        """
        Load_OUTCAR.reset()
        Load_OUTCAR.initialStep = initialStep
        run0 = UMDSimulationRun(0, 300, 0.5)
        simulation = UMDSimulation('', self.lattice, [run0])
        with open('./examples/OUTCAR_single.outcar', 'r') as outcar:
            with open('./examples/OUTCAR_single.umd', 'w') as umd:
                Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
                if initialStep == 0:
                    mock_before.assert_not_called()
                    mock_around.assert_not_called()
                    mock_after.assert_called_once()
                elif initialStep < 300:
                    mock_before.assert_not_called()
                    mock_around.assert_called_once()
                    mock_after.assert_not_called()
                else:
                    mock_before.assert_called_once()
                    mock_around.assert_not_called()
                    mock_after.assert_not_called()
                assert Load_OUTCAR.finalStep == 300
                assert Load_OUTCAR.loadedSteps == 300
        os.remove('./examples/OUTCAR_single.umd')
        mock_before.reset_mock()
        mock_around.reset_mock()
        mock_after.reset_mock()

    @mock.patch.object(Load_OUTCAR, '_run_after_initialStep')
    @mock.patch.object(Load_OUTCAR, '_run_around_initialStep')
    @mock.patch.object(Load_OUTCAR, '_run_before_initialStep')
    @hp.given(initialStep=st.integers(0, 2000))
    def test_UMDSnapshot_from_outcar_multiple(self, initialStep, mock_before,
                                              mock_around, mock_after):
        """
        Test UMDSnapshot_from_outcar function loading all the snapshots from a
        Vasp OUTCAR file containing multiple simulation runs concatenated.
        It must call _run_before_initialStep, _run_around_initialStep and
        _run_after_initialStep as many times as it is expected in agreement
        with the initialStep parameter.

        """
        Load_OUTCAR.reset()
        Load_OUTCAR.initialStep = initialStep
        run0 = UMDSimulationRun(0, 300, 0.5)
        run1 = UMDSimulationRun(1, 600, 0.5)
        run2 = UMDSimulationRun(2, 1000, 0.4)
        simulation = UMDSimulation('', self.lattice)
        with open('./examples/OUTCAR_multiple.outcar', 'r') as outcar:
            with open('./examples/OUTCAR_multiple.umd', 'w') as umd:
                # The UMDSnapshot_from_outcar is called once for each
                # simulation run update. The loadedSteps and finalStep 
                # parameters are updated at each function call.
                simulation.runs.append(run0)
                Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
                assert Load_OUTCAR.finalStep == 300
                assert Load_OUTCAR.loadedSteps == 300
                simulation.runs.append(run1)
                Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
                assert Load_OUTCAR.finalStep == 900
                assert Load_OUTCAR.loadedSteps == 900
                simulation.runs.append(run2)
                Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
                assert Load_OUTCAR.finalStep == 1900
                assert Load_OUTCAR.loadedSteps == 1900
                # According to the initialStep value, it is tested, the number
                # of times that each function is called.
                if initialStep == 0:
                    assert mock_before.call_count == 0
                    assert mock_around.call_count == 0
                    assert mock_after.call_count == 3
                elif initialStep < 300:
                    assert mock_before.call_count == 0
                    assert mock_around.call_count == 1
                    assert mock_after.call_count == 2
                elif initialStep == 300:
                    assert mock_before.call_count == 1
                    assert mock_around.call_count == 0
                    assert mock_after.call_count == 2
                elif initialStep < 900:
                    assert mock_before.call_count == 1
                    assert mock_around.call_count == 1
                    assert mock_after.call_count == 1
                elif initialStep == 900:
                    assert mock_before.call_count == 2
                    assert mock_around.call_count == 0
                    assert mock_after.call_count == 1
                elif initialStep < 1900:
                    assert mock_before.call_count == 2
                    assert mock_around.call_count == 1
                    assert mock_after.call_count == 0
                else:
                    assert mock_before.call_count == 3
                    assert mock_around.call_count == 0
                    assert mock_after.call_count == 0
        os.remove('./examples/OUTCAR_multiple.umd')
        mock_before.reset_mock()
        mock_around.reset_mock()
        mock_after.reset_mock()
