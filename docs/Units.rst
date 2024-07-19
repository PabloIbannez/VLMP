Units
=====

.. include:: UnitsIntro.rst

KcalMol_A
---------

	:author: Pablo Ibáñez-Freire

Component for defining the unit system of (Kcal/mol)/A in a simulation. This unit component, part of the 'units' category, specifies the system's energy and distance units as kilocalories per mole and Angstroms, respectively. It includes fundamental constants relevant to this unit system, such as the Boltzmann constant (KBOLTZ) and the electrostatics coefficient (ELECOEF).


Example:

.. code-block:: python

	{
		"type": "KcalMol_A"
	}



none
----

	:author: Pablo Ibáñez-Freire

Component for defining a 'none' unit system in a simulation. This units component is used when no specific unit conversions are required. It sets all constants, such as the Boltzmann constant (KBOLTZ) and the electrostatic coefficient (ELECOEF), to a value of 1. This can be particularly useful in simulations where unitless or normalized values are preferred, or where specific unit conversions are handled externally.


Example:

.. code-block:: python

	{
		"type": "none"
	}



