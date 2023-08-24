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
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        shellCenter = params["shellCenter"]
        shellRadius = params["shellRadius"]

        ###########

        shellEpsilon = params.get("shellEpsilon",1.0)
        shellSigma   = params.get("shellSigma",1.0)

        minShellRadius = params.get("minShellRadius",0.0)
        maxShellRadius = params.get("maxShellRadius","INFINITY")

        radiusVelocity = params.get("radiusVelocity",0.0)

        ###########

        if shellRadius == "auto":
            if "selection" not in params:
                self.logger.error(f"[sphericalShell] ({name}) Selection \
                                    is required when shellRadius is 'auto'.")
                raise Exception("Not compatible parameters.")

            # Get selection
            selIds = self.getSelection("selection")

            # Get the maximum distance to the center
            posIds = self.getIdsState(selIds, "position")
            maxDist = np.max(np.linalg.norm(np.asarray(posIds) - shellCenter, axis=1))

            self.logger.debug(f"[sphericalShell] ({name}) Maximum distance to the center: {maxDist}")

            # Get the maximum radius
            radIds = self.getIdsProperty(selIds, "radius")
            maxRad = np.max(radIds)

            self.logger.debug(f"[sphericalShell] ({name}) Maximum radius: {maxRad}")

            shellRadius = maxDist + (shellSigma  + maxRad)*1.1

            self.logger.info(f"[sphericalShell] ({name}) Shell radius: {shellRadius}")

        elif "selection" in params:
            self.logger.error(f"[sphericalShell] ({name}) Selection selected \
                                but radius is not set to 'auto'.")
            raise Exception("Not compatible parameters.")

        ###########

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
