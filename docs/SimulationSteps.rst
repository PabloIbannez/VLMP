SimulationSteps
===============

.. include:: SimulationStepsIntro.rst

- :ref:`AFMMaxForce`

- :ref:`afmMeasurement`

- :ref:`anglesMeasurement`

- :ref:`centerOfMassMeasurement`

- :ref:`forceBetweenSetsMeasurement`

- :ref:`gyrationRadius`

- :ref:`heightMeasurement`

- :ref:`info`

- :ref:`lambdaActivation`

- :ref:`lambdaCycle`

- :ref:`meanMagnetizationMeasurement`

- :ref:`meanRadius`

- :ref:`meanSquareDisplacement`

- :ref:`nativeContactsMeasurement`

- :ref:`oscillatoryForceMeasurement`

- :ref:`pairwiseForces`

- :ref:`patchPolymersMeasurement`

- :ref:`potentialEnergyMeasurement`

- :ref:`potentialMeasurement`

- :ref:`savePatchyParticlesState`

- :ref:`saveState`

- :ref:`stressMeasurement`

- :ref:`thermodynamicIntegration`

- :ref:`thermodynamicMeasurement`

- :ref:`vqcmMeasurement`

- :ref:`vqcmMeasurementFromMobility`



----

AFMMaxForce
-----------

	:author: Pablo Ibáñez-Freire

 Implements a maximum force criterion for Atomic Force Microscopy (AFM) simulations. 

 This step terminates the simulation when a specified maximum force is reached.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - maxForce
	  - The maximum force threshold for terminating the simulation.
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "AFMMaxForce",
		"parameters":{
			"maxForce": 1000.0
		}
	}



----

afmMeasurement
--------------

	:author: Pablo Ibáñez-Freire

 Performs measurements for Atomic Force Microscopy (AFM) simulations, recording force-distance data.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for AFM measurements.
	  - str
	  - afm_measurement.dat

Example:

.. code-block:: python

	{
		"type": "afmMeasurement",
		"parameters":{
			"outputFilePath": "afm_data.dat"
		}
	}



----

anglesMeasurement
-----------------

	:author: Pablo Ibáñez-Freire

 Measures angles between specified triplets of particles in the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for angle measurements.
	  - str
	  - angles.dat
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particle triplets for angle measurement.
	  - list of triplets

Example:

.. code-block:: python

	{
		"type": "anglesMeasurement",
		"parameters":{
			"outputFilePath": "angle_data.dat",
			"selection": "model1 forceField ANGLES"
		}
	}



----

centerOfMassMeasurement
-----------------------

	:author: Pablo Ibáñez-Freire

 Measures the center of mass of a selected group of particles throughout the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for center of mass measurements.
	  - str
	  - com.dat
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for center of mass calculation.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "centerOfMassMeasurement",
		"parameters":{
			"outputFilePath": "com_data.dat",
			"selection": "model1 type A B C"
		}
	}



----

forceBetweenSetsMeasurement
---------------------------

	:author: Pablo Palacios-Alonso

 Measures the force between two sets of particles in the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - setName_idList
	  - Dictionary mapping set names to lists of particle IDs.
	  - dict
	  - 
	* - outputFilePath
	  - Path to the output file for force measurements.
	  - str
	  - force_between_sets.dat

Example:

.. code-block:: python

	{
		"type": "forceBetweenSetsMeasurement",
		"parameters":{
			"outputFilePath": "force_data.dat",
			"setName_idList": {'set1': [1, 2, 3], 'set2': [4, 5, 6]}
		}
	}



----

gyrationRadius
--------------

	:author: Pablo Ibáñez-Freire

 Calculates the radius of gyration for a selected group of particles over time.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for gyration radius measurements.
	  - str
	  - gyration_radius.dat
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for gyration radius calculation.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "gyrationRadius",
		"parameters":{
			"outputFilePath": "gyration_data.dat",
			"selection": "model1 type protein"
		}
	}



----

