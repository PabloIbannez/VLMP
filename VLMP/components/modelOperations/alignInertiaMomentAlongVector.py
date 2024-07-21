from VLMP.components.modelOperations import modelOperationBase

import numpy as np

from scipy.spatial.transform import Rotation as R

class alignInertiaMomentAlongVector(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Aligns the largest inertia moment of selected particles along a specified vector.",
        "parameters": {
            "vector": {
                "description": "Vector along which to align the largest inertia moment.",
                "type": "list of float",
                "default": null
            },
        },
        "selections":{
            "selection": {
                "description": "Selection of particles to align.",
                "type": "list of ids",
            }
        },
        "example": "{
            "type": "alignInertiaMomentAlongVector",
            "parameters": {
                "vector": [0.0, 0.0, 1.0],
                "selection": \"model1 chain A\"
            }
        }"
    }
    """

    availableParameters = {"vector"}
    requiredParameters  = {"vector"}
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

        vector = np.asarray(params["vector"])
        vector /= np.linalg.norm(vector)

        ############################################################

        selectedIds = self.getSelection("selection")

        if len(selectedIds) == 0:
            self.error("No elements selected.")
            raise Exception("No elements selected.")

        if len(selectedIds) > 1:

            masses = np.asarray(self.getIdsProperty(selectedIds,"mass"))
            pos    = np.asarray(self.getIdsState(selectedIds,"position"))

            inertia = np.zeros((3,3))
            for i in range(len(selectedIds)):
                inertia += masses[i]*np.outer(pos[i],pos[i])

            inertia /= np.sum(masses)

            # Find the largest inertia moment
            eigVal, eigVec = np.linalg.eig(inertia)
            maxInertia = np.argmax(eigVal)

            maxInertiaVal = eigVal[maxInertia]
            maxInertiaVec = eigVec[:,maxInertia]
            maxInertiaVec /= np.linalg.norm(maxInertiaVec)

            #Compare maxInertiaVec with vector, and if they are not the same, rotate
            if np.dot(maxInertiaVec,vector) < 0.9999:
                # Find the rotation axis
                rotAxis = np.cross(maxInertiaVec,vector)
                rotAxis /= np.linalg.norm(rotAxis)

                # Find the rotation angle
                rotAngle = np.arccos(np.dot(maxInertiaVec,vector))
                rot = R.from_rotvec(rotAngle*rotAxis)

                # Rotate the model, create rotation matrix using scipy
                center = np.sum(pos*masses[:,np.newaxis],axis=0)/np.sum(masses)
                pos -= center
                pos = rot.apply(pos)
                pos += center

                self.setIdsState(selectedIds,"position",pos.tolist())
