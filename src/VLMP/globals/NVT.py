import sys, os

import logging

from . import globalBase

class NVT(globalBase):

    """
    Set the box size and temperature.
    :class:`NVT` is a subclass of :class:`GlobalBase`.

    :param box: box size
    :param temperature: temperature

    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="NVT",
                         _name= name,
                         availableParameters  = ["box","temperature"],
                         compulsoryParameters = ["box","temperature"],
                         **kwargs)

        ############################################################
        ####################  NVT Parameters ####################
        ############################################################

        self.globals = {}

        self.globals["box"]         = kwargs.get("box")
        self.globals["temperature"] = kwargs.get("temperature")
