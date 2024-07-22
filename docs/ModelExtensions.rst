ModelExtensions
===============

.. include:: ModelExtensionsIntro.rst

- :ref:`ACMagneticField`

- :ref:`AFM`

- :ref:`LennardJones`

- :ref:`WCA`

- :ref:`absortionSurface`

- :ref:`addBond`

- :ref:`constantForce`

- :ref:`constantForceBetweenCentersOfMass`

- :ref:`constantForceOverCenterOfMass`

- :ref:`constantTorqueBetweenCentersOfMass`

- :ref:`constantTorqueOverCenterOfMass`

- :ref:`constraintCenterOfMassPosition`

- :ref:`constraintParticlesListPositionLambda`

- :ref:`constraintParticlesPosition`

- :ref:`constraintParticlesPositionLambda`

- :ref:`harmonicBondBetweenCentersOfMass`

- :ref:`helixBoundaries`

- :ref:`plates`

- :ref:`sphericalShell`

- :ref:`steric`

- :ref:`surface`

- :ref:`surfaceMaxForce`

- :ref:`uniformMagneticField`



----

ACMagneticField
---------------

	:author: P. Palacios-Alonso

 Applies an alternating current (AC) magnetic field to selected magnetic particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - frequency
	  - Frequency of the AC field
	  - float
	  - 
	* - b0
	  - Amplitude of the magnetic field
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
	* - direction
	  - Direction of the magnetic field
	  - list of float
	  - [0, 0, 1]

Example:

.. code-block:: python

	{
		"type": "ACMagneticField",
		"parameters":{
			"b0": 1.0,
			"frequency": 100.0,
			"direction": [0, 0, 1]
		}
	}



----

AFM
---

	:author: Pablo Ibáñez-Freire

 Atomic Force Microscopy (AFM) model extension for simulating AFM experiments. This extension add an interaction between a particle (the tip) and other set of particles (the sample). The interaction between the tip and the sample is modeled as a Lennard-Jones potential. The tip is modeled as a spherical particle with a spring attached to it.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - epsilon
	  - Energy parameter for tip-sample interaction
	  - float
	  - 
	* - K
	  - Spring constant for the AFM cantilever
	  - float
	  - 
	* - Kxy
	  - Lateral spring constant
	  - float
	  - 
	* - tipVelocity
	  - Velocity of the AFM tip
	  - float
	  - 
	* - sigma
	  - Distance parameter for tip-sample interaction
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
	* - indentationStartStep
	  - Simulation step to start indentation
	  - int
	  - 0
	* - indentationBackwardStep
	  - Simulation step to start backward indentation
	  - int
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - tip
	  - Selection for the AFM tip
	  - list of with one id, [id]
	* - sample
	  - Selection for the sample particles
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "AFM",
		"parameters":{
			"K": 1.0,
			"Kxy": 0.5,
			"epsilon": 1.0,
			"sigma": 1.0,
			"tipVelocity": 0.1,
			"indentationStartStep": 1000,
			"tip": "model1 type TIP",
			"sample": "model2"
		}
	}



----

LennardJones
------------

	:author: Pablo Ibáñez-Freire

 Implements Lennard-Jones potential between particles for non-bonded interactions.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - cutOffFactor
	  - Factor to multiply sigma to obtain the cut-off distance
	  - float
	  - 
	* - interactionMatrix
	  - Matrix of interaction parameters between different types of particles
	  - list of lists
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - condition
	  - Condition for the interaction (e.g., 'inter', 'intra')
	  - str
	  - inter
	* - addVerletList
	  - Whether to add a Verlet list for the interactions
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "LennardJones",
		"parameters":{
			"interactionMatrix": [['A', 'B', 1.0, 1.0], ['B', 'B', 0.5, 1.2]],
			"cutOffFactor": 2.5,
			"condition": "inter"
		}
	}



----

WCA
---

	:author: Pablo Ibáñez-Freire

 Adds Weeks-Chandler-Andersen (WCA) potential interactions between particles.

