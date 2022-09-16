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

In this module the UMDVapsParser is tested on the
example/OUTCAR_multiple.outcar.

See Also
--------
    UMDVaspParser
    test_UMDVaspParser_single

"""


from ..UMDVaspParser import UMDVaspParser
from ..load_UMDSimulation_from_umd import load_UMDSimulation_from_umd

import os
import filecmp
import numpy as np
import hypothesis as hp
import hypothesis.strategies as st

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSimulation import UMDSimulation
from ..libs.UMDSimulationRun import UMDSimulationRun


class TestUMDVaspParser_multiple:

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

    simulation = UMDSimulation('', lattice, [run0, run1, run2])

    def test_UMDVaspParser(self):
        """
        The UMDVaspParser must generate, from the OUTCARfile, a UMD file
        identical to './examples/UMD_multiple.umd'.

        """
        UMDVaspParser(self.file_multiple+'.outcar')
        assert filecmp.cmp('./examples/OUTCAR_multiple.umd',
                           './examples/UMD_multiple.umd')
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_multiple_nsteps(self):
        """
        Test UMDSimulation_from_outcar function when it reads all the snapshots
        from the OUTCAR file of a single simulation run.
        The UMDVaspParser must return a UMDSimulation object identical to the
        one expected.

        """
        simulation = UMDVaspParser(self.file_multiple+'.outcar')
        assert simulation == self.simulation
        os.remove(self.file_multiple+'.umd')

    # %% UMDVaspParser initialStep argument tests
    def test_UMDVaspParser_initialStep_run0(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, starting from an initial
        snapshots, nStep, in run0.

        """
        initialStep = 100
        simulation = UMDVaspParser(self.file_multiple+'.outcar',
                                   initialStep=initialStep)
        assert simulation.runs[0].steps == self.run0.steps - initialStep
        assert simulation.runs[1] == self.run1
        assert simulation.runs[2] == self.run2
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_initialStep_run1(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, starting from an initial
        snapshots, nStep, in run1.

        """
        initialStep = 450
        simulation = UMDVaspParser(self.file_multiple+'.outcar',
                                   initialStep=initialStep)
        assert simulation.runs[0].steps == 0
        runSteps = initialStep-self.run0.steps
        assert simulation.runs[1].steps == self.run1.steps - runSteps
        assert simulation.runs[2] == self.run2
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_initialStep_run2(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, starting from an initial
        snapshots, nStep, in run2.

        """
        initialStep = 1450
        simulation = UMDVaspParser(self.file_multiple+'.outcar',
                                   initialStep=initialStep)
        assert simulation.runs[0].steps == 0
        assert simulation.runs[1].steps == 0
        runSteps = initialStep-self.run0.steps-self.run1.steps
        assert simulation.runs[2].steps == (self.run2.steps-runSteps)
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_initialStep_toolarge(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, starting from an initial
        snapshots, nStep, too large.

        """
        initialStep = 1950
        simulation = UMDVaspParser(self.file_multiple+'.outcar',
                                   initialStep=initialStep)
        assert simulation.runs[0].steps == 0
        assert simulation.runs[1].steps == 0
        assert simulation.runs[2].steps == 0
        os.remove(self.file_multiple+'.umd')

    @hp.settings(max_examples=10, deadline=None)
    @hp.given(initialStep=st.integers(0, 2500))
    def test_UMDVaspParser_initialStep(self, initialStep):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, starting from a generic initial
        snapshots, nStep.

        """
        simulation = UMDVaspParser(self.file_multiple+'.outcar',
                                   initialStep=initialStep)
        totalSteps = 0
        totalTime = 0.
        for i in range(3):
            runSteps = self.simulation.runs[i].steps
            stepTime = self.simulation.runs[i].steptime
            totalSteps += runSteps
            if initialStep > totalSteps:
                assert simulation.runs[i].steps == 0
            elif initialStep > totalSteps-runSteps:
                assert simulation.runs[i].steps == totalSteps-initialStep
                totalTime += (totalSteps-initialStep)*stepTime
            else:
                assert simulation.runs[i] == self.simulation.runs[i]
                totalTime += self.simulation.runs[i].time()
        assert simulation.steps() == max(self.simulation.steps()-initialStep,0)
        assert np.isclose(simulation.time(), totalTime)
        os.remove(self.file_multiple+'.umd')

    # %% UMDVaspParser nSteps argument tests
    def test_UMDVaspParser_nSteps_run0(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, loading a number of snapshots,
        nStep, up to run0.

        """
        nSteps = 100
        simulation = UMDVaspParser(self.file_multiple+'.outcar', nSteps=nSteps)
        assert simulation.runs[0].steps == nSteps
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_nSteps_run1(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, loading a number of snapshots,
        nStep, up to run1.

        """
        nSteps = 450
        simulation = UMDVaspParser(self.file_multiple+'.outcar', nSteps=nSteps)
        assert simulation.runs[0] == self.run0
        runSteps = nSteps - self.run0.steps
        assert simulation.runs[1].steps == runSteps
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_nSteps_run2(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, loading a number of snapshots,
        nStep, up to run2.

        """
        nSteps = 1450
        simulation = UMDVaspParser(self.file_multiple+'.outcar', nSteps=nSteps)
        assert simulation.runs[0] == self.run0
        assert simulation.runs[1] == self.run1
        runSteps = nSteps - (self.run1.steps + self.run0.steps)
        assert simulation.runs[2].steps == runSteps
        os.remove(self.file_multiple+'.umd')

    def test_UMDVaspParser_nSteps_toolarge(self):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, loading a number of snapshots,
        nStep, too large.

        """
        nSteps = 1950
        simulation = UMDVaspParser(self.file_multiple+'.outcar', nSteps=nSteps)
        assert simulation == self.simulation
        os.remove(self.file_multiple+'.umd')

    @hp.settings(max_examples=10, deadline=None)
    @hp.given(nSteps=st.integers(0, 2500))
    def test_UMDVaspParser_nSteps(self, nSteps):
        """
        Test UMDVaspParser function when it reads data from the OUTCAR file
        containing multiple simulation runs, loading a generic number of
        snapshots, nStep.

        """
        simulation = UMDVaspParser(self.file_multiple+'.outcar', nSteps=nSteps)
        totalSteps = 0
        totalTime = 0.
        for i in range(3):
            runSteps = self.simulation.runs[i].steps
            stepTime = self.simulation.runs[i].steptime
            if nSteps > totalSteps+runSteps:
                assert simulation.runs[i] == self.simulation.runs[i]
                totalTime += self.simulation.runs[i].time()
            elif nSteps >= totalSteps:
                assert simulation.runs[i].steps == nSteps-totalSteps
                totalTime += (nSteps-totalSteps)*stepTime
                break
            else:
                assert simulation.runs[i].steps == 0
            totalSteps += runSteps
        assert simulation.steps() == min(nSteps, self.simulation.steps())
        assert np.isclose(simulation.time(), totalTime)
        os.remove(self.file_multiple+'.umd')
