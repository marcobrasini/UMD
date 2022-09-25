# UMD package

The project implements the **UMDVaspParser** function for parsing the results of a molecular dynamics simulation made with the Vasp package.

The UMDVaspParser function converts the OUTCAR file obtained from a Vasp simulation, into a more readable UMD file.


## UMD file example

The UMD file structure generated by the UMDVaspParser function has a simple structure. 
+ A section summarizing the general simulation information like the number of molecular dynamics steps and their time duration.

	```
	Simulation: OUTCAR_multiple               
	  Total cycles =            3
	  Total steps  =         1900
	  Total time   =      850.000 fs

	Run        0:
	  Steps     =      300
	  Step time =    0.500 (fs)
	Run        1:
	  Steps     =      600
	  Step time =    0.500 (fs)
	Run        2:
	  Steps     =     1000
	  Step time =    0.400 (fs)
	```

+ A section reporting the characteristics of the periodic lattice structure used for the simulation.

	```
	Lattice: 3bccH2O+1Fe                   
	       5.700000        0.000000        0.000000
	       0.000000        5.700000        0.000000
	       0.000000        0.000000        5.700000
	O         H         Fe       
	     16.0       1.0     55.85
	      6.0       1.0       8.0
	       15        28         1
	```
 
+ A section listing, for every snapshot (or simulation step), the system's thermodynamic quantities (like temperature, pressure and energy) and the ions' dynamic data (position, velocity and force coordinates).

	```
	Snapshot:          0
	Thermodynamics:
  	Temperature =    1804.370000 K
  	Pressure    =      24.652533 GPa
  	Energy      =    -192.707742 eV
	Dynamics:        0.500 fs
	Position_x      Position_y      Position_z      Velocity_x      Velocity_y      Velocity_z      Force_x         Force_y         Force_z         
	      5.69600000      5.69749000      0.00046000      0.00000000      0.00000000      0.00000000      0.31302000      0.30705300      0.14822600
	      0.00364000      0.00356000      2.84787000      0.00000000      0.00000000      0.00000000      0.65081300      0.57985500     -0.77866100
	      0.00563000      2.84499000      5.69930000      0.00000000      0.00000000      0.00000000      0.54635500     -0.61306800      0.70719600
	      5.69597000      2.85071000      2.84751000      0.00000000      0.00000000      0.00000000      0.33261100     -0.20250400     -0.20863600
	      2.84784000      0.00074000      0.00233000      0.00000000      0.00000000      0.00000000     -0.62123400      0.77716800      0.59520700
	      2.85261000      0.00425000      2.84564000      0.00000000      0.00000000      0.00000000     -0.23609800      0.14775600     -0.22563900
	      ...             ...             ...             ...             ...             ...             ...             ...             ...
	```

## Motivation

The UMD package wants to provides useful tools for the analysis of molecular dynamics simulation with Vasp.

The Vasp results are reported in the OUTCAR file. For a molecular dynamics simulation, the OUTCAR file is very big and contains more data than what is necessary for studying ion motion. 
The UMDVaspParser function in the UMD package allows converting and summarizing the OUTCAR data into a more readable UMD format. 

The aim of the project is to implement other analysis functions starting from the UMD file. For example the radial pair distribution function or the time correlation function.

In this way, the UMD package would become a universal package for studying the results of Vasp moleuclar dynamics simulations.


## Getting Started

### Prerequisites

For the execution of the code it is necessary to have a Python 3.9.7 compiler.
For testing the code it is necessary the Pytest framework and the hypothesis 6.54.6 package.


### Installation 

Download the code and save the package in the desired directory.

	git clone https://github.com/marcobrasini/UMD.git

Whenever the package is used, import the desired classes and the functions from the package.


### Testing

The package functions can be tested executing the command on the terminal.

	pytest


### Usage

#### Convert OUTCAR to UMD
To use the UMDVaspParser function to convert a Vasp OUTCAR file, it is necessary to import the UMDVaspParser function from the UMD package and execute the function with the name of an OUTCAR file.
The UMD output file is generated in the same directory as the input file.

	from UMD import UMDVaspParser

	UMDVaspParser('OUTCAR.outcar')

Some examples of OUTCAR file, can be found inside the UMD package in the directory 'UMD/tests/examples'. 	

#### Read from UMD
To read back the data from the UMD file, the first step is to load the simulation information with the *UMDSimulation_from_umd* method.

	from UMD import UMDSnapshot
	from UMD import UMDSimulation

	with open('UMD.umd') as umd:
		simulation = UMDSimulation()
		simulation.UMDSimulation_from_umd(umd)

Once the simulation is loaded, an empty snapshot must be created with the lattice information stored in the UMDSimulation object obtained.
Finally, a single snapshot is loaded from the UMD file with the *UMDSnapshot_from_umd* method. The snapshot to load is chosen by setting the index argument (for example the 20-th).

		snapshot = UMDSnapshot(lattice=simulation.lattice)
		snapshot.UMDSnapshot_from_umd(umd, index=19)


## Contacts

Marco Brasini - marco.brasini@studio.unibo.it
