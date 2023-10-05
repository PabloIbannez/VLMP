Simulation
==========

Setting up a simulation in VLMP is akin to assembling a puzzle. Each section
is like a different type of puzzle piece, and when properly arranged in the
right order, these pieces form the complete picture of your simulation.

It's essential to understand that sections are evaluated in sequence, adding
their respective components to the simulation in the order specified. Both the
sections and their internal components follow this ordered addition to the
simulation pipeline.

1. **System**
   The System section is the cornerstone, laying the foundation with high-level
   settings like the simulation name or backup intervals.

2. **Units**
   The Units section sets the unit system, ensuring uniformity in results.

3. **Types**
   The Types section specifies if the simulation is atomic, coarse-grained, or
   otherwise, setting the flavor of the puzzle.

4. **Ensemble**
   In the Ensemble section, state variables like temperature and pressure are
   determined, shaping the thermodynamic landscape.

5. **Models**
   The Models section defines the molecular or particle components, bringing
   characters into the puzzle's narrative.

6. **Model Operations**
   This section manipulates these characters, rotating particles or setting the
   center of mass.

7. **Model Extensions**
   Additional attributes like forces or torques are added here, enriching the
   existing models.

8. **Integrators**
   The Integrators section dictates how the system evolves, setting the rules
   of time progression.

9. **Simulation Steps**
   Finally, the Simulation Steps section specifies tasks to be performed at
   regular intervals, completing the puzzle. The components added in this
   section can be used to monitor the simulation, output data, or perform
   analysis.

Not all sections are mandatory. Specifically, the Model Operations, Model
Extensions, and Simulation Steps sections are optional.
