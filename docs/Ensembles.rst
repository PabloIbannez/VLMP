Ensembles
=========

.. include:: EnsemblesIntro.rst

- :ref:`NVT`

- :ref:`NVTlambda`



----

NVT
---

	:author: Pablo Ibáñez-Freire

 Component for setting up an NVT (constant Number of particles, Volume, and Temperature) ensemble in a simulation. This component is used to define the simulation environment with a fixed box size and temperature. It is essential for simulations that require a controlled temperature and volume, commonly used in molecular dynamics and other statistical mechanics simulations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - temperature
	  - Temperature of the simulation environment
	  - float
	  - 
	* - box
	  - Size of the simulation box
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "NVT",
		"parameters":{
			"box": 10.0,
			"temperature": 300.0
		}
	}



----

NVTlambda
---------

	:author: Pablo Ibáñez-Freire

 Component for setting up an NVTlambda ensemble in a simulation. This ensemble type extends the standard NVT (constant Number of particles, Volume, and Temperature) by introducing an additional lambda parameter, which is essential for thermodynamic integration. The component is used to define the simulation environment with a fixed box size, temperature, and the lambda value, enabling more complex thermodynamic calculations.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - temperature
	  - Temperature of the simulation environment
	  - float
	  - 
	* - lambda
	  - Lambda parameter for thermodynamic integration
	  - float
	  - 
	* - box
	  - Size of the simulation box
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "NVTlambda",
		"parameters":{
			"box": 10.0,
			"temperature": 300.0,
			"lambda": 0.5
		}
	}



