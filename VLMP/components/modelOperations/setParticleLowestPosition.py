from VLMP.components.modelOperations import modelOperationBase

import numpy as np

class setParticleLowestPosition(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Sets the lowest particle in the selection to a specified Z position.",
        "parameters": {
            "position": {
                "description": "Z coordinate to set for the lowest particle.",
                "type": "float",
                "default": null
            },
            "considerRadius": {
                "description": "Whether to consider particle radius when setting the position.",
                "type": "bool",
                "default": false
            },
            "radiusFactor": {
                "description": "Factor to multiply the radius by when considering it.",
                "type": "float",
                "default": 1.0
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to consider.",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"setParticleLowestPosition\",
            \"parameters\": {
                \"position\": 0.0,
                \"considerRadius\": true,
                \"radiusFactor\": 1.1,
                \"selection\": \"model1 all\"
            }
        }"
    }
    """

    availableParameters = {"position","considerRadius","radiusFactor"}
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

        selectedIds = self.getSelection("selection")

        pos    = np.asarray(self.getIdsState(selectedIds,"position"))

        if params.get("considerRadius",False):
            rad = np.asarray(self.getIdsProperty(selectedIds,"radius"))
            radFactor = params.get("radiusFactor",1.0)
            rad = radFactor*rad

        # Find the lowest position
        lowestPosIndex = np.argmin(pos[:,2])
        lowestPos      = pos[lowestPosIndex,2]

        # Set the lowest position to the given value
        offset = 0.0
        if params.get("considerRadius",False):
            rad = np.asarray(self.getIdsProperty(selectedIds,"radius"))
            offset = rad[lowestPosIndex]

        translation = np.asarray([0,0,params["position"] - lowestPos + offset])

        for i in range(len(selectedIds)):
            pos[i] = pos[i] + translation

        self.setIdsState(selectedIds,"position",pos.tolist())
