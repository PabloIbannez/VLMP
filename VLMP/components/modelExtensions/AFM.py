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
    :param sigma: sigma parameter for tip-particle interaction
    :type sigma: float
    :param K: spring constant
    :type K: float
    :param Kxy: xy spring constant
    :type Kxy: float
    :param tipVelocity: tip velocity
    :type tipVelocity: float
    :param startChipPosition: initial position of the chip
    :type startChipPosition: list of float [x,y,z]
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"epsilon",
                                                "sigma",
                                                "K","Kxy",
                                                "tipVelocity",
                                                "indentationStartStep",
                                                "indentationBackwardStep"},
                         requiredParameters  = {"epsilon",
                                                "sigma",
                                                "K","Kxy",
                                                "tipVelocity"},
                         availableSelections = {"tip","sample"},
                         requiredSelections  = {"tip","sample"},
                         **params)

        epsilon = params["epsilon"]
        sigma   = params["sigma"]

        K   = params["K"]
        Kxy = params["Kxy"]

        tipVelocity = params["tipVelocity"]

        indentationStartStep    = params.get("indentationStartStep",0)
        indentationBackwardStep = params.get("indentationBackwardStep",0)

        ############################################################

        tipIds    = self.getSelection("tip")
        sampleIds = self.getSelection("sample")

        # Check tipIds has only one element
        if len(tipIds) != 1:
            self.logger.error("AFM model extension only supports tips made of one particle")
            raise Exception("Not supported tip selection")
        else:
            tipPos = self.getIdsState(tipIds,"position")
            startChipPosition = tipPos[0]

            self.logger.debug(f"AFM model extension, startChipPosition: {startChipPosition}")


        extension = {}

        extension[name] = {}
        extension[name]["type"]       = ["AFM","SphericalTip"]
        extension[name]["parameters"] = {}

        extension[name]["labels"] = ["idSet_i","idSet_j","epsilon","sigma","K","Kxy","tipVelocity","startChipPosition","indentationStartStep","indentationBackwardStep"]
        extension[name]["data"]   = [[tipIds,sampleIds,epsilon,sigma,K,Kxy,tipVelocity,startChipPosition,indentationStartStep,indentationBackwardStep]]

        ############################################################

        self.setExtension(extension)
