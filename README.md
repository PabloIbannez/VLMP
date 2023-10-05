# VLMP (Virtual Laboratory Massively Parallelized)

<p align="center">
    <img src="https://github.com/PabloIbannez/VLMP/blob/main/docs/_images/logo.png" width="250">  
</p>

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Workflow](#workflow)
- [License](#license)
- [Contact](#contact)

## Introduction

VLMP is a Python library designed for running parallelized simulations, specifically optimized for molecular dynamics and other continuous models. Built on the backend technology of UAMMD-structured, it leverages multi-level parallelization to achieve highly efficient simulation runs.

### Features

- **Multi-level Parallelization**: Run multiple simulations concurrently on a single GPU or distribute across multiple GPUs.
- **Optimized for Coarse-grained Models**: Achieve better GPU utilization with small-scale simulations.
- **Highly Configurable**: Easily adaptable for a variety of scientific phenomena.
- **Community Sharing**: Distribute new models as VLMP modules.

## Documentation

Coming soon.

## Installation

### Prerequisites

Install UAMMD-structured before proceeding. [UAMMD-structured Documentation](https://uammd-structured.readthedocs.io/en/latest/)

### Installing VLMP

Via pip:
```bash
pip install pyVLMP
```

Or clone the GitHub repository:

```bash
git clone https://github.com/PabloIbannez/VLMP.git
cd VLMP
pip install .
```

### Verifying Installation

```python
import VLMP
```

## Getting Started

Here's a minimal example to simulate a set of DNA chains:

```python

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
   vlmp.setUpSimulation("EXAMPLE")
```

Execute the simulations with:

```bash
cd EXAMPLE
python -m VLMP -s VLMPsession.json --local --gpu 0 1
```

## Workflow

1. **Simulation Configuration**: Define simulation parameters.
2. **Simulation Pool Creation**: Prepare multiple configurations for batch execution.
3. **Simulation Distribution**: Distribute simulations across computational resources.
4. **Simulation Execution**: Execute simulations on GPU using UAMMD-structured.

## License

[GPLv3](./LICENSE.txt)

## Contact

For issues and contributions, please contact: [GitHub Issues](https://github.com/PabloIbannez/VLMP/issues)

