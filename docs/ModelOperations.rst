ModelOperations
===============

.. include:: ModelOperationsIntro.rst

- :ref:`alignInertiaMomentAlongVector`

- :ref:`distributeRandomly`

- :ref:`rotation`

- :ref:`setCenterOfMassPosition`

- :ref:`setContactDistance`

- :ref:`setParticleLowestPosition`

- :ref:`setParticlePositions`

- :ref:`setParticleXYPosition`



----

alignInertiaMomentAlongVector
-----------------------------

	:author: Pablo Ibáñez-Freire

 Aligns the largest inertia moment of selected particles along a specified vector.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - vector
	  - Vector along which to align the largest inertia moment.
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
	  - Selection of particles to align.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "alignInertiaMomentAlongVector",
		"parameters":{
			"vector": [0.0, 0.0, 1.0],
			"selection": "model1 chain A"
		}
	}



----

distributeRandomly
------------------

	:author: Pablo Ibáñez-Freire

 Distributes selected particles randomly within specified bounds.

.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - mode
	  - Distribution mode, either 'box' or 'sphere'.
	  - str
	  - box
	* - randomRotation
	  - Whether to apply random rotations to the particles.
	  - bool
	  - True
	* - avoidClashes
	  - Number of attempts to avoid particle clashes. If 0, clashes are not avoided.
	  - int
	  - 0
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to distribute.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "distributeRandomly",
		"parameters":{
			"mode": "sphere",
			"avoidClashes": 100,
			"randomRotation": True,
			"selection": "model1 all"
		}
	}



----

rotation
--------

	:author: Pablo Ibáñez-Freire

 Applies a rotation to selected particles around a specified axis.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - angle
	  - Angle of rotation in radians.
	  - float
	  - 
	* - axis
	  - Axis of rotation.
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
	  - Selection of particles to rotate.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "rotation",
		"parameters":{
			"axis": [0.0, 0.0, 1.0],
			"angle": 3.14159,
			"selection": "model1 resid 1 to 10"
		}
	}



----

setCenterOfMassPosition
-----------------------

	:author: Pablo Ibáñez-Freire

 Sets the center of mass of a selection of particles to a specified position.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - position
	  - Target position for the center of mass.
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
	  - Selection of particles to move.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "setCenterOfMassPosition",
		"parameters":{
			"position": [0.0, 0.0, 0.0],
			"selection": "model1 type A B C"
		}
	}



----

setContactDistance
------------------

	:author: Pablo Ibáñez-Freire

 Sets the contact distance between two selections of particles.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - distance
	  - Target contact distance between the selections.
	  - float
	  - 
	* - resolution
	  - Resolution for the contact distance adjustment.
	  - float
	  - 0.1
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - inverse
	  - Whether to invert the direction of the contact.
	  - bool
	  - False
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - reference
	  - Reference selection of particles.
	  - list of ids
	* - mobile
	  - Mobile selection of particles to be moved.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "setContactDistance",
		"parameters":{
			"distance": 5.0,
			"resolution": 0.01,
			"inverse": False,
			"reference": "model1 type A",
			"mobile": "model2 type B"
		}
	}



----

setParticleLowestPosition
-------------------------

	:author: Pablo Ibáñez-Freire

 Sets the lowest particle in the selection to a specified Z position.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - position
	  - Z coordinate to set for the lowest particle.
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
	* - radiusFactor
	  - Factor to multiply the radius by when considering it.
	  - float
	  - 1.0
	* - considerRadius
	  - Whether to consider particle radius when setting the position.
	  - bool
	  - False
.. list-table:: Required Selections
	:header-rows: 1
	:widths: 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	* - selection
	  - Selection of particles to consider.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "setParticleLowestPosition",
		"parameters":{
			"position": 0.0,
			"considerRadius": True,
			"radiusFactor": 1.1,
			"selection": "model1 all"
		}
	}



----

setParticlePositions
--------------------

	:author: Pablo Ibáñez-Freire

 Sets the positions of a group of particles to specified coordinates.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - ids
	  - List of particle IDs to move.
	  - list of int
	  - 
	* - positions
	  - List of new positions for the selected particles.
	  - list of list of float
	  - 

Example:

.. code-block:: python

	{
		"type": "setParticlePositions",
		"parameters":{
			"positions": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
			"ids": [0, 1]
		}
	}



----

setParticleXYPosition
---------------------

	:author: Pablo Ibáñez-Freire

 Sets the XY position of selected particles to a specified value.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - position
	  - New XY position for the particles.
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
	  - Selection of particles to move.
	  - list of ids

Example:

.. code-block:: python

	{
		"type": "setParticleXYPosition",
		"parameters":{
			"position": [1.0, 2.0],
			"selection": "model1 type A"
		}
	}



