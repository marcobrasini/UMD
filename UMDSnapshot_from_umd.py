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
    line = umd.readline()
    while line:
        if 'Thermodynamics:' in line:
            T = float(umd.readline().split()[-2])
            P = float(umd.readline().split()[-2])
            E = float(umd.readline().split()[-2])
            snapThermodynamics = UMDSnapThermodynamics(T, P, E)
            return snapThermodynamics
        line = umd.readline()


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
    line = umd.readline()
    while line:
        if 'Position' in line and 'Velocity' in line and 'Force' in line:
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
        line = umd.readline()


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
