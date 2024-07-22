HighThroughputAFM
=================

Introduction
------------

The HighThroughputAFM experiment in VLMP provides a framework for conducting multiple Atomic Force Microscopy (AFM) simulations in parallel. 

We can indicate the parameters of the sample, and the rest of the AFM elements 
(as well as the simulation steps used for the measurements) are added. 
Many of the parameters can be indicated not with a single value but as a list. 
Each element of the list creates an additional simulation that can be executed in parallel, 
thus allowing us to easily construct AFM simulations with different samples in parallel.

Setting Up the Experiment
-------------------------

To begin, import the necessary modules and define your experiment parameters:

.. code-block:: python

   from VLMP.experiments import HighThroughputAFM

   parameters = {
       "AFM": {
           "K": 1.0,
           "Kxy": 0.5,
           "epsilon": 1.0,
           "sigma": 1.0,
           "tipVelocity": 0.1,
           "tipMass": 100.0,
           "tipRadius": 5.0,
           "initialTipSampleDistance": 10.0,
           "indentationPositionX": 0.0,
           "indentationPositionY": 0.0
       },
       "indentation": {
           "thermalizationSteps": 10000,
           "indentationSteps": 50000,
           "fixSampleDuringThermalization": True,
           "KxyFixing": 10.0
       },
       "surface": {
           "epsilon": 1.0,
           "position": -50.0
       },
       "simulation": {
           "units": "KcalMol_A",
           "types": "basic",
           "temperature": 300.0,
           "box": [100.0, 100.0, 100.0],
           "integrator": {
               "type": "BBK",
               "parameters": {
                   "timeStep": 0.002,
                   "frictionConstant": 2.0
               }
           },
           "samples": {
               "sample1": {
                   "models": [
                       {"type": "SOP", "parameters": {"PDB": "sample1.pdb"}}
                   ]
               },
               "sample2": {
                   "models": [
                       {"type": "SOP", "parameters": {"PDB": "sample2.pdb"}}
                   ]
               }
           }
       },
       "output": {
           "infoIntervalStep": 1000,
           "afmMeasurementIntervalStep": 100,
           "afmMeasurementOutputFilePath": "afm.dat"
       }
   }

This parameter dictionary configures all aspects of the AFM simulations, including:

1. AFM settings: Tip properties, force constants, and interaction parameters.
   The diffrent parameters can be indicated as a list, creating multiple simulations.
2. Indentation process: Thermalization and indentation steps.
3. Surface properties: Optional surface interaction.
4. Simulation parameters: Units, temperature, box size, and integrator settings.
   The `samples` section defines the samples to simulate, each with its own model.
   Each entry in the `samples` dictionary creates a separate simulation.
5. Output configuration: Measurement intervals and file paths.

.. tip::

    We can define parallel simulation in both sections `AFM` and `simulation`. In this case,
    the number of simulations will be the product of the number of simulations in each section.

Running the Simulations
-----------------------

With the parameters defined, you can now set up and run the simulations:

.. code-block:: python

   experiment = HighThroughputAFM(parameters)
   experiment.generateSimulationPool()
   experiment.distributeSimulationPool("one")
   experiment.setUpSimulation("afm_session")

This process involves several steps:

1. The `HighThroughputAFM` class is initialized with the parameters.
2. `generateSimulationPool()` creates a set of simulations, one for each sample.
   It automatically sets up the AFM tip, sample positioning, and all necessary interactions.
3. `distributeSimulationPool()` splits the simulation pool into smaller groups.
   In this example, we use the "one" distribution method, which would create a single simulation for each sample.
4. `setUpSimulation()` prepares the simulation environment, creating directories and configuration files.

Behind the scenes, VLMP is creating a complex simulation setup for each sample, including:

- Positioning the sample and AFM tip
- Setting up the AFM interaction potential
- Configuring the surface interaction (if enabled)
- Adding measurement and output steps

Once the simulations are set up, you can run the simulations both in local or in HPC environments.
The process to run the simulations and the different options is explained in the section :ref:`VLMP Execution`.

Analyzing the Results
---------------------

After the simulations are complete, you can use the built-in analysis tools:

.. code-block:: python

   analysis = AnalysisAFM("afm_session/VLMPsession.json", outputUnits="nN_nm")
   analysis.run()

The analysis process includes:

1. Loading simulation results for each sample.
2. Converting units (if necessary).
3. Generating force-distance curves.
4. Plotting the results and saving processed data.

The `AnalysisAFM` class automates these steps, making it easy to visualize and compare results across multiple samples or parameter sets.

Customizing Your Experiment
---------------------------

The HighThroughputAFM experiment is highly flexible. You can customize various aspects:

- **Multiple Samples**: Add more entries to the `samples` dictionary to simulate different systems in parallel.
- **AFM Parameters**: Adjust tip properties, force constants, or interaction parameters in the `AFM` section.
- **Indentation Process**: Modify thermalization and indentation steps, or change sample fixing options.
- **Surface Interaction**: Enable or disable the surface, and adjust its properties.
- **Output and Analysis**: Configure measurement intervals and output formats to suit your needs.

Advanced Usage
--------------

For more complex scenarios, you can:

- Use different models for your samples (e.g., SOP, SBCG, or custom models).
- Implement custom analysis routines by extending the `AnalysisAFM` class.
- Integrate with other VLMP components for more sophisticated simulations.

Conclusion
----------

The HighThroughputAFM experiment in VLMP provides a tool for conducting AFM simulations efficiently. 
By automating the setup of complex AFM components and providing built-in analysis tools, 
it allows researchers to focus on the scientific questions rather than simulation technicalities. 
Whether you're studying single particles, complex biomolecules, or material surfaces, 
this experiment can be adapted to suit a wide range of AFM simulation needs.
