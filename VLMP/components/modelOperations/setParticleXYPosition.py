from VLMP.components.modelOperations import modelOperationBase

import numpy as np

class setParticleXYPosition(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Sets the XY position of selected particles to a specified value.",
        "parameters": {
            "position": {
                "description": "New XY position for the particles.",
                "type": "list of float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to move.",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"setParticleXYPosition\",
            \"parameters\": {
                \"position\": [1.0, 2.0],
                \"selection\": \"model1 type A\"
            }
        }"
    }
    """

    availableParameters = {"position"}
    requiredParameters  = {"position"}
    availableSelections = {"selection"}
    requiredSelections  = {"selection"}

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

        # Check if the given position is a list of two floats
        if not isinstance(params["position"],list) or len(params["position"]) != 2:
            self.logger.error("The given position must be a list of two floats.")
            raise Exception("Parameter bad format")

        targetPosition = params["position"]

        selectedIds = self.getSelection("selection")
        pos = np.asarray(self.getIdsState(selectedIds,"position"))

        for i in range(len(selectedIds)):
            pos[i][0] = targetPosition[0]
            pos[i][1] = targetPosition[1]

        self.setIdsState(selectedIds,"position",pos.tolist())
