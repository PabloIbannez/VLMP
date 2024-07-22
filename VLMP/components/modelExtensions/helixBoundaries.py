from VLMP.components.modelExtensions import modelExtensionBase

class helixBoundaries(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements helical boundary conditions for simulations of helical structures.",
        "parameters": {
            "helixPitch": {"description": "Pitch of the helix", "type": "float", "default": null},
            "helixRadius": {"description": "Radius of the helix", "type": "float", "default": null},
            "eps": {"description": "Helix handedness (1 for right-handed, -1 for left-handed)", "type": "float", "default": null},
            "nTurns": {"description": "Number of turns in the helix", "type": "int", "default": null},
            "nPointsHelix": {"description": "Number of points to discretize the helix", "type": "int", "default": null},
            "helixInnerRadius": {"description": "Inner radius of the helix", "type": "float", "default": null},
            "nx": {"description": "Number of points in x direction", "type": "int", "default": null},
            "ny": {"description": "Number of points in y direction", "type": "int", "default": null},
            "nz": {"description": "Number of points in z direction", "type": "int", "default": null},
            "K": {"description": "Spring constant for boundary conditions", "type": "float", "default": null}
        },
        "selections": {
            "selection": {"description": "Particles to apply helical boundaries to", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"helixBoundaries\",
            \"parameters\": {
                \"helixPitch\": 5.0,
                \"helixRadius\": 10.0,
                \"eps\": 1.0,
                \"nTurns\": 5,
                \"nPointsHelix\": 100,
                \"helixInnerRadius\": 1.0,
                \"nx\": 10,
                \"ny\": 10,
                \"nz\": 50,
                \"K\": 100.0,
                \"selection\": \"model1 all\"
            }
        }"
    }
    """

    availableParameters = {"helixPitch","helixRadius",
                           "eps","nTurns",
                           "nPointsHelix","helixInnerRadius","K",
                           "nx","ny","nz"}
    requiredParameters  = {"helixPitch","helixRadius",
                           "eps","nTurns",
                           "nPointsHelix","helixInnerRadius","K",
                           "nx","ny","nz"}
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

        helixPitch  = params["helixPitch"]
        helixRadius = params["helixRadius"]
        if not isinstance(helixPitch,float):
            self.logger.error("Invalid value for helixPitch. It must be a float")
            raise ValueError("Invalid value for helixPitch")
        if not isinstance(helixRadius,float):
            self.logger.error("Invalid value for helixRadius. It must be a float")
            raise ValueError("Invalid value for helixRadius")

        eps = params["eps"]
        eps = float(eps)

        if eps not in [-1.0,1.0]:
            self.logger.error("Invalid value for eps. It must be either 1.0 or -1.0")
            raise ValueError("Invalid value for eps")

        nTurns = params["nTurns"]
        #Check if nTurns is an integer
        if not isinstance(nTurns,int):
            self.logger.error("Invalid value for nTurns. It must be an integer")
            raise ValueError("Invalid value for nTurns")

        nPointsHelix = params["nPointsHelix"]
        #Check if nPointsHelix is an integer
        if not isinstance(nPointsHelix,int):
            self.logger.error("Invalid value for nPointsHelix. It must be an integer")
            raise ValueError("Invalid value for nPointsHelix")

        helixInnerRadius = params["helixInnerRadius"]
        #Check if helixInnerRadius is a float
        if not isinstance(helixInnerRadius,float):
            self.logger.error("Invalid value for helixInnerRadius. It must be a float")
            raise ValueError("Invalid value for helixInnerRadius")

        K = params["K"]
        #Check if K is a float
        if not isinstance(K,float):
            self.logger.error("Invalid value for K. It must be a float")
            raise ValueError("Invalid value for K")

        nx = params["nx"]
        ny = params["ny"]
        nz = params["nz"]

        #Check if nx, ny and nz are integers
        if not isinstance(nx,int):
            self.logger.error("Invalid value for nx. It must be an integer")
            raise ValueError("Invalid value for nx")
        if not isinstance(ny,int):
            self.logger.error("Invalid value for ny. It must be an integer")
            raise ValueError("Invalid value for ny")
        if not isinstance(nz,int):
            self.logger.error("Invalid value for nz. It must be an integer")
            raise ValueError("Invalid value for nz")

        if "selection" in params:
            self.setGroup("selection")

        ############################################################

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","HelixBoundaries"]
        extension[name]["parameters"] = {"helixPitch":helixPitch,
                                         "helixRadius":helixRadius,
                                         "eps":eps,
                                         "nTurns":nTurns,
                                         "nPointsHelix":nPointsHelix,
                                         "helixInnerRadius":helixInnerRadius,
                                         "nx":nx,"ny":ny,"nz":nz,
                                         "K":K}

        ############################################################

        self.setExtension(extension)