.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - cutOffFactor
	  - Factor to multiply the sigma parameter to obtain the cut-off distance.
	  - float
	  - 2.5
	* - epsilon
	  - Energy parameter for the WCA potential.
	  - float
	  - 1.0
	* - condition
	  - Condition for the interaction.
	  - str
	  - inter
	* - addVerletList
	  - If True, a Verlet list will be created for the interactions.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "WCA",
		"parameters":{
			"condition": "inter",
			"epsilon": 1.0,
			"cutOffFactor": 2.5,
			"addVerletList": True,
			"selection": "model1 all"
		}
	}



----

absortionSurface
----------------

	:author: Pablo Ibáñez-Freire

 Implements an absorption surface that attracts particles within a certain distance. Once the interaction starts this potential add an harmonic contraint to the particles that are below the heightThreshold

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - heightThreshold
	  - Height above the surface where absorption starts
	  - float
	  - 
	* - K
	  - Spring constant for the absorption force
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "absortionSurface",
		"parameters":{
			"heightThreshold": 5.0,
			"K": 10.0
		}
	}



----

addBond
-------

	:author: Pablo Ibáñez-Freire and Pablo Palacios

 Adds a harmonic bond between two particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for the bond
	  - float
	  - 
	* - r0
	  - Equilibrium distance of the bond
	  - float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection2
	  - Second particle in the bond
	  - list of ids
	* - selection1
	  - First particle in the bond
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "addBond",
		"parameters":{
			"K": 100.0,
			"r0": 1.0,
			"selection1": "model1 id 1",
			"selection2": "model1 id 2"
		}
	}



----

constantForce
-------------

	:author: Pablo Ibáñez-Freire

 Applies a constant force to a selection of particles. The force is applied over each individual particle.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - force
	  - Force vector to be applied.
	  - list of float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to which the force will be applied.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constantForce",
		"parameters":{
			"force": [0.0, 0.0, -9.8],
			"selection": "model1 type A B"
		}
	}



----

constantForceBetweenCentersOfMass
---------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a constant force between the centers of mass of two groups of particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - force
	  - Magnitude of the force to be applied.
	  - float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection2
	  - Selection for the second group of particles.
	  - list of ids
	* - selection1
	  - Selection for the first group of particles.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constantForceBetweenCentersOfMass",
		"parameters":{
			"force": 10.0,
			"selection1": "model1 chain A",
			"selection2": "model2 chain B"
		}
	}



----

constantForceOverCenterOfMass
-----------------------------

	:author: Pablo Ibáñez-Freire

 Applies a constant force to the center of mass of a selection of particles. The applied force is distributed among the particles in the selection according to their mass.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - force
	  - Force vector to be applied to the center of mass.
	  - list of float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles whose center of mass will be affected.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constantForceOverCenterOfMass",
		"parameters":{
			"force": [0.0, 0.0, -9.8],
			"selection": "model1 chain A"
		}
	}



----

constantTorqueBetweenCentersOfMass
----------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a constant torque between the centers of mass of two groups of particles. The torque is applied in such a way that the two groups of particles rotate in opposite directions around the axis defined by the vector

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - torque
	  - Magnitude of the torque to be applied
	  - float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection2
	  - Second group of particles
	  - list of ids
	* - selection1
	  - First group of particles
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constantTorqueBetweenCentersOfMass",
		"parameters":{
			"torque": 1.0,
			"selection1": "model1 chain A",
			"selection2": "model1 chain B"
		}
	}



----

constantTorqueOverCenterOfMass
------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a constant torque to the center of mass of selected particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - torque
	  - Torque vector to be applied
	  - list of float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Particles to apply the torque to
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constantTorqueOverCenterOfMass",
		"parameters":{
			"torque": [0.0, 0.0, 1.0],
			"selection": "model1 type ROTOR"
		}
	}



----

constraintCenterOfMassPosition
------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a constraint to the center of mass of a selection of particles. The potential energy of the constraint is given by a harmonic potential.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - position
	  - Position to constrain the center of mass to
	  - list of float
	  - 
	* - K
	  - Spring constant for the constraint
	  - float or list of float
	  - 
	* - r0
	  - Equilibrium distance from the constraint position
	  - float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Particles to apply the constraint to
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constraintCenterOfMassPosition",
		"parameters":{
			"K": [100.0, 100.0, 0.0],
			"r0": 0.0,
			"position": [0.0, 0.0, 0.0],
			"selection": "model1"
		}
	}



----

