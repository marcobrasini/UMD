"""
===============================================================================
                            UMDSnapshot_from_outcar
===============================================================================

This module provides the UMDSnapshot_from_outcar function implementation. The
UMDSnapshot_from_outcar function is necessary to extract the snapshot data from
a Vasp OUTCAR file.
Snapshot informations are reported at the end of a convergence loop executed
at each Iteration in the OUTCAR file.

The convergence loop of the X iteration starts with the line
"---------------------------- Iteration X(   1) ----------------------------".
Then, y convergence steps are performed untill the convergence condition is
satified and the loop is aborted. The line marking the end of the loop is
"------------------ aborting loop because EDIFF is reached -----------------".
From this line on, starts a section summarizing the results of the iteration
and the data allows to initialize the UMDSnapshot.

The different types of informaation are grouped in different sections:

+ Electric charge distribution
  #  total charge
  #
  # # of ion       s       p       d     [...]     tot
  # --------------------------------------------------
  #     1         ...     ...     ...              ...
  #     2         ...     ...     ...              ...
  #    ...
  # --------------------------------------------------
  # tot           ...     ...     ...              ...
  -> to obtain the electric charge distribution of each atoms in each orbital

+ Magnetic moment distribution
  #  magnetization (x)
  #
  # # of ion       s       p       d     [...]     tot
  # --------------------------------------------------
  #     1         ...     ...     ...              ...
  #     2         ...     ...     ...              ...
  #    ...
  # --------------------------------------------------
  # tot           ...     ...     ...              ...
  -> to obtain the magnetic moment distribution of each atoms in each orbital

+ Stress tensor information
  #   FORCE on cell =-STRESS in cart. coord.  units (eV):
  #   Direction    XX        YY        ZZ        XY        YZ        ZX
  # -------------------------------------------------------------------
  # ...           ...       ...       ...       ...       ...       ...
  # ...
  # -------------------------------------------------------------------
  # Total         ...       ...       ...       ...       ...       ...
  # in kB         ...       ...       ...       ...       ...       ...
  # external pressure =      ... kB         Pullay stress =      ... kB
  #
  # kinetic pressure (ideal gas correction) =     ... kB
  # total pressure  =    ... kB
  # Total+kin.    ...       ...       ...       ...       ...       ...
  -> to obtain information on the stress tensor and the pressure on the cell

+ Unit cell transformation
  # VOLUME and BASIS-vectors are now :
  # ------------------------------------------------------------------
  # energy-cutoff  :  ...
  # volume of cell :  ...
  # direct lattice vectors              reciprocal lattice vectors
  # dir_a_x     dir_a_y     dir_a_Z     rec_a_x     rec_a_y     rec_a_z
  # dir_a_x     dir_a_y     dir_a_Z     rec_a_x     rec_a_y     rec_a_z
  # dir_a_x     dir_a_y     dir_a_Z     rec_a_x     rec_a_y     rec_a_z
  #
  # length of vectors
  # norm_dir_a  norm_dir_b  norm_dir_z  norm_rec_a  norm_rec_b  norm_rec_z
  -> to obtain new cell lattice deformations

+ Atomic force field
  # FORCES acting on ions
  #  electron-ion       ewald-force     non-local-force   conv-correction
  # -----------------------------------------------------------------------
  # ...   ...   ...   ...   ...   ...   ...   ...   ...   ...   ...   ...
  # ...
  # -----------------------------------------------------------------------
  #  (tot_ele-ion)      (tot_ewald)      (tot_nonloc)     (tot_conv-corr)
  #
  # POSITION                            TOTAL-FORCE (eV/Angst)
  # ------------------------------------------------------------------------
  # position_x  position_y  position_z  force_x     force_y     force_z
  # ...
  # ------------------------------------------------------------------------
  # total drift:                        totforce_x  totforce_y  totforce_z
  -> to obtain the new atoms positions and the total force acting on them

+ Energy of the system recap
  # FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
  # ---------------------------------------------------
  # free  energy   TOTEN  =          ... eV
  # energy without entropy=          ...    energy(sigma->0) =          ...
  #
  # (... electron-energy time convergence consideration)
  # (... ion-step motion time and RANDOM_SEED value used)
  #
  #   ENERGY OF THE ELECTRON-ION-THERMOSTAT SYSTEM (eV)
  #   ---------------------------------------------------
  # % ion-electron   TOTEN  =              ...  see above
  #   kinetic energy EKIN   =              ...
  #   kin. lattice  EKIN_LAT=              ...  (temperature ... K)
  #   nose potential ES     =              ...
  #   nose kinetic   EPS    =              ...
  #   ---------------------------------------------------
  #   total energy   ETOTAL =              ... eV
  #
  # (... projector operation and memory-time consumption recap)
  #
  -> to obtain information about the system energy

After this section another simulation iteration starts with its convergence
loop and so on. The total number of iteration depends on the number of steps
set among the molecular dynamics parameters (NSW).
"""


