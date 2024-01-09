import VLMP
from VLMP.utils.units import picosecond2KcalMol_A_time

from numpy import random

ps2AKMA = picosecond2KcalMol_A_time()

sequences = {
    "test":"MPKRKAEGDAKGDKAKVKDEPQRRSARLSAKPAPPKPEPKPKKAPAKKGEKVPKGKKGKADAGKEGNNPAENGDAKTDQAQKAEGAGDAK"
}

concentration = 0.001

simulationPool = []
for seq in sequences:
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":seq}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVTlambda","parameters":{"box":[200.0,200.0,400.0],"temperature":300.0,"lambda":0.0}}],
                           "integrators":[{"type":"NVE","parameters":{"timeStep":0.005*ps2AKMA,"integrationSteps":10000000}}],
                           "models":[{"type":"PROTEIN_IDP_PROTEIN",
                                      "parameters":{
                                                    "PDB2":"1ema.pdb",
                                                    "PDB2_conn":"start",
                                                    "sequence":sequences[seq],
                                                    "cutOffVerletFactor":1.1,
                                                    }
                                      },
                                     #{"type":"STERIC_LAMBDA_SOLVATION",
                                     # "parameters":{"concentration":concentration,
                                     #               "addVerletList":False,
                                     #               "condition":"noGroup",
                                     #               "particleName":"W",
                                     #               "particleMass":100.0,
                                     #               "particleRadius":3.8,
                                     #               "particleCharge":0.0,
                                     #               "padding":[[0.0,0.0,0.0],[0.0,0.0,-5.0]]},
                                     #},
                                     ],
                           "modelOperations":[{"type":"setParticleLowestPosition",
                                               "parameters":{"position":-200.0,"considerRadius":True,"radiusFactor":1.1,
                                                             "selection":{"models":["PROTEIN_IDP_PROTEIN"]}}
                                               }],
                           "modelExtensions":[{"type":"WCA",
                                               "parameters":{"addVerletList":False}
                                              },
                                              {"type":"constraintParticlesPosition",
                                               "parameters":{"K":100.0,
                                                             "selection":{"expression":{"particleId":[0]}}}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                "pbc":True,
                                                                                "outputFilePath":"output",
                                                                                "outputFormat":"sp"}},
                                              #{"type":"lambdaCycle","parameters":{"intervalStep":1,
                                              #                                    "activationStep":10000,
                                              #                                    "measureStep":100000,
                                              #                                    "pauseStep":100000,
                                              #                                    "lambdaValues":[0.0,0.0001,0.001,0.01,0.1,0.2,0.5,0.8,1.0]}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("PROT_IDP_SURF_TEST")

