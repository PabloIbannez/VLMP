Types
=====

.. include:: TypesIntro.rst

basic
-----

	:author: Pablo Ibáñez-Freire

Component for defining basic types in a simulation. It includes components for mass, radius, and charge, which are essential attributes for many simulation scenarios. These properties define the physical characteristics of the particles used in the simulation. When a new type is created, if no value is given for any of these properties, the default value is used.

.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - charge
	  - Default charge for a new type
	  - float
	  - 0.0
	* - mass
	  - Default mass for a new type
	  - float
	  - 1.0
	* - radius
	  - Default radius for a new type
	  - float
	  - 1.0

Example:

.. code-block:: python

	{
		"type": "basic"
	}



none
----

	:author: Pablo Ibáñez-Freire

Component representing a 'none' type in a simulation. Essentially, it signifies that no additional components or special characteristics are associated with the entity. This can be useful in simulations where certain entities need to be defined but do not require specific attributes or behaviors.


Example:

.. code-block:: python

	{
		"type": "none"
	}



