import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setContactDistance(modelOperationBase):

    """
    Component name: setDistance
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 28/08/2023

    Set the contact distance between two selections of particles.

    :param distance: distance to set
    :type distance: float
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"distance","invert"},
                         requiredParameters  = {"distance"},
                         availableSelections = {"reference","mobile"},
                         requiredSelections  = {"reference","mobile"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        dst = params["distance"]
        inv = params.get("invert",False)

        referenceIds = self.getSelection("reference")
        mobileIds    = self.getSelection("mobile")

        referencePos  = np.asarray(self.getIdsState(referenceIds,"position"))
        referenceRads = np.asarray(self.getIdsProperty(referenceIds,"radius"))

        mobilePos  = np.asarray(self.getIdsState(mobileIds,"position"))
        mobileRads = np.asarray(self.getIdsProperty(mobileIds,"radius"))

        # Compute the total radius of each selection
        refCenter = np.mean(referencePos,axis=0)
        refMaxRad = np.max(np.linalg.norm(referencePos-refCenter,axis=1)+referenceRads)

        mobCenter = np.mean(mobilePos,axis=0)
        mobMaxRad = np.max(np.linalg.norm(mobilePos-mobCenter,axis=1)+mobileRads)

        # Compute the vector between the centers
        centersVec = mobCenter-refCenter
        if inv:
            centersVec = -centersVec

        targetCenterDist = refMaxRad + mobMaxRad + dst

        # Compute the final position of the mobile selection in order to
        # have the desired distance
        newMobileCenter = refCenter + (centersVec/np.linalg.norm(centersVec))*targetCenterDist
        translation = newMobileCenter - mobCenter

        newPos = []
        for i in range(len(mobileIds)):
            newPos.append(list(mobilePos[i]+translation))

        self.setIdsState(mobileIds,"position",newPos)








