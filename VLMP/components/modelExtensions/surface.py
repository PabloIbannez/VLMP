from VLMP.components.modelExtensions import modelExtensionBase

class surface(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Adds a surface interaction to the simulation.",
        "parameters": {
            "epsilon": {"description": "Energy parameter for surface-particle interaction", "type": "float", "default": 1.0},
            "surfacePosition": {"description": "Z-coordinate of the surface", "type": "float", "default": 0.0}
        },
        "selections": {
            "selection": {"description": "Particles interacting with the surface", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"surface\",
            \"parameters\": {
                \"epsilon\": 1.0,
                \"surfacePosition\": -10.0,
                \"selection\": \"model1 all\"
            }
        }"
    }
    """

    availableParameters = {"epsilon",
                           "surfacePosition"}
    requiredParameters  = {"surfacePosition"}
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

        surfacePosition = params.get("surfacePosition",0.0)
        epsilon         = params.get("epsilon",1.0)

        if "selection" in params:
            self.setGroup("selection")

        ############################################################

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Surface","SurfaceGeneralLennardJonesType2"]
        extension[name]["parameters"] = {"surfacePosition":surfacePosition}

        extension[name]["labels"] = ["name","epsilon","sigma"]
        extension[name]["data"] = []

        types = self.getTypes()
        for typ,info in types.getTypes().items():
            extension[name]["data"].append([typ,epsilon,info["radius"]])

        ############################################################

        self.setExtension(extension)
