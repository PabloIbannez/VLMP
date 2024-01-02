import VLMP

from VLMP.utils.utils import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.01*ps2AKMA,"frictionConstant":1.0/ps2AKMA,"integrationSteps":2000000}}],
                           "models":[{"name":"sample",
                                      "type":"FILE",
                                      "parameters":{"inputFilePath":"tmv_SOP.json"}},
                                     #{"name":"tip",
                                     # "type":"PARTICLE",
                                     # "parameters":{"particleName":"TIP",
                                     #               "particleRadius":250.0,
                                     #               "particleMass":1.0,
                                     #               "position":[0.0,0.0,500.0]}}
                                     ],
                           "modelOperations":[{"type":"alignInertiaMomentAlongVector","parameters":{"vector":[1.0,0.0,0.0],
                                                                                                    "selection":{"models":"sample"}}
                                                                                                    },
                                              {"type":"setParticleLowestPosition","parameters":{"position":0.0,
                                                                                                "considerRadius":True,
                                                                                                "selection":{"models":"sample"}}}
                                              ],
                           #"modelExtensions":[{"type":"surface","parameters":{"epsilon":-2.0,"surfacePosition":0.0}},
                           #                   {"type":"AFM",
                           #                           "parameters":{"epsilon":100.0,
                           #                                         "K":0.1,
                           #                                         "Kxy":10.0,
                           #                                         "tipVelocity":-0.01,
                           #                                         "startChipPosition":[0.0,0.0,500.0],
                           #                                         "surfacePosition":0.0,
                           #                                         "tip":{"models":["tip"]},
                           #                                         "sample":{"models":["sample"]}}
                           #                    }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