heightMeasurement
-----------------

	:author: Pablo Ibáñez-Freire

 Measures the height of selected particles, typically used in surface-based simulations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for height measurements.
	  - str
	  - height.dat
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - particleNumberAverage
	  - Number of particles to average for height calculation.
	  - int
	  - 1
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for height measurement.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "heightMeasurement",
		"parameters":{
			"outputFilePath": "height_data.dat",
			"particleNumberAverage": 5,
			"selection": "model1 type surface"
		}
	}



----

info
----

	:author: Pablo Ibáñez-Freire

 Provides basic information about the simulation progress, including current step, estimated remaining time, and mean FPS.


Example:

.. code-block:: python

	{
		"type": "info",
		"parameters":
		}
	}



----

lambdaActivation
----------------

	:author: Pablo Ibáñez-Freire

 Controls the activation of lambda parameter in thermodynamic integration simulations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - lambdaValues
	  - List of lambda values to use in the simulation.
	  - list of float
	  - [0.0, 1.0]
	* - lambdaValueStep
	  - Step size for changing lambda value.
	  - float
	  - 0.1

Example:

.. code-block:: python

	{
		"type": "lambdaActivation",
		"parameters":{
			"lambdaValueStep": 0.1,
			"lambdaValues": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
		}
	}



----

lambdaCycle
-----------

	:author: Pablo Ibáñez-Freire

 Implements a cycle of lambda values for enhanced sampling in thermodynamic integration.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - activationStep
	  - Number of steps for each lambda activation phase.
	  - int
	  - 1000
	* - pauseStep
	  - Number of steps for pause between lambda changes.
	  - int
	  - 100
	* - measureStep
	  - Number of steps for measurement at each lambda value.
	  - int
	  - 500
	* - lambdaValues
	  - List of lambda values to cycle through.
	  - list of float
	  - [0.0, 1.0]

Example:

.. code-block:: python

	{
		"type": "lambdaCycle",
		"parameters":{
			"activationStep": 1000,
			"measureStep": 500,
			"pauseStep": 100,
			"lambdaValues": [0.0, 0.25, 0.5, 0.75, 1.0]
		}
	}



----

meanMagnetizationMeasurement
----------------------------

	:author: P. Palacios Alonso

 Measures the mean magnetization of selected magnetic particles in the system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for mean magnetization measurements.
	  - str
	  - mean_magnetization.dat
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of magnetic particles for magnetization measurement.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "meanMagnetizationMeasurement",
		"parameters":{
			"outputFilePath": "magnetization_data.dat",
			"selection": "model1 type magnetic"
		}
	}



----

meanRadius
----------

	:author: Pablo Ibáñez-Freire

 Calculates the mean radius of selected particles over time.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for mean radius measurements.
	  - str
	  - mean_radius.dat
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for mean radius calculation.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "meanRadius",
		"parameters":{
			"outputFilePath": "radius_data.dat",
			"selection": "model1 type sphere"
		}
	}



----

meanSquareDisplacement
----------------------

	:author: Pablo Diez-Silva

 Calculates the mean square displacement (MSD) of selected particles over time.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for MSD measurements.
	  - str
	  - msd.dat
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for MSD calculation.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "meanSquareDisplacement",
		"parameters":{
			"outputFilePath": "msd_data.dat",
			"selection": "model1 type diffusive"
		}
	}



----

nativeContactsMeasurement
-------------------------

	:author: Pablo Ibáñez-Freire

 Measures the native contacts between selected pairs of particles, typically used in protein folding simulations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for native contacts measurements.
	  - str
	  - native_contacts.dat
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particle pairs for native contacts measurement.
	  - list of pairs

Example:

.. code-block:: python

	{
		"type": "nativeContactsMeasurement",
		"parameters":{
			"outputFilePath": "contacts_data.dat",
			"selection": "model1 contacts 1:5 6:10 11:15"
		}
	}



----

