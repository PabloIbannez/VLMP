SurfaceUmbrellaSampling
=======================

Introduction
------------

The SurfaceUmbrellaSampling experiment in VLMP provides a framework for conducting umbrella sampling simulations 
to study the free energy profile of molecules interacting with surfaces. 

To determine the free energy of interaction between a sample and a surface, 
we can perform a technique known as umbrella sampling [Shirts2008]_ [Zhu2012]_ [Tan2012]_.
The procedure requires applying a series of harmonic potentials that restrict the position of the sample at different heights. 
Subsequently, by applying the WHAM algorithm, we can calculate the effective free energy potential [Shirts2008]_.
In VLMP, there is an experiment where we can indicate the sample, and it automatically makes copies of the sample, 
places them in the appropriate initial position, and adds the harmonic potential.

Setting Up the Experiment
-------------------------

To begin, import the necessary modules and define your experiment parameters:

.. code-block:: python

   from VLMP.experiments import SurfaceUmbrellaSampling

   parameters = {
       "umbrella": {
           "nWindows": 20,
           "windowsStartPosition": 10.0,
           "windowsEndPosition": 40.0,
           "K": [10.0, 20.0],
           "Ksteps": [10000, 90000],
           "measurementsIntervalStep": 100
       },
       "simulation": {
           "units": "KcalMol_A",
           "types": "basic",
           "temperature": 300.0,
           "box": [50.0, 50.0, 100.0],
           "models": [
               {"name": "molecule", "type": "SOP", "parameters": {"PDB": "molecule.pdb"}}
           ],
           "selection": "molecule all",
           "integrator": {
               "type": "BBK",
               "parameters": {
                   "timeStep": 0.002,
                   "frictionConstant": 2.0
               }
           }
       },
       "output": {
           "infoIntervalStep": 1000,
           "saveStateIntervalStep": 10000,
           "saveStateOutputFilePath": "state.pdb",
           "saveStateOutputFormat": "pdb"
       }
   }

This parameter dictionary configures all aspects of the umbrella sampling simulations, including:

1. Umbrella sampling settings: Number of windows, start and end positions, spring constants, and simulation steps.
   We can define different spring constants. The simulation runs a number of steps given by "Ksteps" for each spring constant.
   This is useful for systems where the initial conditions are far from the equilibrium position. Performing some steps
   with a lower spring constant can help the system to reach the equilibrium position. The measure interval step is the number
   of steps between measurements, this measurement is only performed for the last spring constant.
2. Simulation parameters: Units, temperature, box size, molecule model, and integrator settings. This is a regular simulation object.
3. Output configuration: Information and state saving intervals and formats. Using this parameters we can
   take a snapshot of the system at a given interval, for each window and indpendent file is created.


Running the Simulations
-----------------------

With the parameters defined, set up and run the simulations:

.. code-block:: python

   experiment = SurfaceUmbrellaSampling(parameters)
   experiment.generateSimulationPool()
   experiment.distributeSimulationPool("one")
   experiment.setUpSimulation("umbrella_session")

This process involves several steps:

1. Initialize the ``SurfaceUmbrellaSampling`` class with the parameters.
2. ``generateSimulationPool()`` creates a set of simulations, one for each umbrella sampling window.
3. ``distributeSimulationPool()`` organizes the simulation pool. The "one" method creates a separate simulation for each window.
4. ``setUpSimulation()`` prepares the simulation environment, creating directories and configuration files.

VLMP automatically sets up each window's simulation, including:

- Positioning the molecule at the correct window center
- Setting up the umbrella potential
- Configuring measurement and output steps

Once set up, run the simulations in local or HPC environments as explained in the :ref:`VLMP Execution` section.

Analyzing the Results
---------------------

After simulations are complete, use the built-in analysis tools:

.. code-block:: python

   analysis = AnalysisSurfaceUmbrellaSampling("umbrella_session/surfaceUmbrella.json")
   analysis.run()

The analysis process includes:

1. Loading simulation results for each umbrella window.
2. Computing histograms of molecule positions for each window.
3. Applying the Weighted Histogram Analysis Method (WHAM) to compute the potential of mean force (PMF).
4. Generating plots of the histograms and PMF.
5. Saving the processed data and plots.

The ``AnalysisSurfaceUmbrellaSampling`` class automates these steps, making it easy to obtain the free energy profile from your umbrella sampling simulations.

Customizing Your Experiment
---------------------------

The SurfaceUmbrellaSampling experiment is flexible and can be customized:

- **Window Parameters**: Adjust number of windows, range, and spring constants to suit your system.
- **Simulation Model**: Use different models for your molecule (e.g., SOP, SBCG, or custom models).
- **Integration Scheme**: Modify integrator type and parameters as needed.
- **Output and Analysis**: Configure measurement intervals and output formats to suit your needs.

Conclusion
----------

The SurfaceUmbrellaSampling experiment in VLMP provides a tool for studying molecule-surface interactions 
through free energy calculations. 

References
----------

.. [Shirts2008] Shirts, M. R., & Chodera, J. D. (2008). Statistically optimal analysis of samples from multiple equilibrium states. The Journal of Chemical Physics, 129(12), 124105. 

.. [Zhu2012] Zhu, F., & Hummer, G. (2012). Convergence and error estimation in free energy calculations using the weighted histogram analysis method. Journal of Computational Chemistry, 33(4), 453-465. 

.. [Tan2012] Tan, Z., Gallicchio, E., Lapelosa, M., & Levy, R. M. (2012). Theory of binless multi-state free energy estimation with applications to protein-ligand binding. The Journal of Chemical Physics, 136(14), 144102. 
