import sys, os

import logging

from . import systemBase

class simulationName(systemBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Essential component for naming a simulation. This component is compulsory
      in every simulation configuration as each simulation requires a unique name.
      The 'simulationName' component assigns a descriptive and identifiable name
      to a simulation, facilitating its management and reference within the system.
      This name is used as the primary identifier for the simulation across various
      components and modules.",

     "parameters":{
        "simulationName":{"description":"Unique name assigned to the simulation",
                          "type":"str"}
            },

     "example":"
         {
            \"type\":\"simulationName\",
            \"simulationName\":\"MyUniqueSimulationName\"
         }
        "
    }
    """

    availableParameters = {"simulationName"}
    requiredParameters  = {"simulationName"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        system = {
            name:{"type":["Simulation","Information"],
                  "parameters":{}}
        }

        system[name]["parameters"]["name"] = params.get("simulationName")

        ############################################################

        self.setSystem(system)

