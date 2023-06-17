import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class sphericalShell(modelExtensionBase):

    """
    Component name: sphericalShell
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 15/06/2023

    Spherical shell model extension for the model.

    :param shellCenter: Center of the spherical shell.
    :type shellCenter: list of floats
    :param shellRadius: Radius of the spherical shell.
    :type shellRadius: float
    :param shellEpsilon: Epsilon of the spherical shell.
    :type shellEpsilon: float, optional (default = 1.0)
    :param shellSigma: Sigma of the spherical shell.
    :type shellSigma: float, optional (default = 1.0)
    :param minShellRadius: Minimum radius of the spherical shell.
    :type minShellRadius: float, optional (default = 0.0)
    :param maxShellRadius: Maximum radius of the spherical shell.
    :type maxShellRadius: float, optional (default = inf)
    :param radiusVelocity: Velocity of the radius of the spherical shell.
    :type radiusVelocity: float, optional (default = 0.0)

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"shellCenter",
                                                "shellRadius",
                                                "shellEpsilon",
                                                "shellSigma",
                                                "minShellRadius",
                                                "maxShellRadius",
                                                "radiusVelocity"},
                         requiredParameters  = {"shellCenter",
                                                "shellRadius"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        shellCenter = params["shellCenter"]
        shellRadius = params["shellRadius"]

        shellEpsilon = params.get("shellEpsilon",1.0)
        shellSigma   = params.get("shellSigma",1.0)

        minShellRadius = params.get("minShellRadius",0.0)
        maxShellRadius = params.get("maxShellRadius","INFINITY")

        radiusVelocity = params.get("radiusVelocity",0.0)

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","SphericalShell"]
        extension[name]["parameters"] = {"shellCenter":shellCenter,
                                         "shellRadius":shellRadius,
                                         "shellEpsilon":shellEpsilon,
                                         "shellSigma":shellSigma,
                                         "minShellRadius":minShellRadius,
                                         "radiusVelocity":radiusVelocity}

        if maxShellRadius != "INFINITY":
            extension[name]["parameters"]["maxShellRadius"] = maxShellRadius

        ############################################################

        self.setExtension(extension)
