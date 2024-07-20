Systems
=======

.. include:: SystemsIntro.rst

backup
------

	:author: Pablo Ibáñez-Freire

 Component used to add a backup system to the simulation. When this component is added to the simulation, the simulation will create a backup of the simulation every backupIntervalStep steps. The simulation will try to restore the simulation from the backup if the simulation crashes.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - backupIntervalStep
	  - Interval of steps between backups
	  - ullint
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - backupEndStep
	  - Step at which the backup ends
	  - ullint
	  - MAX_ULLINT
	* - backupStartStep
	  - Step at which the backup starts
	  - ullint
	  - 0
	* - backupFilePath
	  - Path to the backup file
	  - str
	  - backup

Example:

.. code-block:: python

	{
		"type": "backup",
		"backupIntervalStep": 1000,
		"backupFilePath": "backup"
	}



seed
----

	:author: Pablo Ibáñez-Freire

 This component sets the seed for the random number generator

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - seed
	  - Seed for the random number generator
	  - int
	  - 

Example:

.. code-block:: python

	{
		"type": "seed",
		"seed": 123456
	}



simulationName
--------------

	:author: Pablo Ibáñez-Freire

 Essential component for naming a simulation. This component is compulsory in every simulation configuration as each simulation requires a unique name. The 'simulationName' component assigns a descriptive and identifiable name to a simulation, facilitating its management and reference within the system. This name is used as the primary identifier for the simulation across various components and modules.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - simulationName
	  - Unique name assigned to the simulation
	  - str
	  - 

Example:

.. code-block:: python

	{
		"type": "simulationName",
		"simulationName": "MyUniqueSimulationName"
	}



