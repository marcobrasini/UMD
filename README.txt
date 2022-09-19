===============================================================================
                                 UMD package
===============================================================================

The project implements a code to analyze the results of a Molecular Dynamics
simulation made with the Vasp package.

The Vasp results are listed in the OUTCAR file. 
For a Molecular Dynamics simulation, the OUTCAR file is very big and contains
more data than what is necessary for studying ion motion. The UMD package
allows summarizing the system's thermodynamic and dynamic information into a
more readable format, into a UMD file.

The UMDVaspParser function is the main tool to extract the OUTCAR data and
save them into the UMD file.

More functions can be built starting from the UMD data and, for this purpose,
the UMDSimulation_from_umd and the UMDSnapshot_from_umd functions are defined.
These functions give access to the simulation parameters and snapshot data
respectively. 
The implementation of new functions based on the UMD would allow to have a
generic and universal package for the analysis of molecular dynamics 
simulations.  
 
To start with the package, try to first convert a Vasp OUTCAR file into a UMD
file. Into a new python module import the UMDVaspParser function from the UMD
package and pass the name of an OUTCAR file to the function as argument
(examples of OUTCAR file are reported into the UMD/tests/examples directory).

The UMD package is written in Python 3.9.7 and tested with Pytest.
