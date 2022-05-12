# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:08:16 2022

@author: marco
"""
"""
To test load_UMDSnapshot we use three examples of OUTCARfile:
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
     
For each simulation, we consider only a single snapshot.
The snapshot considered is the 144-th snapshot of the cycle number 2, which 
correspond to the 1044-th snapshot of the whole simulation in the OUTCAR file.
The data of this snapshots are copied in separate individual files:
 - /tests/nomag5.70a1800T.outcar.snap1044
 - /tests/mag5.70a1800T.outcar.snap1044
 - /tests/magpU5.70a1800T.outcar.snap1044
and the reference values of this sanpshot are initialiazed in order to be
compared with the results of the load_Snapshot function.
"""


from UMDSnapshot_from_outcar import UMDSnapshot_from_outcar
from UMDSnapshot_from_outcar import load_UMDSnapshot

import numpy as np

from UMDAtom import UMDAtom
from UMDLattice import UMDLattice
from UMDSnapshot import UMDSnapshot


snap_reference = 1044
testOUTCAR_nomag = 'tests/nomag5.70a1800T.outcar'
testOUTCAR_mag = 'tests/mag5.70a1800T.outcar'
testOUTCAR_magpU = 'tests/magpU5.70a1800T.outcar'


# %% The lattice structure values
# According to the header, we initialize the structure vaules, necessary to
# set the UMDSnapshot attributes and make the load_Snapshot function work
# properly.
name = '2bccH2O+1Fe'
basis = np.array([[5.7, 0.0, 0.0],
                  [0.0, 5.7, 0.0],
                  [0.0, 0.0, 5.7]])
H = UMDAtom('H', mass=1.00, valence=1.0)
O = UMDAtom('O', mass=16.00, valence=6.0)
Fe = UMDAtom('Fe', mass=55.85, valence=8.0)
lattice = UMDLattice(name, basis, atoms={O: 15, H: 28, Fe: 1})


# %% nomag snapshot reference value
temperature_nomag = 1819.39
energy_nomag = -178.923811
pressure_nomag = np.mean(np.array([722.834, 640.974, 593.446])) / 10
position_nomag = np.array([[0.23152,      0.11933,      0.44371],
                           [0.14342,      5.28471,      2.72325],
                           [5.61987,      2.56012,      0.14974],
                           [0.18324,      2.97870,      3.20319],
                           [2.69444,      0.25094,      0.58211],
                           [2.31258,      5.57314,      2.90268],
                           [3.27000,      2.51876,      0.00869],
                           [2.63712,      2.58248,      3.07975],
                           [1.05518,      1.32278,      4.63340],
                           [1.47719,      3.92271,      1.34445],
                           [1.50852,      4.06361,      4.57128],
                           [4.52734,      1.29398,      2.11486],
                           [4.05867,      0.76696,      4.46126],
                           [4.21063,      4.38172,      1.34622],
                           [4.44930,      4.33091,      4.42891],
                           [3.42990,      5.62481,      1.23286],
                           [5.33583,      3.18362,      0.97753],
                           [0.42486,      1.68844,      3.83177],
                           [3.77142,      1.79329,      2.42480],
                           [5.25622,      2.42842,      2.86820],
                           [3.14726,      1.13913,      0.21414],
                           [1.77877,      2.99487,      3.49530],
                           [2.65445,      0.38886,      2.10227],
                           [5.54277,      4.44186,      3.25550],
                           [1.36183,      5.46893,      3.28235],
                           [4.39569,      1.75478,      4.58976],
                           [3.41832,      4.29974,      1.79429],
                           [0.80344,      5.23711,      1.05324],
                           [5.20154,      5.22663,      0.63123],
                           [1.25164,      3.73764,      5.55623],
                           [0.71285,      3.62831,      1.84732],
                           [2.66319,      3.17949,      5.10414],
                           [4.95791,      0.10889,      2.56337],
                           [5.01307,      1.43771,      1.08619],
                           [3.79338,      3.13365,      0.60646],
                           [5.10440,      3.57878,      4.46415],
                           [0.51857,      0.50476,      5.24325],
                           [1.78771,      4.52174,      2.16804],
                           [3.82818,      4.04006,      3.77507],
                           [2.62837,      2.61074,      2.07959],
                           [3.17853,      0.92342,      3.74320],
                           [4.59665,      5.48401,      4.25040],
                           [2.12074,      4.75761,      4.68935],
                           [1.50252,      2.13619,      0.51298]])
force_nomag = np.array([[-0.889002,     -2.569627,      4.179830],
                        [-1.923847,     -0.631682,      2.442681],
                        [-4.626970,      3.146240,      3.442406],
                        [ 1.885726,      1.254894,      0.625579],
                        [ 0.260557,      2.367783,      0.482230],
                        [ 3.507183,     -0.786563,      1.033411],
                        [-0.703137,      2.536183,     -1.508339],
                        [ 1.592848,      0.027481,     -0.418834],
                        [ 1.145203,     -1.529714,     -4.293747],
                        [ 1.369993,      0.326594,      0.159188],
                        [ 0.106505,     -0.903382,      2.067180],
                        [ 1.017910,     -0.026264,     -3.192036],
                        [-0.999716,      4.120476,     -2.689255],
                        [ 2.136972,     -1.781081,     -1.295941],
                        [-0.778273,     -0.572304,      1.637904],
                        [ 0.161567,     -0.211488,     -2.593499],
                        [-0.476745,     -0.921152,     -2.466151],
                        [ 2.457425,      0.576535,      2.411251],
                        [-0.609188,      0.788834,      0.083045],
                        [-3.039821,     -2.587296,     -2.362018],
                        [-0.509956,     -2.401895,      0.136966],
                        [ 0.472661,     -0.751916,     -0.762802],
                        [-2.482053,      0.167014,      0.709115],
                        [ 1.255526,      1.090327,     -2.029044],
                        [-1.146975,      1.948666,     -0.888280],
                        [-0.304471,     -2.985886,     -0.019228],
                        [-2.174163,     -0.726589,      1.936882],
                        [ 0.528018,      0.959232,     -0.820756],
                        [-2.803073,     -0.865093,     -0.052310],
                        [ 0.119660,      1.426431,     -2.238275],
                        [-1.530025,     -0.996679,      2.100091],
                        [ 1.160804,     -0.815410,      0.258997],
                        [ 2.023767,     -0.037338,      0.047906],
                        [-1.053641,      0.328351,      2.409248],
                        [-0.199402,      1.358129,     -0.041747],
                        [ 0.659026,     -0.126863,     -0.085222],
                        [ 1.320193,      0.965276,     -2.894883],
                        [ 1.361493,      0.378899,     -0.489685],
                        [-1.266231,     -0.593521,     -1.176741],
                        [-1.218236,      0.231320,      0.873114],
                        [ 1.845893,     -1.256231,      2.312111],
                        [-0.493567,      0.623327,      0.678727],
                        [ 1.499671,      2.330067,      0.855290],
                        [ 1.341410,     -2.860666,      1.440891]])

# %% mag snapshot reference values
temperature_mag = 1769.01
energy_mag = -178.209742
pressure_mag = np.mean(np.array([604.475, 627.147, 688.912])) / 10
position_mag = np.array([[5.30395,      5.36673,      5.42726],
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
force_mag = np.array([[ 4.346583,      1.975307,      2.707162],
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

# %% magpU snapshot reference values
temperature_magpU = 2072.46
energy_magpU = -181.020677
pressure_magpU = np.mean(np.array([644.048, 619.413, 579.457])) / 10
position_magpU = np.array([[4.81140,      5.05304,      0.62052],
                           [5.64000,      1.07079,      2.21302],
                           [5.40278,      2.85900,      0.58884],
                           [1.02287,      3.43327,      2.34712],
                           [2.91308,      5.20162,      4.58730],
                           [3.55181,      0.00219,      2.35106],
                           [2.60012,      3.18898,      5.46502],
                           [2.52609,      1.82268,      3.49773],
                           [1.11863,      1.57274,      5.01512],
                           [1.48630,      5.30348,      0.99535],
                           [0.51523,      4.97741,      4.12584],
                           [3.58050,      1.35612,      0.64878],
                           [4.69865,      1.06270,      4.42889],
                           [3.59461,      3.55297,      2.09858],
                           [4.64749,      3.36053,      4.03777],
                           [1.06650,      0.66288,      5.24249],
                           [5.00998,      3.82671,      3.22793],
                           [0.33238,      3.42755,      1.35585],
                           [4.17439,      0.14354,      0.44255],
                           [3.83668,      2.77046,      1.37936],
                           [3.03409,      3.13930,      3.02328],
                           [5.10491,      2.39435,      4.35454],
                           [3.42333,      0.93415,      1.86034],
                           [2.90346,      5.68533,      3.69978],
                           [0.71262,      4.81508,      5.04710],
                           [5.06696,      1.84210,      1.77202],
                           [1.69176,      1.68696,      3.92873],
                           [4.46729,      5.50287,      2.24534],
                           [4.53611,      4.00472,      4.73226],
                           [2.84668,      1.93507,      5.61462],
                           [2.51844,      4.07495,      4.69996],
                           [1.03414,      4.45024,      3.28098],
                           [2.16823,      5.33998,      5.23162],
                           [5.46225,      0.22378,      4.44631],
                           [5.46018,      1.29063,      3.22000],
                           [4.95645,      3.87651,      0.58713],
                           [2.34235,      5.23234,      1.55556],
                           [2.84055,      3.69567,      0.58609],
                           [0.02791,      5.19579,      1.02316],
                           [4.02671,      1.40782,      5.25625],
                           [0.49663,      2.34578,      5.52892],
                           [0.59393,      2.64194,      2.70147],
                           [3.51580,      1.72589,      3.89576],
                           [1.86669,      1.55386,      1.56857]])
force_magpU = np.array([[ 1.065789,     -0.680029,     -2.024788],
                        [ 0.106954,      2.889532,      1.628988],
                        [ 0.667190,      1.512405,      0.014929],
                        [ 0.159582,      0.954088,      1.163075],
                        [-0.448471,     -0.204534,     -0.202341],
                        [-3.491008,      1.228752,      2.478614],
                        [-0.812692,      1.178867,     -0.024969],
                        [ 5.618999,      1.572900,     -4.935917],
                        [-0.742723,      0.759181,      2.039565],
                        [ 0.901409,      1.039580,     -0.498763],
                        [ 0.602590,      1.086423,     -1.501501],
                        [-1.495577,      0.788779,     -1.978871],
                        [ 0.222348,      2.115043,     -1.437283],
                        [-1.151622,     -3.544877,     -0.538672],
                        [ 0.881608,     -1.282408,     -0.674397],
                        [-0.774261,     -0.724528,      0.850669],
                        [-0.832413,     -0.737087,      0.661705],
                        [ 0.599645,     -1.189517,     -0.147061],
                        [ 0.276257,     -0.259172,      0.625377],
                        [-0.615110,      1.557681,      2.586589],
                        [ 1.430970,      0.359267,     -3.711767],
                        [-1.176963,     -0.012091,     -0.164278],
                        [ 1.843430,     -2.331510,      1.492421],
                        [ 0.500756,     -0.394316,     -0.383430],
                        [ 0.525047,     -1.539843,      0.773874],
                        [ 1.326648,     -1.462565,     -0.462211],
                        [-1.521970,     -0.182535,      2.656876],
                        [ 0.692224,     -0.408224,     -0.124771],
                        [-0.118438,      0.855153,      0.953267],
                        [ 0.087648,      1.946593,      0.914108],
                        [ 1.143264,     -1.278945,      0.637432],
                        [-0.841990,     -0.529307,      0.672918],
                        [ 0.740764,      0.944664,      0.958230],
                        [-1.675829,      0.463131,     -0.901767],
                        [-0.519086,     -1.283184,     -1.099713],
                        [-0.643024,     -0.637523,     -0.729454],
                        [-0.311480,     -1.054274,     -0.259108],
                        [-0.123467,     -0.245266,      0.092501],
                        [ 0.620439,      0.987530,     -0.142638],
                        [ 2.204716,     -1.241788,      0.343461],
                        [-0.395816,     -0.596780,      0.803792],
                        [-0.110844,      0.188136,      0.786183],
                        [-1.879259,     -1.208186,     -0.927068],
                        [-2.535113,      0.621257,     -0.261538]])


# %% load_UMDSnapshot function tests on single snapshot file
def test_load_UMDSnapshot_nomag():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a single file containing only that
    snapshot data (in non magnetic configuration).

    """
    UMDSnapshot.reset(0.5, lattice)
    testSnap = testOUTCAR_nomag + '.snap'+str(snap_reference)
    with open(testSnap, 'r') as outcar:
        snapshot = load_UMDSnapshot(outcar, snap_reference)
        assert snapshot.snapThermodynamics.energy == energy_nomag
        assert snapshot.snapThermodynamics.temperature == temperature_nomag
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_nomag)
        assert np.array_equal(snapshot.snapDynamics.position, position_nomag)
        assert np.array_equal(snapshot.snapDynamics.force, force_nomag)


