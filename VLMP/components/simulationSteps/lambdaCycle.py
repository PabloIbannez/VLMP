import sys, os

import logging

from . import simulationStepBase

class lambdaCycle(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements a cycle of lambda values for enhanced sampling in thermodynamic integration.",
        "parameters": {
            "activationStep": {
                "description": "Number of steps for each lambda activation phase.",
                "type": "int",
                "default": 1000
            },
            "measureStep": {
                "description": "Number of steps for measurement at each lambda value.",
                "type": "int",
                "default": 500
            },
            "pauseStep": {
                "description": "Number of steps for pause between lambda changes.",
                "type": "int",
                "default": 100
            },
            "lambdaValues": {
                "description": "List of lambda values to cycle through.",
                "type": "list of float",
                "default": [0.0, 1.0]
            }
        },
        "example": "
        {
            \"type\": \"lambdaCycle\",
            \"parameters\": {
                \"activationStep\": 1000,
                \"measureStep\": 500,
                \"pauseStep\": 100,
                \"lambdaValues\": [0.0, 0.25, 0.5, 0.75, 1.0]
            }
        }
        "
    }
    """

    availableParameters = {"activationStep","measureStep","pauseStep","lambdaValues"}
    requiredParameters  = {"activationStep","measureStep","pauseStep","lambdaValues"}
    availableSelections = set()
    requiredSelections  = set()

    def __init__(self,name,**params):
        # Chech if interval step is defined
        if 'intervalStep' in params:
            # Check if interval step is equal to 1
            if params['intervalStep'] != 1:
                # Raise error
                raise ValueError('Interval step must be equal to 1 for lambdaCycle component')
        else:
            # Set interval step to 1
            params['intervalStep'] = 1
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

        activationStep = params['activationStep']
        measureStep    = params['measureStep']
        pauseStep      = params['pauseStep']

        lambdaValues   = params['lambdaValues']

        #Check if lambdaValues is a list and all elements are numbers between 0 and 1
        if not isinstance(lambdaValues,list):
            self.logger.error('lambdaValues must be a list')
            raise TypeError('lambdaValues must be a list')
        else:
            for i in lambdaValues:
                if not isinstance(i,(int,float)):
                    self.logger.error('lambdaValues must be a list of numbers')
                    raise TypeError('lambdaValues must be a list of numbers')
                elif i < 0 or i > 1:
                    self.logger.error('lambdaValues must be a list of numbers between 0 and 1')
                    raise ValueError('lambdaValues must be a list of numbers between 0 and 1')

        # The first element of lambdaValues must be 0 and the last one must be 1
        if lambdaValues[0] != 0:
            self.logger.error('The first element of lambdaValues must be 0')
            raise ValueError('The first element of lambdaValues must be 0')
        elif lambdaValues[-1] != 1:
            self.logger.error('The last element of lambdaValues must be 1')
            raise ValueError('The last element of lambdaValues must be 1')

        simulationStep = {
            name:{
                  "type":["FlowControl","LambdaCycle"],
                  "parameters":{"activationStep":activationStep,
                                "measureStep":measureStep,
                                "pauseStep":pauseStep,
                                "lambdaValues":lambdaValues}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


