import sys, os

import logging

from . import simulationStepBase

class lambdaActivation(simulationStepBase):
    """
    Component name: lambdaActivation
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 03/01/2023

    Lambda activation.

    :param activationStep: Activation step.
    :type activationStep: int
    :param measureStep: Measure step.
    :type measureStep: int
    :param pauseStep: Pause step.
    :type pauseStep: int
    :param lambdaValues: Lambda values.
    :type lambdaValues: list

    """

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
                         availableParameters = {"lambdaValueStep","lambdaValues"},
                         requiredParameters  = {"lambdaValueStep","lambdaValues"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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