def test_load_UMDSnapshot_mag():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a single file containing only that
    snapshot data (in magnetic configuration).

    """
    UMDSnapshot.reset(0.5, lattice)
    testSnap = testOUTCAR_mag + '.snap'+str(snap_reference)
    with open(testSnap, 'r') as outcar:
        snapshot = load_UMDSnapshot(outcar, snap_reference)
        assert snapshot.snapThermodynamics.energy == energy_mag
        assert snapshot.snapThermodynamics.temperature == temperature_mag
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_mag)
        assert np.array_equal(snapshot.snapDynamics.position, position_mag)
        assert np.array_equal(snapshot.snapDynamics.force, force_mag)


def test_load_UMDSnapshot_magpU():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a single file containing only that
    snapshot data (in magnetic configuration with +U potential correction).

    """
    UMDSnapshot.reset(0.5, lattice)
    testSnap = testOUTCAR_magpU + '.snap'+str(snap_reference)
    with open(testSnap, 'r') as outcar:
        snapshot = load_UMDSnapshot(outcar, snap_reference)
        assert snapshot.snapThermodynamics.energy == energy_magpU
        assert snapshot.snapThermodynamics.temperature == temperature_magpU
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_magpU)
        assert np.array_equal(snapshot.snapDynamics.position, position_magpU)
        assert np.array_equal(snapshot.snapDynamics.force, force_magpU)


