import sys, os

import logging

from . import simulationStepBase

class lambdaActivation(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Controls the activation of lambda parameter in thermodynamic integration simulations.",
        "parameters": {
            "lambdaValueStep": {
                "description": "Step size for changing lambda value.",
                "type": "float",
                "default": 0.1
            },
            "lambdaValues": {
                "description": "List of lambda values to use in the simulation.",
                "type": "list of float",
                "default": [0.0, 1.0]
            }
        },
        "example": "
        {
            \"type\": \"lambdaActivation\",
            \"parameters\": {
                \"lambdaValueStep\": 0.1,
                \"lambdaValues\": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            }
        }
        "
    }
    """

    availableParameters = {"lambdaValueStep","lambdaValues"}
    requiredParameters  = {"lambdaValueStep","lambdaValues"}
    availableSelections = set()
    requiredSelections  = set()

    def __init__(self,name,**params):
        # Chech if interval step is defined
        if 'intervalStep' in params:
            # Check if interval step is equal to 1
            if params['intervalStep'] != 1:
                # Raise error
                raise ValueError('Interval step must be equal to 1 for lambdaActivation component')
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

        lambdaValueStep = params['lambdaValueStep']
        lambdaValues    = params['lambdaValues']

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
                  "type":["FlowControl","LambdaActivation"],
                  "parameters":{"lambdaValueStep":lambdaValueStep,
                                "lambdaValues":lambdaValues}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


