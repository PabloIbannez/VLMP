import sys, os

import logging

from . import simulationStepBase

class AFMMaxForce(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements a maximum force criterion for Atomic Force Microscopy (AFM) simulations.
        <p> This step terminates the simulation when a specified maximum force is reached.",
        "parameters": {
            "maxForce": {
                "description": "The maximum force threshold for terminating the simulation.",
                "type": "float",
                "default": null
            }
        },
        "example": "
        {
            \"type\": \"AFMMaxForce\",
            \"parameters\": {
                \"maxForce\": 1000.0
            }
        }
        "
    }
    """

    availableParameters = {"maxForce"}
    requiredParameters  = {"maxForce"}
    availableSelections = set()
    requiredSelections  = set()

    def __init__(self,name,**params):
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        maxForce = params["maxForce"]

        simulationStep = {
            name:{
                  "type":["FlowControl","AFMMaxForce"],
                  "parameters":{"maxForce":maxForce}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


