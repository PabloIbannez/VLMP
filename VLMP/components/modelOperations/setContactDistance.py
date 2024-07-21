import sys, os

import logging

from . import modelOperationBase

import numpy as np
from scipy.spatial import cKDTree

class setContactDistance(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Sets the contact distance between two selections of particles.",
        "parameters": {
            "distance": {
                "description": "Target contact distance between the selections.",
                "type": "float",
                "default": null
            },
            "resolution": {
                "description": "Resolution for the contact distance adjustment.",
                "type": "float",
                "default": 0.1
            },
            "inverse": {
                "description": "Whether to invert the direction of the contact.",
                "type": "bool",
                "default": false
            }
        },
        "selections": {
            "reference": {
                "description": "Reference selection of particles.",
                "type": "list of ids"
            },
            "mobile": {
                "description": "Mobile selection of particles to be moved.",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"setContactDistance\",
            \"parameters\": {
                \"distance\": 5.0,
                \"resolution\": 0.01,
                \"inverse\": false,
                \"reference\": \"model1 type A\",
                \"mobile\": \"model2 type B\"
            }
        }"
    }
    """

    availableParameters = {"distance","resolution","inverse"}
    requiredParameters  = {"distance","resolution"}
    availableSelections = {"reference","mobile"}
    requiredSelections  = {"reference","mobile"}

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

        dst = params["distance"]
        res = params["resolution"]
        inv = params.get("inverse",False)

        referenceIds = self.getSelection("reference")
        mobileIds    = self.getSelection("mobile")

        referencePos  = np.asarray(self.getIdsState(referenceIds,"position"))
        referenceRads = np.asarray(self.getIdsProperty(referenceIds,"radius"))

        mobilePos  = np.asarray(self.getIdsState(mobileIds,"position"))
        mobileRads = np.asarray(self.getIdsProperty(mobileIds,"radius"))

        # Compute the total radius of each selection
        refCenter = np.mean(referencePos,axis=0)
        mobCenter = np.mean(mobilePos,axis=0)

        # Compute the vector between the centers
        centersVec = mobCenter-refCenter
        if inv:
            for i in range(mobilePos.shape[0]):
                mobilePos[i] = mobCenter-2.0*centersVec
            centersVec = -centersVec
        centersVec = centersVec/np.linalg.norm(centersVec)

        stepSize = res
        prevDist = None
        while True:

            minDst,minDstIndex = cKDTree(referencePos).query(mobilePos, 1)

            ############################################################

            mobileClosestIndex = np.argmin(minDst)
            mobileClosestDst   = minDst[mobileClosestIndex]

            mobileClosestPos = mobilePos[mobileClosestIndex]
            mobileClosestRad = mobileRads[mobileClosestIndex]

            ############################################################

            referenceClosestIndex = minDstIndex[mobileClosestIndex]
            referenceClosestDst   = minDst[mobileClosestIndex]

            referenceClosestPos = referencePos[referenceClosestIndex]
            referenceClosestRad = referenceRads[referenceClosestIndex]

            ############################################################

            currentDst = mobileClosestDst - (mobileClosestRad + referenceClosestRad)

            if np.abs(currentDst-dst) < res:
                break

            if prevDist is not None:
                if np.abs(currentDst-dst) > np.abs(prevDist-dst):
                    stepSize = stepSize/2

            if (currentDst < dst):
                for i in range(mobilePos.shape[0]):
                    mobilePos[i] = mobilePos[i] + centersVec * stepSize
                prevDist = currentDst

            if (currentDst > dst):
                for i in range(mobilePos.shape[0]):
                    mobilePos[i] = mobilePos[i] - centersVec * stepSize
                prevDist = currentDst

        newPos = []
        for i in range(len(mobileIds)):
            newPos.append(list(mobilePos[i]))

        self.setIdsState(mobileIds,"position",newPos)