import numpy as np


def load_UMDSnapshot_from_outcar(outcar, snapshot):
    """
    Read the data and initialize the UMDSnapshot object.

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.
    simulation : simulation object
        A simulation object with information about the lattice.
    step : int
        The identificative step number.

    Returns
    -------
    snapshot : UMDSnapshot object
        A UMDSnapshot object with information about the thermodynamic
        quantities and the atoms dynamics of the current snapshot in the
        stream.

    Raises
    ------
    EOFError :
        If the OUTCAR file ends with uncomplete snapshot information.

    """
    natoms = snapshot.natoms

    # Declare the thermodynamics quantities
    temperature = 0
    pressure = 0
    stress = 0
    energy = 0

    position = np.zeros((natoms, 3), dtype=float)
    velocity = np.zeros((natoms, 3), dtype=float)
    force = np.zeros((natoms, 3), dtype=float)
    charges = np.zeros(natoms, dtype=float)
    magnets = np.zeros(natoms, dtype=float)

    for line in outcar:
        if "total charge" in line:
            charges = load_charges(outcar, natoms)
        if "magnetization (x)" in line:
            magnets = load_magnets(outcar, natoms)
        if "FORCE on cell =-STRESS" in line:
            stress = load_stress(outcar)
            pressure = np.mean(stress[:3])
        if "FORCES acting on ions" in line:
            position, force = load_dynamics(outcar, natoms)
        if "ENERGY OF THE ELECTRON-ION-THERMOSTAT SYSTEM (eV)" in line:
            energy, temperature = load_energy(outcar)

            # Since the energy is the last snapshot section, after that we
            # can initialize the UMDSnapDynamics and UMDSnapThermodynamics
            # objecta and return the UMDSnapshot.
            snapshot.setThermodynamics(temperature, pressure, energy)
            snapshot.setDynamics(position, velocity, force)
            return snapshot

    raise(EOFError('OUTCAR file ended but the last snapshot is uncomplete.'))


def load_charges(outcar, natoms):
    """
    Load the electric charge value distribution of each atom in the orbitals.

    The electric charge section is analyzed and once at the beginning of the
    part with the data, a for loop over all the atoms available is performed.
    The section structure is the following and the first line is already read.
    "  total charge
    ->
      # of ion       s       p       d     [...]     tot
      --------------------------------------------------
          1         ...     ...     ...              ... "

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.
    natoms : int
        The number of atoms in the lattice.

    Returns
    -------
    charges: array.
        Array of the electric charge distribution of each atom in orbitals.

    """
    line = outcar.readline()    # read the blank line
    header = outcar.readline()  # read the header '# of ion      s      p ...'
    line = outcar.readline()    # read the separator '-----------------------'
    norbitals = len(header.replace('# of ion', '').strip().split())
    charges = np.zeros((natoms, norbitals), dtype=float)
    for i in range(natoms):
        atom_charge = outcar.readline().strip().split()
        charges[i] = atom_charge[1:]
    return charges


def load_magnets(outcar, natoms):
    """
    Load the magnetic moment distribution of each atom in the orbitals.

    The magnetic moment section is analyzed and once at the beginning of the
    part with the data, a for loop over all the atoms available is performed.
    The section structure is the following and the first line is already read.
    "  magnetization (x)
    ->
      # of ion       s       p       d     [...]     tot
      --------------------------------------------------
          1         ...     ...     ...              ... "

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.
    natoms : int
        The number of atoms in the lattice.

    Returns
    -------
    charges: array.
        Array of the magnetic moment distribution of each atom in  orbitals.

    """
    line = outcar.readline()    # read the blank line
    header = outcar.readline()
    line = outcar.readline()    # read the separator -----------------
    norbitals = len(header.replace('# of ion', '').strip().split())
    magnets = np.zeros((natoms, norbitals), dtype=float)
    for i in range(natoms):
        atom_magnet = outcar.readline().strip().split()
        magnets[i] = atom_magnet[1:]
    return magnets


