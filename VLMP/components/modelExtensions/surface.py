from VLMP.components.modelExtensions import modelExtensionBase

class surface(modelExtensionBase):

    """
    Component name: surface
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Common epsilon, sigma surface for particles in the system.

    :param epsilon: epsilon of the surface
    :type epsilon: float
    :param surfacePosition: position of the surface
    :type surfacePosition: float
    :param ignoredTypes: types to ignore
    :type ignoredTypes: list

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
