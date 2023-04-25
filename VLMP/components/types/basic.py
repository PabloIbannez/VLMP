import sys, os

import logging

from . import typesBase

class basic(typesBase):

    """
    Component name: basic
    Component type: types

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    Basic types. Components:
    - mass: mass of the type
    - radius: radius of the type
    - charge: charge of the type

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = set(),
                         requiredParameters  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        self.setTypesName("Basic")

        self.addTypesComponent("mass", 1.0)
        self.addTypesComponent("radius", 1.0)
        self.addTypesComponent("charge", 0.0)
