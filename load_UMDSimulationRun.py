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

    def reset():
        Load_OUTCAR.initialStep = 0
        Load_OUTCAR.finalStep = 0
        Load_OUTCAR.LoadedSteps = 0
        Load_OUTCAR.nSteps = np.infty

    def UMDSimulation_from_outcar(outcar, simulation):
        simulation = load_UMDSimulation_from_outcar(outcar, simulation)
        return simulation

    def UMDSnapshot_from_outcar(outcar, umd, simulation):
        loadedSteps = Load_OUTCAR.loadedSteps
        initialStep = Load_OUTCAR.initialStep
        nSteps = Load_OUTCAR.nSteps

        print('Loaded simulation run...')
        print(simulation.runs[-1])
        print('Loading snapshots ...')
        runSteps = simulation.runs[-1].steps
        Load_OUTCAR.finalStep = min(initialStep+nSteps, loadedSteps+runSteps)
        if initialStep > loadedSteps+runSteps:
            print('before')
            Load_OUTCAR._run_before_initialStep(outcar, simulation)
        elif initialStep > loadedSteps:
            print('around')
            Load_OUTCAR._run_around_initialStep(outcar, umd, simulation)
        else:
            print('after')
            Load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
        Load_OUTCAR.loadedSteps += runSteps
        print(' ... {} snapshots saved.\n'.format(simulation.runs[-1].steps))

    @staticmethod
    def load_UMDSimulationRun(outcar, umd, simulation):
        """
        Convert the data of a simulation run from the OUTCAR to the UMD file.

        The function is implemented in two functions:
        - UMDSimulation_from_outcar,
          to read the lattice structure and the simulation parameters which
          are fixed for every snapshot of the simulation.
          If no UMDSimulation is initialized, then None is returned.
        - UMDSnapshot_from_outcar,
          to read each individual snapshots in the simulation.
          The number of snapshots read depends on the number of iterations set
          among the simulation parameters.
          According to the current simulation cycle and the initialStep, the
          snapshots are managed by one of the following functions:
              - simulation_before_initialStep
              - simulation_around_initialStep
              - simulation_after_initialStep

        Parameters
        ----------
        outcar : input file
            The OUTCAR file.
        umd : output file
            The UMD file.
        cycle : int
            The cycle number of the simulation.

        Returns
        -------
        simulation : UMDsimulation
            The UMDSimulation object updated by the UMDSimulation_from_outcar
            function.

        """        
        simulation = Load_OUTCAR.UMDSimulation_from_outcar(outcar, simulation)
        Load_OUTCAR.UMDSnapshot_from_outcar(outcar, umd, simulation)
        return simulation
        

    # @staticmethod
    # def load_UMDSimulationRun(outcar, umd, simulation):
    #     """
    #     Convert the data of a simulation run from the OUTCAR to the UMD file.

    #     The function is implemented in two functions:
    #     - UMDSimulation_from_outcar,
    #       to read the lattice structure and the simulation parameters which
    #       are fixed for every snapshot of the simulation.
    #       If no UMDSimulation is initialized, then None is returned.
    #     - UMDSnapshot_from_outcar,
    #       to read each individual snapshots in the simulation.
    #       The number of snapshots read depends on the number of iterations set
    #       among the simulation parameters.
    #       According to the current simulation cycle and the initialStep, the
    #       snapshots are managed by one of the following functions:
    #           - simulation_before_initialStep
    #           - simulation_around_initialStep
    #           - simulation_after_initialStep

    #     Parameters
    #     ----------
    #     outcar : input file
    #         The OUTCAR file.
    #     umd : output file
    #         The UMD file.
    #     cycle : int
    #         The cycle number of the simulation.

    #     Returns
    #     -------
    #     simulation : UMDsimulation
    #         The UMDSimulation object updated by the UMDSimulation_from_outcar
    #         function.

    #     """
    #     loadedSteps = Load_OUTCAR.loadedSteps
    #     initialStep = Load_OUTCAR.initialStep
    #     finalStep = Load_OUTCAR.finalStep
    #     nSteps = Load_OUTCAR.nSteps
        
    #     Load_OUTCAR.print_parameters()
        
    #     cycle = simulation.cycle()
    #     simulation = UMDSimulation_from_outcar(outcar, simulation)
    #     if simulation.cycle() == cycle:
    #         return simulation
    #     else:
    #         run = simulation.runs[-1]
    #         print('Loaded simulation run...')
    #         print(run)
    #         print('Loading snapshots ...')
    #         steps = run.steps
    #         Load_OUTCAR.finalStep = min(initialStep+nSteps, loadedSteps+steps)
    #         if initialStep > loadedSteps + steps:
    #             print('before')
    #             Load_OUTCAR._run_before_initialStep(outcar, simulation)
    #         elif initialStep > loadedSteps:
    #             print('around')
    #             Load_OUTCAR._run_around_initialStep(outcar, umd, simulation)
    #         else:
    #             print('after')
    #             Load_OUTCAR._run_after_initialStep(outcar, umd, simulation)
    #         loadedSteps += steps
    #         print(' ... {} snapshots saved.\n'.format(run.steps))

    #         Load_OUTCAR.loadedSteps = loadedSteps
    #         Load_OUTCAR.initialStep = initialStep
    #         Load_OUTCAR.finalStep = finalStep
    #         Load_OUTCAR.nSteps = nSteps
        
    #     Load_OUTCAR.print_parameters()
    #     return simulation

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
