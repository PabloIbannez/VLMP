import sys, os

import logging

from . import typesBase

class none(typesBase):

    """
    Component name: none
    Component type: types

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    None types. No components are added.
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

        self.setTypesName("None")
