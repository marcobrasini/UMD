# -*- coding: utf-8 -*-
"""
Created on Wed May 18 17:09:04 2022

@author: marco
"""

import numpy as np
from .libs.UMDSnapshot import UMDSnapshot
from .libs.UMDSnapDynamics import UMDSnapDynamics
from .libs.UMDSnapThermodynamics import UMDSnapThermodynamics


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
            temperature = float(umd.readline().split()[-2])
            pressure = float(umd.readline().split()[-2])
            energy = float(umd.readline().split()[-2])
            thermodynamics = UMDSnapThermodynamics(temperature=temperature,
                                                   pressure=pressure,
                                                   energy=energy)
            return thermodynamics
        line = umd.readline()


def UMDSnapDynamics_from_umd(umd, natoms):
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
        if 'Dynamics' in line:
            time = float(line.strip().split()[-2])
            line = umd.readline()  # We read the header line
            dynamics = np.zeros((natoms, 9), dtype=float)
            for i in range(natoms):
                line = umd.readline().strip().split()
                dynamics[i] = line
            position = dynamics[:, 0:3]
            velocity = dynamics[:, 3:6]
            force = dynamics[:, 6:9]
            dynamics = UMDSnapDynamics(time=time, position=position,
                                       velocity=velocity, force=force)
            return dynamics
        line = umd.readline()


def UMDSnapshot_from_umd(umd, simulation):
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
    lattice = simulation.lattice
    natoms = lattice.natoms()
    line = umd.readline()
    while line:
        if 'Snapshot:' in line:
            step = int(line.replace('Snapshot:', '').strip())
            thermodynamics = UMDSnapThermodynamics_from_umd(umd)
            dynamics = UMDSnapDynamics_from_umd(umd, natoms)
            snapshot = UMDSnapshot(step, time=0.0, lattice=lattice)
            snapshot.setDynamics(dynamics)
            snapshot.setThermodynamics(thermodynamics)
            return snapshot
        line = umd.readline()
