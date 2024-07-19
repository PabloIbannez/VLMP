Installation
============

**Prerequisites**

VLMP can generate the simulations input without the need for any external dependencies. However,
if you want to run the simulations, you will need to install UAMMD-structured, which will handle the execution
of simulations. You can find the installation instructions for UAMMD-structured in its official
documentation:

`UAMMD-structured Documentation <https://uammd-structured.readthedocs.io/en/latest/>`_

**Installing VLMP**

There are multiple ways to install VLMP. The easiest method is
through Python's package manager, pip:

.. code-block:: bash

   pip install pyVLMP

Alternatively, you can clone the repository directly from GitHub:

`VLMP GitHub Repository <https://github.com/PabloIbannez/VLMP>`_

After cloning, navigate to the repository directory and run:

.. code-block:: bash

   pip install .

This will install all the additional required packages.

**Verifying Installation**

To verify that the installation was successful, import the VLMP library in a Python interpreter:

.. code-block:: python

   import VLMP

This will trigger VLMP to perform an internal check. Note that if some modules fail to load due
to missing specific libraries, error messages will be displayed. These errors won't generally
impact VLMP's overall functionality; only the unavailable components will be affected.
