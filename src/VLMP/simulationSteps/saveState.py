import sys, os

import logging

from . import simulationStepBase

class saveState(simulationStepBase):
    """
    Save the state of the simulation. The state is saved in a file.
    The format can be selected by the user.
    :class:`saveState` is a subclass of :class:`simulationStepBase`.

    :param name: name of the simulation step
    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="Info",
                         _name= name,
                         availableParameters  = {"outputFilePath","outputFormat"},
                         compulsoryParameters = {"outputFilePath","outputFormat"},
                         **kwargs)

        ############################################################
        #################### Save State Parameters #################
        ############################################################

        self.simulationStep = {
            "write":{
              "type":["WriteStep","WriteStep"],
              "parameters":{"intervalStep":kwargs.get("intervalStep"),
                            "outputFilePath":kwargs.get("outputFilePath"),
                            "outputFormat":kwargs.get("outputFormat")}
            }
        }



