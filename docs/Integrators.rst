Integrators
===========

.. include:: IntegratorsIntro.rst

- :ref:`BBK`

- :ref:`EulerMaruyama`

- :ref:`EulerMaruyamaRigidBody`

- :ref:`EulerMaruyamaRigidBodyPatchesState`

- :ref:`GFJ`

- :ref:`MagneticBrownian`

- :ref:`NVE`



----

BBK
---

	:author: Pablo Ibáñez-Freire

 BBK integrator for the NVT ensemble. This Langevin integrator is designed for simulations that maintain a constant number of particles, volume, and temperature. It is particularly useful for molecular dynamics simulations requiring stochastic thermal noise and friction.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - frictionConstant
	  - Friction constant of the integrator
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "BBK",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"frictionConstant": 0.1
		}
	}



----

EulerMaruyama
-------------

	:author: Pablo Ibáñez-Freire

 Simple Euler-Maruyama integrator for Brownian dynamics. This integrator is suitable for simulations involving stochastic processes, particularly in fluid environments with defined viscosity.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - viscosity
	  - Viscosity of the fluid
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "EulerMaruyama",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"viscosity": 0.01
		}
	}



----

EulerMaruyamaRigidBody
----------------------

	:author: Pablo Ibáñez-Freire

 Euler-Maruyama integrator for rigid bodies, based on the approach detailed in DOI: 10.1063/1.4932062. Suitable for simulations involving Brownian dynamics of rigid bodies in a viscous fluid.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - viscosity
	  - Viscosity of the fluid
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "EulerMaruyamaRigidBody",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"viscosity": 0.01
		}
	}



----

EulerMaruyamaRigidBodyPatchesState
----------------------------------

	:author: Pablo Ibáñez-Freire

 Euler-Maruyama integrator designed for rigid bodies with patches state. This integrator extends the standard Euler-Maruyama approach to accommodate simulations involving rigid bodies with specific patches states, adding complexity and realism to the simulated dynamics. The update of the patches state is performed using the a Monte Carlo approach, after the Euler-Maruyama update of the rigid body state. Random numbers are generated and used to decide whether a patch is going to be update its state or not.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - viscosity
	  - Viscosity of the fluid
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "EulerMaruyamaRigidBodyPatchesState",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"viscosity": 0.01
		}
	}



----

GFJ
---

	:author: Pablo Ibáñez-Freire

 GJF integrator, a Langevin integrator for the NVT ensemble, as described in DOI: 10.1080/00268976.2012.760055. This integrator is designed for simulations that maintain a constant number of particles, volume, and temperature, incorporating stochastic thermal noise and friction in the dynamics.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - frictionConstant
	  - Friction constant of the integrator
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "GFJ",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"frictionConstant": 0.1
		}
	}



----

MagneticBrownian
----------------

	:author: P. Palacios-Alonso

 Simple Euler-Maruyama integrator adapted for Brownian dynamics with magnetic properties. It is designed for simulating the behavior of magnetically responsive particles in a fluid, considering viscosity, gyromagnetic ratio, damping, and saturation magnetization.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - magneticIntegrationAlgorithm
	  - Algorithm for magnetic integration
	  - string
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 
	* - msat
	  - Saturation magnetization
	  - float
	  - 
	* - viscosity
	  - Viscosity of the fluid
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
	* - damping
	  - Damping factor
	  - float
	  - 
	* - gyroRatio
	  - Gyromagnetic ratio
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "MagneticBrownian",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001,
			"viscosity": 0.01,
			"gyroRatio": 2.8,
			"damping": 0.1,
			"msat": 1.0,
			"magneticIntegrationAlgorithm": "algorithmName"
		}
	}



----

NVE
---

	:author: Pablo Ibáñez-Freire

 NVE integrator for simulations maintaining a constant number of particles, volume, and energy. This integrator is suitable for closed-system simulations where energy exchange with the environment is not considered.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - timeStep
	  - Time step of the integrator
	  - float
	  - 
	* - integrationSteps
	  - Number of integration steps
	  - int
	  - 

Example:

.. code-block:: python

	{
		"type": "NVE",
		"parameters":{
			"integrationSteps": 10000,
			"timeStep": 0.001
		}
	}



