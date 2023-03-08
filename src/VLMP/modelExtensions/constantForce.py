import sys, os

import logging

from . import modelExtensionBase

import numpy as np

class constantForce(modelExtensionBase):
    """
    Apply a constant force to the model
    :class:`constantForce` is a subclass of :class:`modelExtensionBase`.

    :param force: force to be applied to the model
    :type force: list of floats
    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="ConstantForce",
                         _name= name,
                         availableParameters  = {"force"},
                         compulsoryParameters = {"force"},
                         **kwargs)
        self.extension = {}
        print("constantForce.__init__")