oscillatoryForceMeasurement
---------------------------

	:author: Pablo Palacios-Alonso

 Performs oscillatory force measurements to study viscoelastic properties of the system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - fluidDensity
	  - Density of the fluid.
	  - float
	  - 
	* - outputFilePath
	  - Path to the output file for oscillatory force measurements.
	  - str
	  - 
	* - id_and_force
	  - Dictionary of particle IDs and corresponding force amplitudes.
	  - dict
	  - 
	* - hydrodynamicRadius
	  - Hydrodynamic radius of the particles.
	  - float
	  - 
	* - f
	  - Frequency of the oscillatory force.
	  - float
	  - 
	* - viscosity
	  - Viscosity of the fluid.
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - tolerance
	  - Tolerance for Gaussian kernel. Only used if kernel is 'Gaussian'.
	  - float
	  - 1e-05
	* - memory
	  - Number of previous steps to consider in the solver.
	  - int
	  - 15
	* - h
	  - Step size for numerical integration. If 0, it's computed automatically.
	  - float
	  - 0.0
	* - damping
	  - Damping factor for the solver.
	  - float
	  - 1e-05
	* - maxNIterations
	  - Maximum number of iterations for the solver.
	  - int
	  - 10000
	* - toleranceConvergence
	  - Convergence tolerance for the solver.
	  - float
	  - 0.0001
	* - kernel
	  - Kernel function for force calculation. Options: 'Gaussian' or 'Peskin3p'.
	  - str
	  - Peskin3p
	* - printSteps
	  - Number of steps between prints of intermediate results.
	  - int
	  - 0
	* - notAcceleratedInterval
	  - Interval of non-accelerated steps in the solver.
	  - int
	  - 2

Example:

.. code-block:: python

	{
		"type": "oscillatoryForceMeasurement",
		"parameters":{
			"outputFilePath": "oscforce_results.dat",
			"f": 1000000.0,
			"hydrodynamicRadius": 1e-09,
			"viscosity": 0.001,
			"fluidDensity": 1000,
			"kernel": "Gaussian",
			"tolerance": 1e-06,
			"maxNIterations": 20000,
			"toleranceConvergence": 1e-05,
			"memory": 20,
			"damping": 1e-06,
			"notAcceleratedInterval": 3,
			"h": 1e-06,
			"printSteps": 100
		}
	}



----

pairwiseForces
--------------

	:author: Pablo Palacios-Alonso

 Measures pairwise forces between particles in the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file where pairwise forces will be written.
	  - str
	  - 

Example:

.. code-block:: python

	{
		"type": "pairwiseForces",
		"parameters":{
			"outputFilePath": "pairwise_forces.dat"
		}
	}



----

patchPolymersMeasurement
------------------------

	:author: Pablo Ibáñez-Freire

 Measures properties of polymers created by dynamic bonded patchy particles, including size and surface bonding.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for polymer measurements.
	  - str
	  - 
	* - bufferSize
	  - Size of the buffer for measurements.
	  - int
	  - 
	* - surfaceEnergyThreshold
	  - Energy threshold for determining surface bonding.
	  - float
	  - 
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of patchy particles to measure.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "patchPolymersMeasurement",
		"parameters":{
			"outputFilePath": "patch_polymers.dat",
			"bufferSize": 1000,
			"surfaceEnergyThreshold": -1.0,
			"selection": "model1 type patchy"
		}
	}



----

potentialEnergyMeasurement
--------------------------

	:author: Pablo Ibáñez-Freire

 Measures the potential energy of selected particles or the entire system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for potential energy measurements.
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - potentials
	  - List of potential types to measure. If not specified, all potentials are measured.
	  - list of str
	  - 
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for potential energy measurement.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "potentialEnergyMeasurement",
		"parameters":{
			"outputFilePath": "potential_energy.dat",
			"potentials": ['LennardJones', 'Coulomb'],
			"selection": "model1 type A"
		}
	}



----

