import VLMP

from VLMP.utils.units import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1
icoPerSet = 25

simulationPool = []
for i in range(copies):

    models = []
    for m in range(icoPerSet):
        models.append({"name":f"part_{m}",
                       "type":"ICOSPHERE",
                       #"type":"PARTICLE",
                       "parameters":{"particleName":"A",
                                     "particleRadius":5.0,
                                     "particleMass":1.0,
                                     "Kb":100.0,
                                     "radius":5.0
                                     }})

    models.append({"type":"WLC",
                   "parameters":{"typeName":"B","N":100,"b":10.0,"Kb":10.0,"Ka":5.0,"stericInteraction":True}})

    interactionMatrix = []
    interactionMatrix.append(["A","A",1.0,10.0])
    interactionMatrix.append(["A","B",1.0,10.0])
    interactionMatrix.append(["B","B",1.0,10.0])

    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.0002*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":10000000}}],
                           "models":models.copy(),
                           "modelExtensions":[{"type":"interLennardJones","parameters":{"cutOffFactor":2.5,
                                                                                        "interactionMatrix":interactionMatrix.copy(),
                                                                                        "addVerletList":False}},
                                              {"type":"sphericalShell",
                                               "parameters":{
                                                             "shellRadius":"auto",
                                                             "shellCenter":[0,0,0],
                                                             "minShellRadius":50.0,
                                                             "radiusVelocity":-0.5,
                                                             "selection":{}
                                                            }}
                                              ],
                           "modelOperations":[{"type":"distributeRandomly","parameters":{
                                                                                         "mode":{"sphere":{"radius":100.0,
                                                                                                           "center":[10.0,0.0,0.0]}},
                                                                                         #"mode":{"box":{}},
                                                                                         "avoidClashes":10000,
                                                                                         "randomRotation":True,
                                                                                         "selection":{}}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("size",1)
vlmp.setUpSimulation("TEST")

