import sys, os

import logging

from . import unitsBase

class none(unitsBase):

    """
    None units. No conversion is performed. All constants are set to 1.
    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="none",
                         _name= name,
                         availableParameters  = [],
                         compulsoryParameters = [],
                         **kwargs)

        ############################################################
        ####################  None Parameters   ####################
        ############################################################

        self.unitsUAMMD = "none"

    def fromInputToInternalTime(self, time):
        return time
