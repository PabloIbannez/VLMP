import VLMP

import json
import jsbeautifier

L=100
Kb=100.0

Ka=[10.0,20.0,30.0,40.0,50.0,60.0]

simulationPool = []
for ka in Ka:
    simulationPool.append(
    {"system":[{"type":"simulationName",
                "parameters":{"simulationName":"wlc_Ka_"+str(ka)}},
               {"type":"backup","parameters":{"backupIntervalStep":10000}}],
     "units":[{"type":"none"}],
     "types":[{"type":"basic"}],
     "ensemble":[{"type":"NVT",
                  "parameters":{"box":[200.0,200.0,200.0],
                                "temperature":1.0}}],
     "integrators":[{"type":"BBK",
                     "parameters":{"timeStep":0.001,
                                   "frictionConstant":1.0,
                                   "integrationSteps":1000000}}],
     "models":[{"type":"WLC",
                "parameters":{"N":L,"b":1.0,"Kb":Kb,"Ka":ka}}],
     "modelExtensions":[{"type":"constantForceBetweenCentersOfMass",
                         "parameters":{"force":1.0,
                                       "selection1":"WLC polymerIndex  1",
                                       "selection2":"WLC polymerIndex -1"}
                         }],
     "simulationSteps":[{"type":"saveState",
                         "parameters":{"intervalStep":10000,
                                       "outputFilePath":"output",
                                       "outputFormat":"sp"}},
                        {"type":"anglesMeasurement",
                         "parameters":{"intervalStep":1000,
                                       "outputFilePath":"angles.dat",
                                       "selection":"WLC forceField angles_wlc"}},
                        {"type":"info","parameters":{"intervalStep":10000}}]

    }
)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("size",2)
vlmp.setUpSimulation("TEST")

