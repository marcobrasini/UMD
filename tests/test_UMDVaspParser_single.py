"""
==============================================================================
                              UMDVaspParser tests
==============================================================================

To test UMDVaspParser we use two examples of OUTCAR files:
 - the example/OUTCAR_single.outcar:
   It contains a single simulation run with 300 snapshots of 0.5 fs duration.
 - the example/OUTCAR_multiple.outcar:
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

In this module the UMDVapsParser is tested on the example/OUTCAR_single.outcar.

See Also
--------
    UMDVaspParser
    test_UMDVaspParser_multiple

"""


from ..UMDVaspParser import UMDVaspParser

import os
import filecmp
import numpy as np

import pytest
import hypothesis as hp
import hypothesis.strategies as st

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class TestUMDVaspParser_single:
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

    run0 = UMDSimulationRun(0, 300, 0.5)
    simulation = UMDSimulation('', lattice, [run0])

    def test_UMDVaspParser(self):
        """
        The UMDVaspParser must generate, from the OUTCARfile, a UMD file
        identical to './examples/UMD_single.umd'.

        """
        UMDVaspParser(self.file_single+'.outcar')
        assert filecmp.cmp('./examples/OUTCAR_single.umd',
                           './examples/UMD_single.umd')
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_nsteps(self):
        """
        The UMDVaspParser must return a UMDSimulation object identical to the
        one expected.

        """
        simulation = UMDVaspParser(self.file_single+'.outcar')
        assert simulation == self.simulation
        os.remove(self.file_single+'.umd')

    # %% UMDVaspParser initialStep argument tests
    def test_UMDVaspParser_initialStep_correct(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, starting from a correct initial
        snapshot, initialStep.

        """
        initialStep = 120
        totalSteps = self.simulation.steps()                           # 300
        stepTime = self.simulation.runs[0].steptime                    # 0.5
        simulation = UMDVaspParser(self.file_single+'.outcar',
                                   initialStep=initialStep)
        assert simulation.cycle() == 1
        assert simulation.steps() == totalSteps-initialStep            # 180
        assert simulation.time() == (totalSteps-initialStep)*stepTime  # 90.0
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_initialStep_toolarge(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, starting from a too large initial
        snapshot, initialStep.

        """
        initialStep = 360
        simulation = UMDVaspParser(self.file_single+'.outcar',
                                   initialStep=initialStep)
        assert simulation.cycle() == 1
        assert simulation.steps() == 0
        assert simulation.time() == 0.
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_initialStep_error_negative(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, starting from a negative initial
        snapshot, initialStep.
        If the initialStep is negative a ValueError must be raised.

        """
        with pytest.raises(ValueError):
            UMDVaspParser(self.file_single+'.outcar', initialStep=-1)

    @hp.settings(max_examples=10, deadline=None)
    @hp.given(initialStep=st.integers(0, 500))
    def test_UMDVaspParser_initialStep(self, initialStep):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, starting from a generic initial
        snapshot, initialStep.

        """
        totalSteps = self.simulation.steps()
        snapTime = self.simulation.runs[0].steptime
        simulation = UMDVaspParser(self.file_single+'.outcar',
                                   initialStep=initialStep)
        assert simulation.steps() == max(0, totalSteps-initialStep)
        assert simulation.time() == max(0, totalSteps-initialStep)*snapTime
        os.remove(self.file_single+'.umd')

    # %% UMDVaspParser nSteps argument tests
    def test_UMDVaspParser_nStep_correct(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, loading a correct number of
        snapshots, nStep.

        """
        nSteps = 120
        stepTime = self.simulation.runs[0].steptime                    # 0.5
        simulation = UMDVaspParser(self.file_single+'.outcar', nSteps=nSteps)
        assert simulation.cycle() == 1
        assert simulation.steps() == nSteps                            # 120
        assert simulation.time() == nSteps*stepTime                    # 60.0
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_nStep_toolarge(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, loading a too large number of
        snapshots, nStep.

        """
        nSteps = 360
        simulation = UMDVaspParser(self.file_single+'.outcar', nSteps=nSteps)
        assert simulation.cycle() == 1
        assert simulation.steps() == self.simulation.steps()           # 300
        assert simulation.time() == self.simulation.time()             # 150.0
        os.remove(self.file_single+'.umd')

    def test_UMDVaspParser_nSteps_error_negative(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, loading a negative number of
        snapshots, nStep.
        If the nSteps is negative a ValueError must be raised.

        """
        with pytest.raises(ValueError):
            UMDVaspParser(self.file_single+'.outcar', nSteps=-1)

    @hp.settings(max_examples=10, deadline=None)
    @hp.given(nSteps=st.integers(0, 500))
    def test_UMDVaspParser_nStep(self, nSteps):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, loading a generic number of
        snapshots, nStep.

        """
        totalSteps = self.simulation.steps()
        snapTime = self.simulation.runs[0].steptime
        simulation = UMDVaspParser(self.file_single+'.outcar', nSteps=nSteps)
        assert simulation.steps() == min(nSteps, totalSteps)
        assert simulation.time() == min(nSteps, totalSteps)*snapTime
        os.remove(self.file_single+'.umd')

    # %% UMDVaspParser arguments tests
    @hp.settings(max_examples=50, deadline=None)
    @hp.given(initialStep=st.integers(0, 500), nSteps=st.integers(0, 500))
    def test_UMDVaspParser_initialStep_nSteps(self, initialStep, nSteps):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing a single simulation run, starting for a generic initial
        snapshot, initialStep, and loading a generic number of snapshots,
        nSteps.

        """
        totalSteps = self.simulation.steps()
        snapTime = self.simulation.runs[0].steptime
        simulation = UMDVaspParser(self.file_single+'.outcar',
                                   initialStep=initialStep, nSteps=nSteps)
        totalSteps = max(0, totalSteps-initialStep)
        nSteps = min(totalSteps, nSteps)
        assert simulation.cycle() == 1
        assert simulation.steps() == nSteps
        assert simulation.time() == nSteps*snapTime
        os.remove(self.file_single+'.umd')
