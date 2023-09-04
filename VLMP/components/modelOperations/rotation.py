from VLMP.components.modelOperations import modelOperationBase

import numpy as np

from scipy.spatial.transform import Rotation as R

class rotation(modelOperationBase):

    """
    Component name: rotation
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 01/09/2023

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"axis","angle"},
                         requiredParameters  = {"axis","angle"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
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