test_load_UMDSnapshot_nomag()
test_load_UMDSnapshot_mag()
test_load_UMDSnapshot_magpU()


# %% test load_UMDSnapshot function on whole OUTCAR files
def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_nomag():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a whole OUTCAR file containing many
    snapshot data (in non magnetic configuration).
    All the snapshots are read by the Snapshot_from_outcar function, and when
    it encounters the considered step, the snapshot informations are compared
    with the reference values.

    """
    snap = 0
    UMDSnapshot.reset(0.5, lattice)
    with open(testOUTCAR_nomag, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, snap)
            if snap == snap_reference-1:
                break
            snap += 1
        assert snapshot.snapThermodynamics.energy == energy_nomag
        assert snapshot.snapThermodynamics.temperature == temperature_nomag
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_nomag)
        assert np.array_equal(snapshot.snapDynamics.position, position_nomag)
        assert np.array_equal(snapshot.snapDynamics.force, force_nomag)


def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_mag():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a whole OUTCAR file containing many
    snapshot data (in magnetic configuration).
    All the snapshots are read by the Snapshot_from_outcar function, and when
    it encounters the considered step, the snapshot informations are compared
    with the reference values.

    """
    snap = 0
    UMDSnapshot.reset(0.5, lattice)
    with open(testOUTCAR_mag, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, snap)
            if snap == snap_reference-1:
                break
            snap += 1
        assert snapshot.snapThermodynamics.energy == energy_mag
        assert snapshot.snapThermodynamics.temperature == temperature_mag
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_mag)
        assert np.array_equal(snapshot.snapDynamics.position, position_mag)
        assert np.array_equal(snapshot.snapDynamics.force, force_mag)


