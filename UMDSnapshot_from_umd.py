# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:09:04 2022

@author: marco
"""

import numpy as np
from UMDSnapshot import UMDSnapshot
from UMDSnapDynamics import UMDSnapDynamics
from UMDSnapThermodynamics import UMDSnapThermodynamics


def UMDSnapThermodynamics_from_umd(umd):
    """
    Initialize a UMDSnapThermodynamics object from a UMD file.

    Parameters
    ----------
    umd : input file
        The UMD input file.

    Returns
    -------
    snapThermodynamics : UMDSnapThermodynamics
        A UMDSnapThermodynamics object.

    """
    temperature = float(umd.readline().split()[-2])
    pressure = float(umd.readline().split()[-2])
    energy = float(umd.readline().split()[-2])
    snapThermodynamics = UMDSnapThermodynamics(temperature, pressure, energy)
    return snapThermodynamics


def UMDSnapDynamics_from_umd(umd):
    """
    Initialize a UMDSnapDynamics object from a UMD file.

    Parameters
    ----------
    umd : input file
        The UMD input file.

    Returns
    -------
    snapDynamics : UMDSnapDynamics
        A UMDSnapDynamics object.

    """
    line = umd.readline()  # read the header line
    natoms = UMDSnapshot.natoms
    dynamics = np.zeros((natoms, 9), dtype=float)
    for i in range(natoms):
        line = umd.readline().strip().split()
        dynamics[i] = line
    position = dynamics[:, 0:3]
    velocity = dynamics[:, 3:6]
    force = dynamics[:, 6:9]
    snapDynamics = UMDSnapDynamics(position, velocity, force)
    return snapDynamics


def UMDSnapshot_from_umd(umd):
    """
    Initialize a UMDSnapshot object from a UMD file.

    Parameters
    ----------
    umd : input file
        The UMD input file.

    Returns
    -------
    snapshot : UMDSnapshot
        A UMDSnapshot object.

    """
    line = umd.readline()
    while line:
        if 'Snapshot:' in line:
            step = int(line.replace('Snapshot:', '').strip())
            thermodynamics = UMDSnapThermodynamics_from_umd(umd)
            dynamics = UMDSnapDynamics_from_umd(umd)
            snapshot = UMDSnapshot(step, thermodynamics, dynamics)
            return snapshot
        line = umd.readline()