def load_stress(outcar):
    """
    Load the stress tensor values on the cell.

    The stress tensor section is analized and the Total+kin stress components
    are saved. It has the following and the first line is already read.
    "   FORCE on cell =-STRESS in cart. coord.  units (eV):
    -> Direction    XX        YY        ZZ        XY        YZ        ZX
      -------------------------------------------------------------------
      ...           ...       ...       ...       ...       ...       ...
      ...
      -------------------------------------------------------------------
      Total         ...       ...       ...       ...       ...       ...
      in kB         ...       ...       ...       ...       ...       ...
      external pressure =      ... kB         Pullay stress =      ... kB

      kinetic pressure (ideal gas correction) =     ... kB
      total pressure  =    ... kB
      Total+kin.    ...       ...       ...       ...       ...       ... "

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.

    Returns
    -------
    stress: array.
        Array of the stress components (xx, yy, zz, xy, yz, zx).
    """
    stress = np.zeros(6, dtype=float)
    for line in outcar:
        if "Total+kin." in line:
            stress = np.array(line.strip().split()[1:], dtype=float)
            stress = stress/10.   # to convert it from kBar to GPa
            return stress


def load_dynamics(outcar, natoms):
    """
    Load the position and the force acting on each atom.

    The dynamics section is analized and and once at the beginning of the
    part with the data (starting with "POSITION [...] TOTAL-FORCE (eV/Angst)"),
    a for loop over all the atoms available is performed to read position and
    force. It has the following structure and the first line is already read.
    " FORCES acting on ions
      electron-ion       ewald-force     non-local-force   conv-correction
      -----------------------------------------------------------------------
      ...   ...   ...   ...   ...   ...   ...   ...   ...   ...   ...   ...
      ...
      -----------------------------------------------------------------------
       (tot_ele-ion)      (tot_ewald)      (tot_nonloc)     (tot_conv-corr)

      POSITION                            TOTAL-FORCE (eV/Angst)
      ------------------------------------------------------------------------
      position_x  position_y  position_z  force_x     force_y     force_z
      ...
      ------------------------------------------------------------------------
      total drift:                        totforce_x  totforce_y  totforce_z

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.
    natoms : int
        The number of atoms in the lattice.

    Returns
    -------
    position : array
        Array of the atoms positions.
    force : array
        Array of the atoms forces.

    """
    dynamics = np.zeros((natoms, 6), dtype=float)
    for line in outcar:
        if "POSITION" in line and "TOTAL-FORCE (eV/Angst)" in line:
            line = outcar.readline()    # read the separator ---------
            for i in range(natoms):
                dynamics[i] = outcar.readline().strip().split()
            position = dynamics[:, :3]
            force = dynamics[:, 3:]
            return position, force


def load_energy(outcar):
    """
    Load the internal energy and the temperature of the electron-ion system.

    From the energy section, different energy contributions are analyzed and
    the 'ETOTAL' energy and the temperature reported in the 'kin. lattice
    EKIN_LAT' parameter are returned.
    The section structure is the following and the first line is already read.
    " FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
    ->---------------------------------------------------
      free  energy   TOTEN  =          ... eV
      energy without entropy=          ...    energy(sigma->0) =          ...

      (... electron-energy time convergence consideration)
      (... ion-step motion time and RANDOM_SEED value used)

        ENERGY OF THE ELECTRON-ION-THERMOSTAT SYSTEM (eV)
        ---------------------------------------------------
      % ion-electron   TOTEN  =              ...  see above
        kinetic energy EKIN   =              ...
        kin. lattice  EKIN_LAT=              ...  (temperature ... K)
        nose potential ES     =              ...
        nose kinetic   EPS    =              ...
        ---------------------------------------------------
        total energy   ETOTAL =              ... eV                          "

    Parameters
    ----------
    outcar : input file
        The OUTCAR file.

    Returns
    -------
    energy : float
        System total internal energy.
    temperature : float
        System temperature.

    """
    energy = 0.0
    temperature = 0.0
    for line in outcar:
        if "lattice  EKIN_LAT=" in line:
            temperature = float(line.strip().split()[-2])
        elif "ETOTAL" in line:
            energy = float(line.strip().split()[-2])
            return energy, temperature
