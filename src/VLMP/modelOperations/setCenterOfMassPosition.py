import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setCenterOfMassPosition(modelOperationBase):
    """
    Set the center of mass position of the model.
    :class:`setCenterOfMassPosition` is a subclass of :class:`modelOperationBase`.

    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="SetCenterOfMassPosition",
                         _name= name,
                         availableParameters  = {},
                         compulsoryParameters = {},
                         **kwargs)
        print("setCenterOfMassPosition.__init__")

    def apply(self,**kwargs):
        print("setCenterOfMassPosition.apply")

