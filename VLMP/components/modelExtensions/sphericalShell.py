import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class sphericalShell(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Creates a spherical shell potential around a selection of particles.",
        "parameters": {
            "shellCenter": {
                "description": "Center of the spherical shell.",
                "type": "list of float",
                "default": [0.0, 0.0, 0.0]
            },
            "shellRadius": {
                "description": "Radius of the spherical shell. This can be set to 'auto' to automatically set the radius.",
                "type": "float",
                "default": null
            },
            "shellEpsilon": {
                "description": "Energy parameter for the shell potential.",
                "type": "float",
                "default": 1.0
            },
            "shellSigma": {
                "description": "Distance parameter for the shell potential.",
                "type": "float",
                "default": 1.0
            },
            "minShellRadius": {
                "description": "Minimum radius of the spherical shell.",
                "type": "float",
                "default": 0.0
            },
            "maxShellRadius": {
                "description": "Maximum radius of the spherical shell.",
                "type": "float",
                "default": null
            },
            "radiusVelocity": {
                "description": "Velocity of the radius change.",
                "type": "float",
                "default": 0.0
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to be confined within the shell.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"sphericalShell\",
            \"parameters\": {
                \"shellCenter\": [0.0, 0.0, 0.0],
                \"shellRadius\": 10.0,
                \"shellEpsilon\": 1.0,
                \"shellSigma\": 1.0,
                \"selection\": \"model1 all\"
            }
        }
        "
    }
    """

    availableParameters = {"shellCenter",
                           "shellRadius",
                           "shellEpsilon",
                           "shellSigma",
                           "minShellRadius",
                           "maxShellRadius",
                           "radiusVelocity"}
    requiredParameters  = {"shellCenter",
                           "shellRadius"}
    availableSelections = {"selection"}
    requiredSelections  = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
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
