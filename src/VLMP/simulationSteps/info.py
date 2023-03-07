import sys, os

import logging

from . import simulationStepBase

class info(simulationStepBase):
    """
    Simple info step, it shows the current step,
    an estimation of the remaining time and the mean FPS.
    :class:`info` is a subclass of :class:`simulationStepBase`.

    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="Info",
                         _name= name,
                         availableParameters  = {},
                         compulsoryParameters = {},
                         **kwargs)
        print("info.__init__")
