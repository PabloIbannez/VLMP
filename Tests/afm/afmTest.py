import VLMP
import copy

from VLMP.utils.units import picosecond2KcalMol_A_time, nanonewton2KcalMol_A_force
ps2AKMA = picosecond2KcalMol_A_time(1.0)

from VLMP.experiments.HighThroughputAFM import HighThroughputAFM

samples = {
            "encapsulin": [{
            "type":"FILE",
            "parameters":{"inputFilePath":"encapsulin.json"},
            }],
            "ccmv":[{
            "type":"FILE",
            "parameters":{"inputFilePath":"ccmv.json"},
            }]
           }

#samples = {"none1":[],
#           "none2":[],
#           "none3":[],
#           "none4":[]}

parameters = {"AFM":{"K":0.05,
                     "Kxy":100.0,
                     "epsilon":1.0,
                     "tipVelocity":-0.1/ps2AKMA,
                     "thermalizationSteps":10000,
                     "indentationSteps":10000000,
                     "tipMass":1000.0,
                     "tipRadius":250.0,
                     "initialTipSampleDistance":20.0,
                     "maxForce":nanonewton2KcalMol_A_force(4.0),
                     "maxForceIntervalStep":1000
                    },
              #"surface":{"epsilon":-1.0,
              #           "absorptionHeight":10.0,
              #           "absorptionK":10.0},
              "surface":{"epsilon":1.0},
              "simulation":{"units":"KcalMol_A",
                            "types":"basic",
                            "temperature":300.0,
                            "box":[2000.0, 2000.0, 2000.0],
                            "samples":copy.deepcopy(samples),
                            "integrator":{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,
                                                                     "frictionConstant":1.0}}},
              "output":{"infoIntervalStep":10000,
                        "saveStateIntervalStep":10000,
                        "afmMeasurementIntervalStep":1000,
                        "saveStateOutputFilePath":"output",
                        "saveStateOutputFormat":"sp"}
              }

htafm = HighThroughputAFM(parameters)

htafm.generateSimulationPool()
htafm.distributeSimulationPool("none")
htafm.setUpSimulation("TEST")
