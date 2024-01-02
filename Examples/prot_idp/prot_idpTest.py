import VLMP
from VLMP.utils.units import picosecond2KcalMol_A_time

from numpy import random

ps2AKMA = picosecond2KcalMol_A_time()

sequences = {
    "test":"MPKRKAEGDAKGDKAKVKDEPQRRSARLSAKPAPPKPEPKPKKAPAKKGEKVPKGKKGKADAGKEGNNPAENGDAKTDQAQKAEGAGDAK"
}

simulationPool = []
for seq in sequences:
    #for conn1 in ["start","end"]:
    #    for conn2 in ["start","end"]:
    for conn1 in ["start"]:
        for conn2 in ["start"]:
            simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":seq+"_pdb1_"+conn1+"_pdb2_"+conn2}},
                                             {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                                   "units":[{"type":"KcalMol_A"}],
                                   "types":[{"type":"basic"}],
                                   "ensemble":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                                   "integrators":[{"type":"BBK","parameters":{"timeStep":0.01*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":10000000}}],
                                   "models":[{"type":"PROTEIN_IDP_PROTEIN",
                                              "parameters":{
                                                            "PDB1":"1ema.pdb",
                                                            "PDB1_conn":conn1,
                                                            "PDB2":"1ema.pdb",
                                                            "PDB2_conn":conn2,
                                                            "sequence":sequences[seq]}
                                              }],
                                   "modelExtensions":[{"type":"interWCA",
                                                       "parameters":{"addVerletList":False}
                                                      }],
                                   "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                        "pbc":False,
                                                                                        "outputFilePath":"output",
                                                                                        "outputFormat":"sp"}},
                                                      {"type":"gyrationRadius","parameters":{"intervalStep":10000,
                                                                                             "outputFilePath":"gyrationRadius.dat"}},
                                                      {"type":"info","parameters":{"intervalStep":10000}}]

                                   })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("PROT_IDP_TEST")

