import numpy as np

from VLMP.components.modelExtensions import modelExtensionBase

class plates(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Adds two parallel plates to the simulation box, typically used for confinement.",
        "parameters": {
            "platesSeparation": {
                "description": "Distance between the two plates.",
                "type": "float",
                "default": null
            },
            "epsilon": {
                "description": "Energy parameter for plate-particle interactions.",
                "type": "float",
                "default": null
            },
            "sigma": {
                "description": "Distance parameter for plate-particle interactions.",
                "type": "float",
                "default": null
            },
            "compressionVelocity": {
                "description": "Velocity at which the plates are compressed.",
                "type": "float",
                "default": 0.0
            },
            "minPlatesSeparation": {
                "description": "Minimum allowed separation between plates.",
                "type": "float",
                "default": null
            },
            "maxPlatesSeparation": {
                "description": "Maximum allowed separation between plates.",
                "type": "float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles that interact with the plates.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"plates\",
            \"parameters\": {
                \"platesSeparation\": 20.0,
                \"epsilon\": 1.0,
                \"sigma\": 1.0,
                \"selection\": \"model1 all\"
            }
        }
        "
    }
    """

    availableParameters = {'platesSeparation',
                           'epsilon','sigma',
                           'compressionVelocity',
                           'minPlatesSeparation','maxPlatesSeparation'}
    requiredParameters  = {"platesSeparation",
                           "epsilon","sigma"}
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
        else:
            parameters["platesSeparation"] = float(platesSeparation)

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
