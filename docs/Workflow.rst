Workflow
========

In this section, we list all the different steps we have to follow to run a set of simulations in VLMP. 
As previously mentioned, the process consists of four stages, which we will now describe in greater depth. 
These stages, from the building of simulations to their execution, are:

1. **Simulation Pool Creation**: Initially, we create the simulation pool. 
   This involves constructing various simulations using chosen components. 
   Upon completion, we have a list of dictionaries, where each dictionary represents a simulation. 
   Each dictionary contains entries for categories and a list of components used for each category.

2. **Simulation Pool Distribution**: After filling the simulation pool, we proceed to distribute it. 
   The distribution process transforms the simulation pool from a list into a list of lists, 
   with each sublist being a set of simulations (similar to a simulation pool). 
   This distribution process can be repeated multiple times, and the result is always a list of lists of simulations. 
   Each sublist is known as a simulation set and is the unit executed on each GPU.

3. **Files Generation**: With the different simulation sets prepared, 
   we generate all necessary files and directories for the simulation. A folder with the session name (provided by the user) is created, containing the "VLMPsession.json" file. This file encapsulates all session information, necessary for executing the simulations and reconstructing all simulation files. Additionally, two subfolders are created within the main simulation folder: "simulationSets" for execution and "results" for examining the simulation post-completion. The "results" folder contains a separate folder for each simulation with all the output of the simulation upon completion.

4. **Execution**: VLMP can execute simulations locally (on the current computer) or in an HPC environment with various compute nodes. 
   For execution, VLMP is used as an executable. 
   This executable takes "VLMPsession.json" and parameters selecting and configuring the execution environment (local or HPC) 
   as arguments.

.. code-block:: python

    import VLMP
    ...
    
    simulationPool = []
    # Populate simualtion pool
    for ...
        simulationPool.append(
            {"system":[...],
             "units":[...],
             "types":[...],
             "ensemble":[...],
             "integrators":[...],
             "models":[...],
             "modelExtensions":[...],
             "simulationSteps":[...]}
        )
    ...
    
    vlmp = VLMP.VLMP()
    
    vlmp.loadSimulationPool(simulationPool)
    vlmp.distributeSimulationPool(...)
    vlmp.setUpSimulation("SESSION_NAME")


In the following sections we will discuss in more detail the different aspects of each of these processes. 
First, we will discuss the components available to form a simulation. 
Subsequently we will see how to distribute the simulation pool and how to create the different addresses and files. 
Finally we will discuss the different methods for running the simulations.
