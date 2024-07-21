from VLMP.components.modelOperations import modelOperationBase

import numpy as np

from scipy.spatial.transform import Rotation as R

class rotation(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a rotation to selected particles around a specified axis.",
        "parameters": {
            "axis": {
                "description": "Axis of rotation.",
                "type": "list of float",
                "default": null
            },
            "angle": {
                "description": "Angle of rotation in radians.",
                "type": "float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to rotate.",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"rotation\",
            \"parameters\": {
                \"axis\": [0.0, 0.0, 1.0],
                \"angle\": 3.14159,
                \"selection\": \"model1 resid 1 to 10\"
            }
        }"
    }
    """

    availableParameters = {"axis","angle"}
    requiredParameters  = {"axis","angle"}
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

        rotAxis = params["axis"]
        angle   = params["angle"]

        ############################################################

        selectedIds = self.getSelection("selection")

        if len(selectedIds) == 0:
            self.error("No elements selected.")
            raise Exception("No elements selected.")

        if len(selectedIds) > 1:

            pos    = np.asarray(self.getIdsState(selectedIds,"position"))

            center = np.mean(pos,axis=0)
            pos    = pos - center

            rotAxis = np.asarray(rotAxis)
            rotAxis = rotAxis/np.linalg.norm(rotAxis)

            r = R.from_rotvec(angle*rotAxis)
            pos = r.apply(pos)

            pos = pos + center

            self.setIdsState(selectedIds,"position",pos.tolist())
