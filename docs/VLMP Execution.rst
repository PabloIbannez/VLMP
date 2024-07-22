VLMP Execution
==============

Once we have generated all the files required to carry out the simulations, 
the last step is to actually execute the simulation. 
VLMP provides two execution options: a local option for personal computers, and another for HPC clusters, 
particularly those using Slurm as a manager. The process for both is similar, but the parameters vary.

In both cases, we execute the VLMP module through Python using the command:

.. code-block:: bash

   python -m VLMP --session VLMPsession.json

Note that the session file can have a different name and can be specified using its path. 
The rest of the options specify the type of simulation to execute and how it will be carried out. 
After execution, results can be inspected in their respective folders.

Local Execution
---------------

For local execution, simulations can use visible GPUs. To run in local mode, add the ``--local`` 
parameter and specify the GPUs to use with the ``--gpu`` parameter. For example:

.. code-block:: bash

   python -m VLMP --session VLMPsession.json --local --gpu 0 1

The ``--gpu`` argument is required for local execution and accepts a list of GPU IDs to use for the simulation.

In this mode, VLMP distributes the different simulationSets among the specified GPUs. 
VLMP's job queue manager executes all simulationSets, running them sequentially on each GPU. 
The queue manager initiates remaining simulations when a GPU becomes available.

HPC Cluster
-----------

VLMP supports execution in HPC environments, particularly using the Slurm queue manager. 
To use this mode, add the ``--slurm`` option:

.. code-block:: bash

   python -m VLMP --session VLMPsession.json --slurm --partition gpu --modules gcc/8.4 cuda/10.2

This option adds the simulations to the Slurm queue manager. When executed in this mode, you can specify various options:

- ``--node``: A list of node IDs to use (optional)
- ``--partition``: A list of Slurm partitions to use (required)
- ``--filling``: A list of integers representing the number of simulations per node (optional, only used with ``--node``)
- ``--modules``: A list of modules to load before running the simulation (optional)
- ``--postScript``: A script to run after the simulation completes (optional)

For example, a more complex Slurm execution might look like:

.. code-block:: bash

   python -m VLMP --session VLMPsession.json --slurm --partition gpu --node node001 node002 --filling 2 3 --modules gcc/8.4 cuda/10.2 --postScript cleanup.sh

This command would submit the simulation to the Slurm queue, requesting the 'gpu' partition, 
using nodes 'node001' and 'node002', running 2 simulations on the first node and 3 on the second, 
loading the gcc/8.4 and cuda/10.2 modules, and running cleanup.sh after the simulation completes.