constraintParticlesListPositionLambda
-------------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a lambda-dependent positional constraint to a list of specified particles. The potential applied is a harmonic potential multiplied by a lambda-dependent factor (lambda^n).

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - ids
	  - List of particle IDs to be constrained.
	  - list of int
	  - 
	* - positions
	  - List of positions for each constrained particle.
	  - list of list of float
	  - 
	* - K
	  - Spring constant for the constraint.
	  - float or list of float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - n
	  - Exponent for the lambda dependence.
	  - int
	  - 2

Example:

.. code-block:: python

	{
		"type": "constraintParticlesListPositionLambda",
		"parameters":{
			"K": [100.0, 100.0, 100.0],
			"n": 2,
			"ids": [1, 2, 3],
			"positions": [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]
		}
	}

.. warning::

	This potential requires an ensemble which includes the 'Lambda' variable.



----

constraintParticlesPosition
---------------------------

	:author: Pablo Ibáñez-Freire

 Applies a positional constraint to a selection of particles. The constraint is a harmonic potential with a spring constant K.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for the constraint.
	  - float or list of float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to be constrained.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constraintParticlesPosition",
		"parameters":{
			"K": [100.0, 100.0, 100.0],
			"selection": "model1 type A B C"
		}
	}



----

constraintParticlesPositionLambda
---------------------------------

	:author: Pablo Ibáñez-Freire

 Applies a lambda-dependent positional constraint to a selection of particles. The applied potential is an harmonic potential with a lambda-dependent spring constant. (lambda^(n))

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for the constraint.
	  - float or list of float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - n
	  - Exponent for the lambda dependence.
	  - int
	  - 2
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to be constrained.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "constraintParticlesPositionLambda",
		"parameters":{
			"K": [100.0, 100.0, 100.0],
			"n": 2,
			"selection": "model1 type A B C"
		}
	}

.. warning::

	This potential requires an ensemble which includes the 'Lambda' variable.



----

harmonicBondBetweenCentersOfMass
--------------------------------

	:author: Pablo Ibáñez-Freire

 Adds a harmonic bond between the centers of mass of two groups of particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for the harmonic bond.
	  - float
	  - 
	* - r0
	  - Equilibrium distance for the harmonic bond.
	  - float
	  - 
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection2
	  - Selection for the second group of particles.
	  - list of ids
	* - selection1
	  - Selection for the first group of particles.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "harmonicBondBetweenCentersOfMass",
		"parameters":{
			"K": 100.0,
			"r0": 5.0,
			"selection1": "model1 chain A",
			"selection2": "model2 chain B"
		}
	}



----

helixBoundaries
---------------

	:author: Pablo Ibáñez-Freire

 Implements helical boundary conditions for simulations of helical structures.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for boundary conditions
	  - float
	  - 
	* - helixPitch
	  - Pitch of the helix
	  - float
	  - 
	* - helixInnerRadius
	  - Inner radius of the helix
	  - float
	  - 
	* - eps
	  - Helix handedness (1 for right-handed, -1 for left-handed)
	  - float
	  - 
	* - helixRadius
	  - Radius of the helix
	  - float
	  - 
	* - nPointsHelix
	  - Number of points to discretize the helix
	  - int
	  - 
	* - nz
	  - Number of points in z direction
	  - int
	  - 
	* - ny
	  - Number of points in y direction
	  - int
	  - 
	* - nTurns
	  - Number of turns in the helix
	  - int
	  - 
	* - nx
	  - Number of points in x direction
	  - int
	  - 
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Particles to apply helical boundaries to
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "helixBoundaries",
		"parameters":{
			"helixPitch": 5.0,
			"helixRadius": 10.0,
			"eps": 1.0,
			"nTurns": 5,
			"nPointsHelix": 100,
			"helixInnerRadius": 1.0,
			"nx": 10,
			"ny": 10,
			"nz": 50,
			"K": 100.0,
			"selection": "model1 all"
		}
	}



----

