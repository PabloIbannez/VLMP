from VLMP.components.modelExtensions import modelExtensionBase

class AFM(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Atomic Force Microscopy (AFM) model extension for simulating AFM experiments.
                       This extension add an interaction between a particle (the tip) and other set of
                       particles (the sample). The interaction between the tip and the sample is modeled
                       as a Lennard-Jones potential. The tip is modeled as a spherical particle with a
                       spring attached to it.",
        "parameters": {
            "K": {"description": "Spring constant for the AFM cantilever", "type": "float", "default": null},
            "Kxy": {"description": "Lateral spring constant", "type": "float", "default": null},
            "epsilon": {"description": "Energy parameter for tip-sample interaction", "type": "float", "default": null},
            "sigma": {"description": "Distance parameter for tip-sample interaction", "type": "float", "default": null},
            "tipVelocity": {"description": "Velocity of the AFM tip", "type": "float", "default": null},
            "indentationStartStep": {"description": "Simulation step to start indentation", "type": "int", "default": 0},
            "indentationBackwardStep": {"description": "Simulation step to start backward indentation", "type": "int", "default": null}
        },
        "selections": {
            "tip": {"description": "Selection for the AFM tip", "type": "list of with one id, [id]"},
            "sample": {"description": "Selection for the sample particles", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"AFM\",
            \"parameters\": {
                \"K\": 1.0,
                \"Kxy\": 0.5,
                \"epsilon\": 1.0,
                \"sigma\": 1.0,
                \"tipVelocity\": 0.1,
                \"indentationStartStep\": 1000,
                \"tip\": \"model1 type TIP\",
                \"sample\": \"model2\"
            }
        }"
    }
    """

    availableParameters = {"epsilon",
                           "sigma",
                           "K","Kxy",
                           "tipVelocity",
                           "indentationStartStep",
                           "indentationBackwardStep"}
    requiredParameters  = {"epsilon",
                           "sigma",
                           "K","Kxy",
                           "tipVelocity"}
    availableSelections = {"tip","sample"}
    requiredSelections  = {"tip","sample"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
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
