# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:19:27 2022

@author: marco
"""
"""
To test UMDSimulation_from_outcar we use three examples of OUTCARfile:
 - the OUTCAR_nomag, /tests/nomag5.70a1800T.outcar
 - the OUTCAR_mag,   /tests/mag5.70a1800T.outcar
 - the OUTCAR_magpU, /tests/magpU5.70a1800T.outcar

Each simulation has the same structure:
 + it is run on a 2x2x2 supercelll of a bcc structure with lattice parameter
   of 5.70 ang. The matrix of basis vectors is:
       5.70     0.00     0.00
       0.00     5.70     0.00
       0.00     0.00     5.70
   and the cell contains the following elements:
     - O: 15 atoms,
     - H: 28 atoms,
     - Fe: 1 atom.
 + the simulation is divided in three cycles:
     - cycle 0:  300 steps and 0.5 snap duration
     - cycle 1:  600 steps and 0.5 snap duration
     - cycle 2: 1000 steps and 0.4 snap duration
"""


from ..UMDSimulation_from_outcar import UMDSimulation_from_outcar

import numpy as np

from ..UMDAtom import UMDAtom
from ..UMDLattice import UMDLattice
from ..UMDSimulation import UMDSimulation
from ..UMDSimulationRun import UMDSimulationRun


class TestUMDSimulation_from_outcar:


    OUTCARfile = 'examples/mag5.70a1800T.outcar'
    name = 'mag5.70a1800T'
    
    # According to the lattice structure, we initialize the UMDLattice object
    # that we will use as reference for the test ...
    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)
    # ... and the UMDSimulationRun representing the simulation runs which are
    # concatenated in the OUTCAR file.
    run0 = UMDSimulationRun(0, 300, 0.5)
    run1 = UMDSimulationRun(1, 600, 0.5)
    run2 = UMDSimulationRun(2, 1000, 0.4)
    runs = (run0, run1, run2)

    def test_UMDSimulation_from_outcar(self):
        """
        Test UMDSimulation_from_outcar function when it reads single OUTCAR
        file, containing many OUTCAR files concatenated. Each part of the whole
        OUTCAR corresponds to a single simulation run with its own parameters.
        Scrolling all the OUTCAR file, at each new simulation run the
        UMDSimulation_from_outcar must must update the total UMDSimulation
        object with the new simulation run.

        """
        totsimulation = UMDSimulation(name=self.name, lattice=self.lattice)
        with open(self.OUTCARfile, 'r') as outcar:
            simulation = UMDSimulation(name=self.name, lattice=self.lattice)
            while True:
                cycle = simulation.cycle()
                simulation = UMDSimulation_from_outcar(outcar, simulation)
                if simulation.cycle() == cycle:
                    break
                totsimulation.add(self.runs[cycle])
                assert simulation == totsimulation
            outcar.close()
            assert simulation.lattice == self.lattice
            assert simulation.cycle() == 3
            assert simulation.steps() == 1900
            assert simulation.time() == 850.0

    def test_UMDSimulation_from_outcar(self):
        """
        Test UMDSimulation_from_outcar function when it reads single OUTCAR
        file, containing many OUTCAR files concatenated. Each part of the whole
        OUTCAR corresponds to a single simulation run with its own parameters.
        Scrolling all the OUTCAR file, at each new simulation run the
        UMDSimulation_from_outcar must must update the total UMDSimulation
        object with the new simulation run.

        """
        totsimulation = UMDSimulation(name=self.name, lattice=self.lattice)
        with open(self.OUTCARfile, 'r') as outcar:
            simulation = UMDSimulation(name=self.name, lattice=self.lattice)
            while True:
                cycle = simulation.cycle()
                simulation = UMDSimulation_from_outcar(outcar, simulation)
                if simulation.cycle() == cycle:
                    break
                totsimulation.add(self.runs[cycle])
                assert simulation == totsimulation
                assert simulation.lattice == self.lattice
            outcar.close()