potentialMeasurement
--------------------

	:author: Pablo Ibáñez-Freire

 Measures the potential of individual particles in the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for potential measurements.
	  - str
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for potential measurement.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "potentialMeasurement",
		"parameters":{
			"outputFilePath": "particle_potentials.dat",
			"selection": "model1 type B"
		}
	}



----

savePatchyParticlesState
------------------------

	:author: Pablo Ibáñez-Freire

 Saves the state of patchy particles, including their positions and patch orientations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for saving the state.
	  - str
	  - 
	* - outputFormat
	  - Format of the output file (e.g., 'xyz', 'pdb', 'dcd').
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - pbc
	  - Whether to apply periodic boundary conditions when saving.
	  - bool
	  - False
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of patchy particles to save.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "savePatchyParticlesState",
		"parameters":{
			"outputFilePath": "patchy_state.xyz",
			"outputFormat": "xyz",
			"pbc": True,
			"selection": "model1 type patchy"
		}
	}



----

saveState
---------

	:author: Pablo Ibáñez-Freire

 Saves the current state of the simulation, including particle positions and velocities.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for saving the state.
	  - str
	  - 
	* - outputFormat
	  - Format of the output file (e.g., 'xyz', 'pdb', 'dcd').
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - pbc
	  - Whether to apply periodic boundary conditions when saving.
	  - bool
	  - False
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to save. If not specified, all particles are saved.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "saveState",
		"parameters":{
			"outputFilePath": "simulation_state.pdb",
			"outputFormat": "pdb",
			"pbc": True,
			"selection": "model1 all"
		}
	}



----

stressMeasurement
-----------------

	:author: Pablo Ibáñez-Freire

 Measures the stress tensor of the system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for stress tensor measurements.
	  - str
	  - 
	* - radiusCutOff
	  - Radius cutoff for the calculation of atom volumes.
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "stressMeasurement",
		"parameters":{
			"outputFilePath": "stress_tensor.dat",
			"radiusCutOff": 2.5
		}
	}



----

thermodynamicIntegration
------------------------

	:author: Pablo Ibáñez-Freire

 Performs thermodynamic integration to calculate free energy differences.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for thermodynamic integration results.
	  - str
	  - 
	* - stepLambda
	  - Step size for lambda parameter in the integration.
	  - float
	  - 
	* - lambdaValues
	  - List of lambda values for the integration.
	  - list of float
	  - 

Example:

.. code-block:: python

	{
		"type": "thermodynamicIntegration",
		"parameters":{
			"outputFilePath": "ti_results.dat",
			"stepLambda": 0.1,
			"lambdaValues": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
		}
	}



----

thermodynamicMeasurement
------------------------

	:author: Pablo Ibáñez-Freire

 Measures various thermodynamic properties of the system, including energy, temperature, and pressure.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - outputFilePath
	  - Path to the output file for thermodynamic measurements.
	  - str
	  - 
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles for thermodynamic measurements. If not specified, all particles are included.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "thermodynamicMeasurement",
		"parameters":{
			"outputFilePath": "thermo.dat",
			"selection": "model1 all"
		}
	}



----

