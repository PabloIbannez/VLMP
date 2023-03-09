import sys, os

import logging

from . import systemBase

class simulationName(systemBase):

    """
    Simulation name
    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="simulationName",
                         _name= name,
                         availableParameters  = ["simulationName"],
                         compulsoryParameters = ["simulationName"],
                         **kwargs)

        ############################################################
        ####################  Name Parameters   ####################
        ############################################################

        self.system = {}
        self.system["name"] = kwargs.get("simulationName")

