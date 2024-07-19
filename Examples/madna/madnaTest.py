import VLMP
from VLMP.utils.units import picosecond2KcalMol_A_time

from numpy import random

ps2AKMA = picosecond2KcalMol_A_time()

Nsequence = 1
sequenceLength = 100

basis = ['A', 'C', 'G', 'T']

sequences = []
for i in range(Nsequence):
    sequences.append(''.join(random.choice(basis, sequenceLength)))

simulationPool = []
for seq in sequences:
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":seq}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[200.0,200.0,200.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":1000000}}],
                           "models":[{"name":"dna1",
                                      "type":"MADna",
                                      "parameters":{"sequence":seq,
                                                    "variant":{"fast":{}}},
                                      },
                                     {"name":"dna2",
                                      "type":"MADna",
                                      "parameters":{"sequence":seq,
                                                    "variant":{"fast":{}}},
                                      }
                                     ],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "pbc":False,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp",
                                                                                "selection":"dna1 res 2"}},
                                              {"type":"thermodynamicMeasurement","parameters":{"intervalStep":10000,
                                                                                 "outputFilePath":"thermo.dat"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

