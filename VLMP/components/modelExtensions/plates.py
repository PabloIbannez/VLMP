import numpy as np

from VLMP.components.modelExtensions import modelExtensionBase

class plates(modelExtensionBase):

    """
    Component name: plates
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Common epsilon, sigma plates for particles in the system.

    :param platesSeparation: Distance between plates.
    :param epsilon: Energy parameter for the plates.
    :param sigma: Length parameter for the plates.
    :param compressionVelocity: Velocity at which the plates are compressed.
    :param minPlatesSeparation: Minimum distance between plates.
    :param maxPlatesSeparation: Maximum distance between plates.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {'platesSeparation',
                                                'epsilon','sigma',
                                                'compressionVelocity',
                                                'minPlatesSeparation','maxPlatesSeparation'},
                         requiredParameters  = {"platesSeparation",
                                                "epsilon","sigma"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        platesSeparation = params.get("platesSeparation","auto")

        epsilon         = params["epsilon"]
        sigma           = params["sigma"]

        compressionVelocity = params.get("compressionVelocity",0.0)

        minPlatesSeparation = params.get("minPlatesSeparation",None)
        maxPlatesSeparation = params.get("maxPlatesSeparation",None)

        parameters = {"platesEpsilon":epsilon,
                      "platesSigma":sigma,
                      "compressionVelocity":compressionVelocity}

        if "selection" in params and platesSeparation != "auto":
            self.logger.warning("Selection is ignored when platesSeparation is not set to 'auto'")

        if platesSeparation == "auto":
            # Check if selection is defined
            if "selection" not in params:
                self.logger.error("Selection must be defined when platesSeparation is set to 'auto'")
                raise ValueError("No selection defined")
            else:
                selectedIds  = self.getSelection("selection")
                idsPositions = self.getIdsState(selectedIds,"position")

                if len(idsPositions) == 0:
                    self.logger.error("Selection is empty")
                    raise ValueError("Empty selection")

                platesSeparation = np.max(np.abs(np.array(idsPositions)[:,2]))+sigma
                platesSeparation = 2*platesSeparation

                self.logger.info("Plates separation set to {}".format(platesSeparation))
                parameters["platesSeparation"] = platesSeparation

        if minPlatesSeparation is not None:
            parameters["minPlatesSeparation"] = minPlatesSeparation

        if maxPlatesSeparation is not None:
            parameters["maxPlatesSeparation"] = maxPlatesSeparation

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","Plates"]
        extension[name]["parameters"] = parameters

        ############################################################

        self.setExtension(extension)
