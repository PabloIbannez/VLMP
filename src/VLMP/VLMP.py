import logging

import VLMP.models as mdls

from UAMMD.simulation import simulation

class VLMP:

    def __init__(self):
        self.logger = logging.getLogger("VLMP")

        self.logger.info("[VLMP] Starting VLMP")

    def addSimulationPool(self,simulationPool:dict):
        for simInfo in simulationPool:
            mdlName = simInfo["model"]["name"]
            mdl = eval("mdls."+mdlName)(**simInfo["model"]["parameters"])
            #######

            #getCoor .. and process transformations

            #######

            sim = simulation({"coordinates":mdl.getCoordinates(),"topology":mdl.getTopology()})





