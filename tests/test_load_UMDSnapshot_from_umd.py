"""
==============================================================================
                        load_UMDSnapshot_from_umd tests
==============================================================================

To test load_UMDSnapshot_from_umd we use four examples of UMD files
 - the example/UMD_single.umd:
   It contains a single simulation run with 300 snapshots of 0.4 fs duration.
 - the example/UMD_multiple.umd:
   It containes the results of three concatenated runs:
       - run0 with 300 snapshots of 0.5 fs duration.
       - run1 with 600 snapshots of 0.5 fs duration.
       - run2 with 1000 snapshots of 0.4 fs duration.
 - the examples/UMD_snapshot.umd:
   It contains a single snapshot (the 1044-th of the example/UMD_multiple.umd)
 - the examples/UMD_empty.umd:
   It contains no snapshot.

All simulations are performed on the same lattice structure:
 - the matrix of basis vectors is:
       5.70     0.00     0.00
       0.00     5.70     0.00
       0.00     0.00     5.70
 - the contained atoms are:
     - O: 15 atoms,
     - H: 28 atoms,
     - Fe: 1 atom.

"""

from ..load_UMDSnapshot_from_umd import load_UMDSnapshot_from_umd
from ..load_UMDSnapshot_from_umd import load_UMDSnapThermodynamics_from_umd
from ..load_UMDSnapshot_from_umd import load_UMDSnapDynamics_from_umd

import pytest
import numpy as np
import unittest.mock as mock

from ..libs.UMDAtom import UMDAtom
from ..libs.UMDLattice import UMDLattice
from ..libs.UMDSnapshot import UMDSnapshot
from ..libs.UMDSnapDynamics import UMDSnapDynamics
from ..libs.UMDSnapThermodynamics import UMDSnapThermodynamics


