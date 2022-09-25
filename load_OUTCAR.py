"""
===============================================================================
                                 Load_OUTCAR
===============================================================================

This module provides the Load_OUTCAR namespace containing the functions
necessary to execute the UMDVaspParser function and stores the UMDVaspParser
parameters values.

Classes
-------
    Load_OUTCAR

SeeAlso
-------
    UMDVaspParser

"""

import numpy as np

from .libs.UMDSnapshot import UMDSnapshot
from .load_UMDSimulation_from_outcar import load_UMDSimulation_from_outcar

from .utils.decorator_ProgressBar import ProgressBar


class Load_OUTCAR:
    """
    Load_OUTCAR class to store functions and parameters for the UMDVaspParser.

    It contains the functions necessary to execute the UMDVaspParser function
    and stores the UMDVaspParser parameters values. The function implemented
    read data from the OUTCAR file and print them on a UMD file.

    Parameters
    ----------
    initialStep : int
        The index of the first snapshot to load.
        It is a UMDVaspParser function parameter and it is initialized by it.
    nSteps : int
        The total number of snapshots to load.
        It is a UMDVaspParser function parameter and it is initialized by it.
    finalStep : int
        The index of the last snapshot to load.
        It is calculated and updated for every simulation run.
    loadedSteps : int
        The total number of snapshot previously loaded.
        It is calculated and updated after every simulation run.

    Functions
    ---------
    reset
        Reset all the Load_OUTCAR parameters to their default values.
    load
        Convert the data of a simulation run from the OUTCAR to the UMD file.
    UMDSimulation_from_outcar
        Extract the parameters of a Vasp simulation run from the OUTCAR.
    UMDSnapshot_from_outcar
        Convert all the snapshots of a Vasp simulation run from the OUTCAR
        to the UMD file.

    """

    def __init__(self, initialStep=0, nSteps=np.infty):
        """
        Initialize a Load_OUTCAR instance with default parameters.

        Returns
        -------
        Load_OUTCAR object.

        """
        self.nSteps = nSteps
        self.initialStep = initialStep
        self.finalStep = 0
        self.loadedSteps = 0

    def load(self, outcar, umd, simulation):
        """
        Convert the data of a simulation run from the OUTCAR to the UMD file.

        The function is implemented in two functions:
        - UMDSimulation_from_outcar,
          to read the lattice structure and the simulation parameters which
          are fixed for every snapshot of the simulation.
          If it is not possible to initialize any UMDSimulation because all
          the OUTCAR file has already been read, then a EOFError is raised.
        - UMDSnapshot_from_outcar,
          to read each individual snapshots in the simulation run.
          The number of snapshots read depends on the number of iterations set
          among the simulation parameters.
          According to the current simulation run and the initialStep, the
          snapshot loading is managed by one of the following functions:
              - _run_before_initialStep
              - _run_around_initialStep
              - _run_after_initialStep

        Parameters
        ----------
        outcar : input file
            The OUTCAR file stream.
        umd : output file
            The UMD file stream.
        simulation : UMDSimulation
            The UMDSimulation object storing all the simulation information.

        Returns
        -------
        simulation : UMDsimulation
            The UMDSimulation object updated by the UMDSimulation_from_outcar
            function.

        Raises
        ------
        EOFError
            It raises a EOFError if all the OUTCAR file is read.

        """
        cycle = simulation.cycle()
        simulation = self.UMDSimulation_from_outcar(outcar, simulation)
        if simulation.cycle() == cycle+1:
            print('Loaded simulation run...')
            print(simulation.runs[-1])
            self.UMDSnapshot_from_outcar(outcar, umd, simulation)
        return simulation

    def UMDSimulation_from_outcar(self, outcar, simulation):
        """
        Extract the parameters of a Vasp simulation run from the OUTCAR.

        Parameters
        ----------
        outcar : input file
            The OUTCAR file stream.
        simulation : UMDSimulation
            The UMDSimulation object storing all the simulation information.

        Returns
        -------
        simulation : UMDsimulation
            The UMDSimulation object updated by the UMDSimulation_from_outcar
            function.

        Raises
        ------
        EOFError
            It raises a EOFError if all the OUTCAR file is read.

        """
        simulation = load_UMDSimulation_from_outcar(outcar, simulation)
        return simulation

    def UMDSnapshot_from_outcar(self, outcar, umd, simulation):
        """
        Convert all the snapshots of a Vasp simulation run from the OUTCAR
        to the UMD file.

        The UMDSnapshot objects are loaded from the OUTCAR file, converted
        and saved on the UMD file. The number of snapshots read depends on the
        number of iterations set among the simulation parameters.
        According to the current simulation run and the initialStep parameter,
        the snapshot loading is managed by one of the following functions:
            - _run_before_initialStep
            - _run_around_initialStep
            - _run_after_initialStep

        Parameters
        ----------
        outcar : input file
            The OUTCAR file stream.
        umd : output file
            The UMD file stream.
        simulation : UMDSimulation
            The UMDSimulation object storing all the simulation information.

        Returns
        -------
        None.

        """
        print('Loading snapshots ...')
        runSteps = simulation.runs[-1].steps
        self.finalStep = min(self.initialStep + self.nSteps,
                             self.loadedSteps+runSteps)
        if self.initialStep >= self.loadedSteps+runSteps:
            self._run_before_initialStep(outcar, simulation)
        elif self.initialStep > self.loadedSteps:
            self._run_around_initialStep(outcar, umd, simulation)
        else:
            self._run_after_initialStep(outcar, umd, simulation)
        self.loadedSteps += runSteps
        print(' ... {} snapshots saved.\n'.format(simulation.runs[-1].steps))

    @ProgressBar(length=20)
    def _run_before_initialStep(self, outcar, simulation):
        """
        Read the snapshots before the initialStep.

        The snapshots are read, but no UMDSnapshot object is built and saved.

        Parameters
        ----------
        outcar : input file
            The outcar file.
        simulation : UMDSimulation
            The current UMDSimulation.

        Yields
        ------
        float
            Ratio of the snapshot read.

        """
        print(range(self.loadedSteps, self.finalStep))
        for step in range(self.loadedSteps, self.finalStep):
            UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
            yield float(step-self.loadedSteps)/(self.finalStep-self.loadedSteps)
        simulation.runs[-1].steps = 0

    @ProgressBar(length=20)
    def _run_around_initialStep(self, outcar, umd, simulation):
        """
        Read and load the snapshots for initialStep in the current run.

        The snapshots before initialSteps are read, but no UMDSnapshot object
        is built and saved. The snapshots after initialSteps are read and for
        each a UMDSnapshot object is built and saved in the umd file.

        Parameters
        ----------
        outcar : input file
            The outcar file.
        umd : output file
            The umd file.
        simulation : UMDSimulation
            The current UMDSimulation.

        Yields
        ------
        float
            Ratio of the snapshot read.

        """
        run = simulation.runs[-1]
        for step in range(self.loadedSteps, self.initialStep):
            UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
            yield float(step-self.loadedSteps)/(self.finalStep-self.loadedSteps)
        for step in range(self.initialStep, self.finalStep):
            snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
            snapshot.UMDSnapshot_from_outcar(outcar)
            snapshot.save(umd)
            yield float(step-self.loadedSteps)/(self.finalStep-self.loadedSteps)
        simulation.runs[-1].steps = self.finalStep - self.initialStep

    @ProgressBar(length=20)
    def _run_after_initialStep(self, outcar, umd, simulation):
        """
        Read and load the snapshots after initialStep.

        All the snapshots after initialSteps in the simulation are read and for
        each a UMDSnapshot object is built and saved in the umd file.

        Parameters
        ----------
        outcar : input file
            The outcar file.
        umd : output file
            The umd file.
        simulation : UMDSimulation
            The current UMDSimulation.

        Yields
        ------
        float
            Ratio of the snapshot read.

        """
        run = simulation.runs[-1]
        for step in range(self.loadedSteps, self.finalStep):
            snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
            snapshot.UMDSnapshot_from_outcar(outcar)
            snapshot.save(umd)
            yield float(step-self.loadedSteps)/(self.finalStep-self.loadedSteps)
        simulation.runs[-1].steps = self.finalStep - self.loadedSteps
