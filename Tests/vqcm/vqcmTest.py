import VLMP

copies = 1

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "globals":[{"type":"NVT","parameters":{"box":[16.0,16.0,16.0],"temperature":1.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.01,"frictionConstant":1.0,"integrationSteps":1}}],
                           "models":[{"name":"part1",
                                      "type":"PARTICLE",
                                      "parameters":{"particleName":"A",
                                                    "particleRadius":1.0,
                                                    "particleMass":1.0,
                                                    "position":[0.0,0.0,6.0]}},
                                     {"name":"part2",
                                      "type":"PARTICLE",
                                      "parameters":{"particleName":"A",
                                                    "particleRadius":1.0,
                                                    "particleMass":1.0,
                                                    "position":[6.0,0.0,6.0]}}

                                     ],
                           "modelExtensions":[{"type":"addBond",
                                                      "parameters":{"K":0.05,
                                                                    "r0":6.0,
                                                                    "selection1":{"models":["part1"]},
                                                                    "selection2":{"models":["part2"]}}
                                               }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"VQCM","parameters":{"intervalStep":1,
                                                                           "outputFilePath":"vqcm.dat",
                                                                           "tolerance":1.0e-6,
                                                                           "omega":1.0,
                                                                           "hydrodynamicRadius":1.0,
                                                                           "viscosity":2.0,
                                                                           "fluidMass":0.75,
                                                                           "vwall":[10.0,0.0],
                                                                           "nIterations":30,
                                                                           "gamma":0.5}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP("dev")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