def test_UMDSnapshot_from_outcar_nSnapshot_concatenated_magpU():
    """
    Test the load_UMDSnapshot function in initializing a single UMDSnapshot,
    when it reads the information from a whole OUTCAR file containing many
    snapshot data (in magnetic configuration with +U potential correction).
    All the snapshots are read by the Snapshot_from_outcar function, and when
    it encounters the considered step, the snapshot informations are compared
    with the reference values.

    """
    snap = 0
    UMDSnapshot.reset(0.5, lattice)
    with open(testOUTCAR_magpU, 'r') as outcar:
        while True:
            snapshot = UMDSnapshot_from_outcar(outcar, snap)
            if snap == snap_reference-1:
                break
            snap += 1
        assert snapshot.snapThermodynamics.energy == energy_magpU
        assert snapshot.snapThermodynamics.temperature == temperature_magpU
        assert np.isclose(snapshot.snapThermodynamics.pressure, pressure_magpU)
        assert np.array_equal(snapshot.snapDynamics.position, position_magpU)
        assert np.array_equal(snapshot.snapDynamics.force, force_magpU)


test_UMDSnapshot_from_outcar_nSnapshot_concatenated_nomag()
test_UMDSnapshot_from_outcar_nSnapshot_concatenated_mag()
test_UMDSnapshot_from_outcar_nSnapshot_concatenated_magpU()
