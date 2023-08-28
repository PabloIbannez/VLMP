import VLMP
import copy

from VLMP.utils.units import picosecond2KcalMol_A_time
ps2AKMA = picosecond2KcalMol_A_time()

from VLMP.experiments.HighThroughputAFM import HighThroughputAFM

samples = {
            "ccmv":[{
            "type":"FILE",
            "parameters":{"inputFilePath":"ccmv.json"},
            }],
            "encapsulin": [{
            "type":"FILE",
            "parameters":{"inputFilePath":"encapsulin.json"},
            }]
           }

parameters = {"AFM":{"K":0.05,
                     "Kxy":100.0,
                     "epsilon":1.0,
                     "tipVelocity":0.0/ps2AKMA,
                     "surfacePosition":0.0,
                     "thermalizationSteps":100000,
                     "indentationSteps":10000000,
                     "tipMass":1000.0,
                     "tipRadius":250.0,
                     "initialTipSampleDistance":50.0
                    },
              "surface":{"epsilon":-1.0},
              "simulation":{"units":"KcalMol_A",
                            "types":"basic",
                            "temperature":300.0,
                            "box":[2000.0, 2000.0, 4000.0],
                            "samples":copy.deepcopy(samples),
                            "integrator":{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,
                                                                     "frictionConstant":1.0}}},
              "output":{"infoIntervalStep":10000,
                        "saveStateIntervalStep":100000,
                        "saveStateOutputFilePath":"output",
                        "saveStateOutputFormat":"sp"}
              }

htafm = HighThroughputAFM(parameters)

htafm.generateSimulationPool()
htafm.distributeSimulationPool("none")
htafm.setUpSimulation("TEST")

