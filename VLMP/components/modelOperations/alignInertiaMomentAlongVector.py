from VLMP.components.modelOperations import modelOperationBase

import numpy as np

from scipy.spatial.transform import Rotation as R

class alignInertiaMomentAlongVector(modelOperationBase):

    """
    Component name: alignInertiaMomentAlongVector
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Aling the largest inertia moment of the selected elements along a given vector.

    :param vector: Vector along which the inertia moment will be aligned.
    :type vector: list of floats

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"vector"},
                         requiredParameters  = {"vector"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
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
