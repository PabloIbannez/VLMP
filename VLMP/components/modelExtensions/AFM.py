from VLMP.components.modelExtensions import modelExtensionBase

class AFM(modelExtensionBase):

    """
    Component name: AFM
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    AFM model extension.

    :param epsilon: epsilon parameter for tip-particle interaction
    :type epsilon: float
    :param K: spring constant
    :type K: float
    :param Kxy: xy spring constant
    :type Kxy: float
    :param tipVelocity: tip velocity
    :type tipVelocity: float
    :param startChipPosition: initial position of the chip
    :type startChipPosition: list of float [x,y,z]
    :param surfacePosition: position of the surface
    :type surfacePosition: float, z coordinate

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"epsilon",
                                                "K","Kxy",
                                                "tipVelocity",
                                                "startChipPosition",
                                                "surfacePosition"},
                         requiredParameters  = {"epsilon",
                                                "K","Kxy",
                                                "tipVelocity",
                                                "startChipPosition",
                                                "surfacePosition"},
                         availableSelections = {"tip","sample"},
                         requiredSelections  = {"tip","sample"},
                         **params)

        epsilon = params["epsilon"]

        K   = params["K"]
        Kxy = params["Kxy"]

        tipVelocity = params["tipVelocity"]

        startChipPosition = params["startChipPosition"]
        surfacePosition   = params["surfacePosition"]

        ############################################################

        tipIds    = self.getSelection("tip")
        sampleIds = self.getSelection("sample")

        extension = {}

        extension[name] = {}
        extension[name]["type"]       = ["AFM","SphericalTip"]
        extension[name]["parameters"] = {}

        extension[name]["labels"] = ["idSet_i","idSet_j","epsilon","K","Kxy","tipVelocity","startChipPosition","surfacePosition"]
        extension[name]["data"]   = [[tipIds,sampleIds,epsilon,K,Kxy,tipVelocity,startChipPosition,surfacePosition]]

        ############################################################

        self.setExtension(extension)
