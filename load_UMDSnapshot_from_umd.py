"""
===============================================================================
                            UMDSnapshot_from_umd
===============================================================================

This module provides the UMDSnapshot_from_umd function implementation. The
UMDSnapshot_from_umd function is necessary to extract the snapshot data from
a UMD file.
All snapshot informations are reported after the header of the UMD file and
are grouped into a single snapshot section.

The snapshot section starts with the string "Snapshot:          x", where x is
the snapshot index. Then it is subdevided into two subsections:
 + the thermodynamics section
       Thermodynamics:
       Temperature = xxxxx.xxxxxx K
       Pressure    = xxxxx.xxxxxx GPa
       Energy      = xxxxx.xxxxxx eV
 + the dynamics section containing the snapshot duration
       Dynamics: xxxxxxxx.xxx fs
   and a list of all the N atoms dynamic informations. Each line contains the
   cartesian coordinates of the single atom position, velocity and force.
       "Position_x      Position_y      Position_z      "
       +"Velocity_x      Velocity_y      Velocity_z      "
       +"Force_x         Force_y         Force_z         \n"
         r1_x    r1_y    r1_z    v1_x    v1_y    v1_z    F1_x    F1_y    F1_z
         r2_x    r2_y    r2_z    v2_x    v2_y    v2_z    F2_x    F2_y    F2_z
         ...     ...     ...     ...     ...     ...     ...     ...     ...
         rN_x    rN_y    rN_z    vN_x    vN_y    vN_z    FN_x    FN_y    FN_z
"""

import numpy as np
from .libs.UMDSnapDynamics import UMDSnapDynamics
from .libs.UMDSnapThermodynamics import UMDSnapThermodynamics


def load_UMDSnapThermodynamics_from_umd(umd):
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
    for line in umd:
        if 'Thermodynamics:' in line:
            temperature = float(umd.readline().split()[-2])
            pressure = float(umd.readline().split()[-2])
            energy = float(umd.readline().split()[-2])
            thermodynamics = UMDSnapThermodynamics(temperature=temperature,
                                                   pressure=pressure,
                                                   energy=energy)
            return thermodynamics
    raise(EOFError('UMD file ended with UMDSnapTermodynamics uninitialized.'))


def load_UMDSnapDynamics_from_umd(umd, natoms):
    """
    Initialize a UMDSnapDynamics object from a UMD file.

    Parameters
    ----------
    umd : input file
        The UMD input file.
    natoms : int
        The number of atoms in the snapshot.

    Returns
    -------
    snapDynamics : UMDSnapDynamics
        A UMDSnapDynamics object.

    """
    for line in umd:
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
    raise(EOFError('UMD file ended with UMDSnapDynamics uninitialized.'))


def load_UMDSnapshot_from_umd(umd, snapshot):
    """
    Initialize a UMDSnapshot object from a UMD file.

    Parameters
    ----------
    umd : input file
        The UMD input file.
    snapshot : UMDSnapshot
        The UMDSnapshot object with the snapshot data.

    Returns
    -------
    snapshot : UMDSnapshot
        A UMDSnapshot object.

    """
    thermodynamics = load_UMDSnapThermodynamics_from_umd(umd)
    dynamics = load_UMDSnapDynamics_from_umd(umd, snapshot.natoms)
    snapshot.setDynamics(dynamics)
    snapshot.setThermodynamics(thermodynamics)
    return snapshot
