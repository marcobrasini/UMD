# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:08:28 2022

@author: marco
"""


import numpy as np

from .libs.UMDSnapshot import UMDSnapshot
from .load_UMDSimulation_from_outcar import load_UMDSimulation_from_outcar

from .decorator_ProgressBar import ProgressBar


class Load_OUTCAR:

    initialStep = 0
    finalStep = 0
    loadedSteps = 0
    nSteps = np.infty

    @staticmethod
    def reset():
        Load_OUTCAR.initialStep = 0
        Load_OUTCAR.finalStep = 0
        Load_OUTCAR.loadedSteps = 0
        Load_OUTCAR.nSteps = np.infty

    def UMDSimulation_from_outcar(outcar, simulation):
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

    def UMDSnapshot_from_outcar(outcar, umd, simulation):
        """
        Convert all the snapshot data of a Vasp simulation run from the OUTCAR
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
        loadedSteps = Load_OUTCAR.loadedSteps
        initialStep = Load_OUTCAR.initialStep
        nSteps = Load_OUTCAR.nSteps
        print('Loaded simulation run...')
        print(simulation.runs[-1])
        print('Loading snapshots ...')
        runSteps = simulation.runs[-1].steps
        Load_OUTCAR.finalStep = min(initialStep+nSteps, loadedSteps+runSteps)
        if initialStep > loadedSteps+runSteps:
            Load_OUTCAR._run_before_initialStep(outcar, simulation)
        elif initialStep > loadedSteps:
            Load_OUTCAR._run_around_initialStep(outcar, umd, simulation)
        else:
            Load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
        Load_OUTCAR.loadedSteps += runSteps
        print(' ... {} snapshots saved.\n'.format(simulation.runs[-1].steps))

    @staticmethod
    def load(outcar, umd, simulation):
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
        simulation = Load_OUTCAR.UMDSimulation_from_outcar(outcar, simulation)
        Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
        return simulation

    @ProgressBar(length=20)
    def _run_before_initialStep(outcar, simulation):
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
        run = simulation.runs[-1]
        loadedSteps = Load_OUTCAR.loadedSteps
        steps = run.steps
        for step in range(loadedSteps, loadedSteps + steps):
            UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
            yield float(step-loadedSteps)/steps
        simulation.runs[-1].steps = 0

    @ProgressBar(length=20)
    def _run_around_initialStep(outcar, umd, simulation):
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
        steps = run.steps
        loadedSteps = Load_OUTCAR.loadedSteps
        initialStep = Load_OUTCAR.initialStep
        finalStep = Load_OUTCAR.finalStep
        for step in range(loadedSteps, initialStep):
            UMDSnapshot.UMDSnapshot_from_outcar_null(outcar)
            yield float(step-loadedSteps)/steps
        for step in range(initialStep, loadedSteps+steps):
            snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
            snapshot.UMDSnapshot_from_outcar(outcar)
            snapshot.save(umd)
            yield float(step-loadedSteps)/steps
        simulation.runs[-1].steps = finalStep - initialStep

    @ProgressBar(length=20)
    def _run_after_initialStep(outcar, umd, simulation):
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
        steps = run.steps
        loadedSteps = Load_OUTCAR.loadedSteps
        finalStep = Load_OUTCAR.finalStep
        for step in range(loadedSteps, loadedSteps + steps):
            snapshot = UMDSnapshot(step, run.steptime, simulation.lattice)
            snapshot.UMDSnapshot_from_outcar(outcar)
            snapshot.save(umd)
            yield float(step-loadedSteps)/steps
        simulation.runs[-1].steps = finalStep - loadedSteps
