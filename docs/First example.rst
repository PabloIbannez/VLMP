First example
=============

This section provides a simple example to illustrate how to use VLMP. 
The example demonstrates how to simulate a set of DNA chains using the MADna model. 
We begin by setting various simulation parameters such as the number of sequences, sequence length, and others. 
The script then generates random DNA sequences and populates the simulation pool with the necessary configuration. 
Finally, VLMP is initialized, and the simulation pool is loaded and distributed.

.. code-block:: python

   import VLMP
   from VLMP.utils.units import picosecond2KcalMol_A_time
   from numpy import random

   # Convert picoseconds to AKMA time unit
   ps2AKMA = picosecond2KcalMol_A_time()

   # Number of sequences and sequence set size
   Nsequence = 10
   sequenceSetSize = 10

   # Length of each sequence and the basis of DNA
   sequenceLength  = 100
   basis = ['A', 'C', 'G', 'T']

   # Generate random sequences
   sequences = []
   for i in range(Nsequence):
       sequences.append(''.join(random.choice(basis, sequenceLength)))

   # Populate simulation pool
   simulationPool = []
   for seq in sequences:
       # Configure simulation parameters
       simulationPool.append({
           "system": [
               {"type": "simulationName", "parameters": {"simulationName": seq}},
               {"type": "backup", "parameters": {"backupIntervalStep": 100000}}
           ],
           "units": [{"type": "KcalMol_A"}],
           "types": [{"type": "basic"}],
           "ensemble": [
               {"type": "NVT", "parameters": {"box": [2000.0, 2000.0, 2000.0], 
                                              "temperature": 300.0}}
           ],
           "integrators": [
               {"type": "BBK", "parameters": {"timeStep": 0.02*ps2AKMA, 
                                              "frictionConstant": 0.2/ps2AKMA, 
                                              "integrationSteps": 1000000}}
           ],
           "models": [
               {"type": "MADna", "parameters": {"sequence": seq}}
           ],
           "simulationSteps": [
               {"type": "saveState", "parameters": {"intervalStep": 10000, 
                                                    "outputFilePath": "traj", 
                                                    "outputFormat": "dcd"}},
               {"type": "thermodynamicMeasurement", "parameters": {"intervalStep": 10000, 
                                                                   "outputFilePath": "thermo.dat"}},
               {"type": "info", "parameters": {"intervalStep": 10000}}
           ]
       })

   # Initialize VLMP and load simulation pool
   vlmp = VLMP.VLMP()
   vlmp.loadSimulationPool(simulationPool)

   # Distribute simulations and set up
   vlmp.distributeSimulationPool("size", sequenceSetSize)
   vlmp.setUpSimulation("FIRST_EXAMPLE")

**Executing Simulations**

To execute the simulations, use the following terminal command:

.. code-block:: bash

   python -m VLMP -s VLMPsession.json --local --gpu 0 1

Run this command in the directory "FIRST_EXAMPLE," which is created by the preceding code. 
The `--local` flag indicates that the simulations will run on the current machine. 
However, VLMP provides the option to run simulations on other machines like a HPC cluster.
The `--gpu 0 1` option specifies that GPUs 0 and 1 will be used for the simulations.