plates
------

	:author: Pablo Ibáñez-Freire

 Adds two parallel plates to the simulation box, typically used for confinement.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - platesSeparation
	  - Distance between the two plates.
	  - float
	  - 
	* - epsilon
	  - Energy parameter for plate-particle interactions.
	  - float
	  - 
	* - sigma
	  - Distance parameter for plate-particle interactions.
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
	* - compressionVelocity
	  - Velocity at which the plates are compressed.
	  - float
	  - 0.0
	* - minPlatesSeparation
	  - Minimum allowed separation between plates.
	  - float
	  - 
	* - maxPlatesSeparation
	  - Maximum allowed separation between plates.
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
	  - Selection of particles that interact with the plates.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "plates",
		"parameters":{
			"platesSeparation": 20.0,
			"epsilon": 1.0,
			"sigma": 1.0,
			"selection": "model1 all"
		}
	}



----

sphericalShell
--------------

	:author: Pablo Ibáñez-Freire

 Creates a spherical shell potential around a selection of particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - shellRadius
	  - Radius of the spherical shell. This can be set to 'auto' to automatically set the radius.
	  - float
	  - 
	* - shellCenter
	  - Center of the spherical shell.
	  - list of float
	  - [0.0, 0.0, 0.0]
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - shellSigma
	  - Distance parameter for the shell potential.
	  - float
	  - 1.0
	* - minShellRadius
	  - Minimum radius of the spherical shell.
	  - float
	  - 0.0
	* - radiusVelocity
	  - Velocity of the radius change.
	  - float
	  - 0.0
	* - shellEpsilon
	  - Energy parameter for the shell potential.
	  - float
	  - 1.0
	* - maxShellRadius
	  - Maximum radius of the spherical shell.
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
	  - Selection of particles to be confined within the shell.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "sphericalShell",
		"parameters":{
			"shellCenter": [0.0, 0.0, 0.0],
			"shellRadius": 10.0,
			"shellEpsilon": 1.0,
			"shellSigma": 1.0,
			"selection": "model1 all"
		}
	}



----

steric
------

	:author: Pablo Ibáñez-Freire

 Adds steric interactions between particles. If molecules are bonded, the interaction is not considered.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - cutOffFactor
	  - Factor to multiply the sigma parameter to obtain the cut-off distance.
	  - float
	  - 
	* - epsilon
	  - Energy parameter for the interaction.
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
	* - addVerletList
	  - If True, a Verlet list will be created for the interactions.
	  - bool
	  - True
	* - excludedBonds
	  - Number of bonds to exclude from the steric interactions.                                 This option is only available if addVerletList is True.                                 If excludedBonds > 0, the Verlet list will be created                                 with the non-bonded interactions and the excluded bonds.
	  - int
	  - 0
	* - condition
	  - Condition for the interaction.
	  - str
	  - inter

Example:

.. code-block:: python

	{
		"type": "steric",
		"parameters":{
			"condition": "inter",
			"epsilon": 1.0,
			"cutOffFactor": 2.5,
			"addVerletList": True,
			"selection": "model1 type A B C"
		}
	}



----

surface
-------

	:author: Pablo Ibáñez-Freire

 Adds a surface interaction to the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - surfacePosition
	  - Z-coordinate of the surface
	  - float
	  - 0.0
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - epsilon
	  - Energy parameter for surface-particle interaction
	  - float
	  - 1.0
.. list-table:: Optional Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Particles interacting with the surface
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "surface",
		"parameters":{
			"epsilon": 1.0,
			"surfacePosition": -10.0,
			"selection": "model1 all"
		}
	}



----

surfaceMaxForce
---------------

	:author: Pablo Ibáñez-Freire

 Implements a surface interaction with a maximum force constraint.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - maxForce
	  - Maximum force allowed in the interaction
	  - float
	  - 
	* - surfacePosition
	  - Z-coordinate of the surface
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
	* - epsilon
	  - Energy parameter for surface-particle interaction
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
	  - Particles interacting with the surface
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "surfaceMaxForce",
		"parameters":{
			"epsilon": 1.0,
			"surfacePosition": -10.0,
			"maxForce": 100.0,
			"selection": "model1 all"
		}
	}



----

uniformMagneticField
--------------------

	:author: P. Palacios-Alonso

 Applies a uniform magnetic field to selected magnetic particles in the simulation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - b0
	  - Magnitude of the magnetic field
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "uniformMagneticField",
		"parameters":{
			"b0": 1.0,
			"direction": [0, 0, 1]
		}
	}



