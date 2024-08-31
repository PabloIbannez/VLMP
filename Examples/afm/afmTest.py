import VLMP
import copy

from VLMP.utils.units import picosecond2KcalMol_A_time, nanonewton2KcalMol_A_force
ps2AKMA = picosecond2KcalMol_A_time(1.0)

from VLMP.experiments.HighThroughputAFM import HighThroughputAFM

samples = {
            #"encapsulin": {"models":[{"type":"FILE",
            #                          "parameters":{"inputFilePath":"encapsulin.json"}}]},
            #"ccmv":{"models":[{"type":"FILE",
            #                          "parameters":{"inputFilePath":"ccmv.json"}}]},
            "tmv":{"models":[{"type":"FILE",
                              "parameters":{"inputFilePath":"tmv.json"}}],
                   "modelOperations":[{"type":"rotation",
                                       "parameters":{"axis":[1.0,0.0,0.0],
                                                     "angle":3.141592/2.0,
                                                     "selection":"FILE"}}]
                   }
           }

parameters = {
              "simulation":{"units":"KcalMol_A",
                            "types":"basic",
                            "temperature":300.0,
                            "box":[2000.0, 2000.0, 2000.0],
                            "samples":copy.deepcopy(samples),
                            "integrator":{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,
                                                                     "frictionConstant":1.0}}},
              "AFM":{"K":0.05,
                     "Kxy":100.0,
                     "epsilon":1.0,
                     "sigma":1.0,
                     "tipVelocity":[0.0],
                     "thermalizationSteps":100000000,
                     "indentationSteps":10000000,
                     "tipMass":1000.0,
                     "tipRadius":250.0,
                     "initialTipSampleDistance":10.0,
                     "indentationPositionX":0.0,
                     "indentationPositionY":0.0},
              "indentation": {
                  "thermalizationSteps": 10000,
                  "indentationSteps": 50000,
                  "fixSampleDuringThermalization": True,
                  "KxyFixing": 10.0},
              "surface":{"epsilon":-1.0,
                         "absorptionHeight":10.0,
                         "absorptionK":10.0},
              "maxForce":{"force":nanonewton2KcalMol_A_force(5.0),
                          "maxForceIntervalStep":1000},
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
