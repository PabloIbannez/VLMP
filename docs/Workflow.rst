Workflow
========

VLMP streamlines the process of large-scale molecular simulations through a Python interface.
The workflow comprises four primary stages:

1. **Simulation Configuration**:
   At this stage, parameters for a single molecular simulation are defined. These include the
   molecular model, ensemble type, integration scheme, and more. The configuration is typically
   defined using a Python dictionary.

2. **Simulation Pool Creation**:
   A simulation pool holds multiple configurations that are prepared for batch execution. This
   enables variations in systems, ensembles, or other parameters for comparative analyses.

3. **Simulation Distribution**:
   After creating the pool, the next step is to distribute the simulations across multiple
   computational resources. VLMP offers flexible distribution strategies, be it based on size,
   complexity, or custom criteria.

4. **Simulation Execution**:
   Finally, the simulations are executed. VLMP seamlessly integrates with UAMMD-structured to
   ensure efficient GPU-based execution.

The following sections delve into the specifics of each stage, demonstrating VLMP's capabilities.