class Test_load_UMDSnapshot_from_umd:

    module = 'UMD.load_UMDSnapshot_from_umd.'

    lattice_name = '2bccH2O+1Fe'
    H = UMDAtom(name='H', mass=1.00, valence=1.0)
    O = UMDAtom(name='O', mass=16.00, valence=6.0)
    Fe = UMDAtom(name='Fe', mass=55.85, valence=8.0)
    atoms = {O: 15, H: 28, Fe: 1}
    basis = 5.7*np.identity(3)
    lattice = UMDLattice(lattice_name, basis, atoms)
    natoms = lattice.natoms()

    step = 1043
    time = 0.4
    temperature = 1769.01
    energy = -178.209742
    pressure = np.mean(np.array([604.475, 627.147, 688.912]))/10
    position = np.array([[5.30395,      5.36673,      5.42726],
                         [0.25290,      5.49507,      3.03868],
                         [0.01625,      2.54823,      0.19909],
                         [0.26805,      3.28280,      2.40297],
                         [3.10211,      0.38845,      5.62765],
                         [2.51248,      0.00957,      3.22512],
                         [3.36397,      3.00867,      5.49845],
                         [2.76431,      2.42273,      2.14134],
                         [1.31249,      1.62186,      4.24494],
                         [1.54416,      4.92408,      0.98482],
                         [1.49931,      3.96795,      4.38480],
                         [4.78171,      1.17054,      1.76894],
                         [4.46734,      1.82999,      4.03760],
                         [4.04422,      4.32309,      1.37821],
                         [4.13389,      4.08425,      3.72340],
                         [2.58826,      2.61592,      3.08179],
                         [0.18641,      3.48484,      5.66585],
                         [1.46176,      4.32037,      1.80470],
                         [3.50121,      2.12178,      0.34013],
                         [3.62713,      1.62924,      4.27020],
                         [5.26567,      1.74077,      1.01405],
                         [3.62770,      4.12647,      0.53820],
                         [4.35136,      0.48245,      1.42105],
                         [2.35142,      5.69396,      0.64815],
                         [4.97405,      4.91621,      4.71204],
                         [2.19214,      2.68601,      4.96147],
                         [4.75860,      1.58939,      3.01558],
                         [5.00462,      3.34324,      1.76249],
                         [5.30565,      4.02186,      2.76723],
                         [2.48783,      0.55272,      4.87161],
                         [3.03130,      3.36984,      1.72325],
                         [0.55947,      3.77872,      4.05693],
                         [0.98017,      0.64167,      3.75907],
                         [0.53008,      4.90820,      0.46412],
                         [4.15131,      3.24991,      4.00669],
                         [1.83765,      3.87383,      5.31869],
                         [1.08036,      1.68795,      5.21131],
                         [5.06137,      0.15377,      2.84364],
                         [4.49922,      0.15894,      5.63098],
                         [3.69352,      4.85878,      3.99004],
                         [5.25817,      1.97418,      4.88882],
                         [2.93729,      5.32423,      2.47768],
                         [2.07799,      4.88050,      3.72449],
                         [1.14056,      1.30966,      1.87068]])
    velocity = np.zeros((44, 3), dtype=float)
    force = np.array([[ 4.346583,      1.975307,      2.707162],
                      [ 0.068890,      2.020951,      0.599096],
                      [ 0.646264,     -0.591564,     -0.960353],
                      [-1.641598,     -0.638223,     -0.578769],
                      [-0.741747,      1.554483,      0.154278],
                      [ 1.258265,      0.880869,     -0.173089],
                      [-5.619718,     -4.987019,     -0.029841],
                      [-1.727388,      0.166832,      0.389615],
                      [ 0.966525,     -0.857317,      0.563598],
                      [-2.376987,     -1.973354,      1.262744],
                      [-0.812807,     -0.375136,     -0.163459],
                      [ 2.347666,      5.597721,      0.557532],
                      [ 6.278242,     -0.765039,     -3.302839],
                      [-0.460630,      1.100438,      3.401684],
                      [ 2.401092,      5.441276,     -3.936564],
                      [-0.334891,      0.007334,     -0.356843],
                      [-0.781699,     -1.051797,      0.897297],
                      [-1.039054,      0.412452,     -0.808916],
                      [-0.681380,      2.464334,     -1.101236],
                      [-4.038112,     -1.540466,      1.123499],
                      [-1.554406,      1.351007,     -0.200527],
                      [ 0.286244,     -0.095348,     -0.788921],
                      [-3.287319,     -5.627440,     -1.985435],
                      [ 1.453983,     -0.275200,     -1.121846],
                      [-0.576863,     -2.636953,     -3.605522],
                      [ 3.892479,     -0.323818,      0.036463],
                      [-1.193676,      0.588033,      1.272675],
                      [ 0.898419,      1.063521,     -0.188156],
                      [ 1.426308,     -0.392434,      0.773351],
                      [ 0.388964,      0.543124,      0.061032],
                      [ 1.220740,     -0.166714,      0.585322],
                      [ 1.719612,     -0.055232,     -0.209813],
                      [-1.383706,      0.310055,      0.620480],
                      [ 0.727753,      1.602906,      0.549045],
                      [-0.593003,     -5.358561,      2.820735],
                      [-0.489129,      1.046920,      0.274305],
                      [-0.509906,     -0.570402,     -0.323577],
                      [ 1.595880,     -1.285913,      1.000185],
                      [-1.614718,      0.282760,      0.617217],
                      [-2.174539,      1.050728,      0.753147],
                      [-0.840822,      1.005338,      0.016669],
                      [ 1.453374,     -1.296291,     -1.659476],
                      [-0.280773,      0.605878,     -0.507692],
                      [ 1.387906,     -0.202300,      0.976311]])
    
    snapshot = UMDSnapshot(step, time, lattice)
    dynamics = UMDSnapDynamics(time, position, velocity, force)
    thermodynamics = UMDSnapThermodynamics(temperature, pressure, energy)
    snapshot.setDynamics(dynamics)
    snapshot.setThermodynamics(thermodynamics)

    #%% load_UMDSnapThermodynamics_from_umd tests
    def test_load_UMDSnapThermodynamics_from_umd_snapshot(self):
        """
        Test the load_UMDSnapThermodynamics_from_umd function reading an
        isolated from a UMD file and comparing it with the reference
        UMDSnapThermodynamics object.

        """
        with open('examples/UMD_snapshot.umd', 'r') as umd:
            thermodynamics = load_UMDSnapThermodynamics_from_umd(umd)
            assert thermodynamics == self.thermodynamics
            umd.close()

    def test_load_UMDSnapThermodynamics_from_umd_eof(self):
        """
        Test load_UMDSnapThermodynamics_from_umd function reading from an empty
        UMD file. An EOFError is raised.

        """
        with open('examples/UMD_empty.umd', 'r') as umd:
            with pytest.raises(EOFError):
                load_UMDSnapThermodynamics_from_umd(umd)
            umd.close()

    # %% load_UMDSnapDynamcis_from_umd tests
    def test_load_UMDSnapDynamics_from_umd_snapshot(self):
        """
        Test the load_UMDSnapDynamics_from_umd function reading an isolated
        snapshot from a UMD file and comparing it with the reference
        UMDSnapDynamics object.

        """
        with open('examples/UMD_snapshot.umd', 'r') as umd:
            dynamics = load_UMDSnapDynamics_from_umd(umd, self.natoms)
            assert dynamics == self.dynamics
            umd.close()

    def test_load_UMDSnapDynamics_from_umd_eof(self):
        """
        Test load_UMDSnapDynamics_from_umd function when it reads an empty UMD
        file. An EOFError is raised.

        """
        with open('examples/UMD_empty.umd', 'r') as umd:
            with pytest.raises(EOFError):
                load_UMDSnapDynamics_from_umd(umd, self.natoms)
            umd.close()

    # %% load_UMDSnapshot_from_umd tests
    def test_load_UMDSnapshot_from_umd_snapshot(self):
        """
        Test the load_UMDSnapshot_from_umd function reading an isolated
        snapshot from a UMD file and comparing it with the reference
        UMDSnapshot object.

        """
        with open('examples/UMD_snapshot.umd', 'r') as umd:
            snapshot = UMDSnapshot(snap=1043, lattice=self.lattice)
            snapshot = load_UMDSnapshot_from_umd(umd, snapshot)
            assert snapshot == self.snapshot
            umd.close()

    @mock.patch(module+'load_UMDSnapDynamics_from_umd')
    @mock.patch(module+'load_UMDSnapThermodynamics_from_umd')
    @mock.patch.object(UMDSnapshot, 'setDynamics')
    @mock.patch.object(UMDSnapshot, 'setThermodynamics')
    def test_load_UMDSnapshot_from_umd(self, mock_thermo, mock_dynamics,
                                       mock_load_thermo, mock_load_dynamics):
        """
        Test the load_UMDSnapshot_from_umd function reading an isolated
        snapshot from a UMD file.

        """
        with open('examples/UMD_snapshot.umd', 'r') as umd:
            snapshot = UMDSnapshot(snap=1043, lattice=self.lattice)
            snapshot = load_UMDSnapshot_from_umd(umd, snapshot)
            mock_load_dynamics.assert_called_once()
            mock_load_thermo.assert_called_once()
            mock_dynamics.assert_called_once()
            mock_thermo.assert_called_once()
            umd.close()