vqcmMeasurement
---------------

	:author: Pablo Palacios-Alonso and Pablo Ibáñez-Freire

 Performs Virtual Quartz Crystal Microbalance (VQCM) measurements to study viscoelastic properties of the system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - fluidDensity
	  - Density of the fluid.
	  - float
	  - 
	* - outputFilePath
	  - Path to the output file for VQCM measurements.
	  - str
	  - 
	* - f0
	  - Fundamental frequency of the quartz crystal.
	  - float
	  - 
	* - hydrodynamicRadius
	  - Hydrodynamic radius of the particles.
	  - float
	  - 
	* - viscosity
	  - Viscosity of the fluid.
	  - float
	  - 
	* - overtone
	  - Overtone number for the measurement.
	  - int
	  - 
	* - vwall
	  - Velocity of the wall.
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - tolerance
	  - Tolerance for Gaussian kernel. Only used if kernel is 'Gaussian'.
	  - float
	  - 1e-05
	* - memory
	  - Number of previous steps to consider in the solver.
	  - int
	  - 5
	* - h
	  - Step size for numerical integration. If 0, it's computed automatically.
	  - float
	  - 0.0
	* - damping
	  - Damping factor for the solver.
	  - float
	  - 1e-05
	* - toleranceConvergence
	  - Convergence tolerance for the solver.
	  - float
	  - 0.0001
	* - tetherInteractorNames
	  - List of names for tether interactors.
	  - list of str
	  - 
	* - printSteps
	  - Number of steps between prints of intermediate results.
	  - int
	  - 0
	* - notAcceleratedInterval
	  - Interval of non-accelerated steps in the solver.
	  - int
	  - 2
	* - maxNIterations
	  - Maximum number of iterations for the solver.
	  - int
	  - 10000
	* - kernel
	  - Kernel function for force calculation. Options: 'Gaussian' or 'Peskin3p'.
	  - str
	  - Peskin3p
	* - resonatorImpedance
	  - Impedance of the resonator. If -1, it's ignored by UAMMD.
	  - float
	  - -1.0

Example:

.. code-block:: python

	{
		"type": "vqcmMeasurement",
		"parameters":{
			"outputFilePath": "vqcm_results.dat",
			"f0": 5000000.0,
			"overtone": 3,
			"hydrodynamicRadius": 1e-09,
			"viscosity": 0.001,
			"vwall": 0.001,
			"fluidDensity": 1000,
			"kernel": "Gaussian",
			"tolerance": 1e-06,
			"maxNIterations": 20000,
			"toleranceConvergence": 1e-05,
			"memory": 10,
			"damping": 1e-06,
			"notAcceleratedInterval": 3,
			"h": 1e-06,
			"resonatorImpedance": 1000000.0,
			"printSteps": 100,
			"tetherInteractorNames": ['tether1', 'tether2']
		}
	}



----

vqcmMeasurementFromMobility
---------------------------

	:author: Pablo Palacios-Alonso

 Performs Virtual Quartz Crystal Microbalance (VQCM) measurements from mobility data to study viscoelastic properties of the system.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - fluidDensity
	  - Density of the fluid.
	  - float
	  - 
	* - outputFilePath
	  - Path to the output file for VQCM measurements.
	  - str
	  - 
	* - f0
	  - Fundamental frequency of the quartz crystal.
	  - float
	  - 
	* - hydrodynamicRadius
	  - Hydrodynamic radius of the particles.
	  - float
	  - 
	* - viscosity
	  - Viscosity of the fluid.
	  - float
	  - 
	* - overtone
	  - Overtone number for the measurement.
	  - int
	  - 
	* - vwall
	  - Velocity of the wall.
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - tolerance
	  - Tolerance for Gaussian kernel. Only used if kernel is 'Gaussian'.
	  - float
	  - 1e-05
	* - h
	  - Step size for numerical integration. If 0, it's computed automatically.
	  - float
	  - 0.0
	* - kernel
	  - Kernel function for force calculation. Options: 'Gaussian' or 'Peskin3p'.
	  - str
	  - Peskin3p
	* - tetherInteractorNames
	  - List of names for tether interactors.
	  - list of str
	  - 
	* - resonatorImpedance
	  - Impedance of the resonator. If -1, it's ignored by UAMMD.
	  - float
	  - -1.0

Example:

.. code-block:: python

	{
		"type": "vqcmMeasurementFromMobility",
		"parameters":{
			"outputFilePath": "vqcm_mobility_results.dat",
			"f0": 5000000.0,
			"overtone": 3,
			"hydrodynamicRadius": 1e-09,
			"viscosity": 0.001,
			"vwall": 0.001,
			"fluidDensity": 1000,
			"kernel": "Gaussian",
			"tolerance": 1e-06,
			"h": 1e-06,
			"resonatorImpedance": 1000000.0,
			"tetherInteractorNames": ['tether1', 'tether2']
		}
	}



