import sys, os

import random
import math

import logging

from . import modelOperationBase

from ...utils.selections import splitStateAccordingStructure
from ...utils.input import getSubParameters
from ...utils.geometry import distributeRandomlyGeneratorChecker

from scipy.spatial.transform import Rotation

import numpy as np

class distributeRandomly(modelOperationBase):

    """
    Component name: distributeRandomly
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 26/08/2023

    Distribution of the selected particles in different bounds

    :param mode: Mode of distribution, the bound where the particles will be distributed, can be "box" or "sphere"
    :type mode: dict, optional, default='box'
    :param avoidClashes: If is larger than 0, the particles will be distributed avoiding clashes with other particles.
                         The value of this parameter is the number of tries to avoid the clash.
                         If the number of tries is reached, an error will be raised.
    :type avoidClashes: int, optional, default=0
    :param randomRotation: If True, the particles will be randomly rotated before being distributed
    :type randomRotation: bool, optional, default=True

    """

    def __randomBoxPoint(self):
        mp = np.random.uniform(low  = [-self.boxX,-self.boxY,-self.boxZ],
                               high = [ self.boxX, self.boxY, self.boxZ])
        return mp

    def __boxCheckDistance(self,p1,p2,r1,r2):
        # Check if the distance between two points is larger than the sum of the radius
        # of the particles, taking into account the periodicity of the box

        # Calculate the distance between the two points
        dr = p1-p2
        # Apply mic periodicity
        dr[0] = dr[0] - math.floor(dr[0]/self.box[0]+0.5)*self.box[0]
        dr[1] = dr[1] - math.floor(dr[1]/self.box[1]+0.5)*self.box[1]
        dr[2] = dr[2] - math.floor(dr[2]/self.box[2]+0.5)*self.box[2]

        d = np.linalg.norm(dr)

        # Check if the distance is larger than the sum of the radius
        if d > 1.05*(r1+r2):
            return True

        return False

    def __randomSpherePoint(self):
        # Generate a random point in a sphere
        # of center self.center and radius self.radius

        maxRad = np.max([np.max(r) for r in self.modelsRads])

        # Generate random radius
        rho = (self.radius-maxRad)*(random.random() ** (1/3))

        # Generate random angles
        theta = math.acos(2 * random.random() - 1)  # Polar angle
        phi = 2 * math.pi * random.random()         # Azimuthal angle

        # Convert to Cartesian coordinates
        x = rho * math.sin(theta) * math.cos(phi)
        y = rho * math.sin(theta) * math.sin(phi)
        z = rho * math.cos(theta)

        mp = np.array([x,y,z]) + self.center

        return mp

    def __sphereCheckDistance(self,p1,p2,r1,r2):
        # Check if the distance between two points is larger than the sum of the radius
        # of the particles

        # Calculate the distance between the two points
        d = np.linalg.norm(p1-p2)

        # Check if the distance is larger than the sum of the radius
        if d > 1.05*(r1+r2):
            return True

        return False

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"mode","avoidClashes","randomRotation"},
                         requiredParameters  = set(),
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        self.randomRotation = params.get("randomRotation",True)

        self.mode,self.modeParams = getSubParameters("mode",params)

        if self.mode == "box" or self.mode == None:
            self.box  = self.getEnsemble().getEnsembleComponent("box")
            self.boxX,self.boxY,self.boxZ = [b/2.0 for b in self.box]

            self.getRandomPoint = self.__randomBoxPoint
            self.checkDistance  = self.__boxCheckDistance

        elif self.mode == "sphere":

            requiredModeParams = {"center","radius"}

            if not requiredModeParams.issubset(self.modeParams):
                self.logger.error(f"Missing parameters for mode {self.mode}: {requiredModeParams}")
                raise Exception("Missing parameters")

            self.center = self.modeParams["center"]
            self.radius = self.modeParams["radius"]

            self.box  = self.getEnsemble().getEnsembleComponent("box")
            boxX,boxY,boxZ = [b/2.0 for b in self.box]

            # Check center is inside the box
            if self.center[0] < -boxX or self.center[0] > boxX:
                self.logger.error(f"Center {self.center} is outside the box in X")
                raise Exception("Center outside box")
            if self.center[1] < -boxY or self.center[1] > boxY:
                self.logger.error(f"Center {self.center} is outside the box in Y")
                raise Exception("Center outside box")
            if self.center[2] < -boxZ or self.center[2] > boxZ:
                self.logger.error(f"Center {self.center} is outside the box in Z")
                raise Exception("Center outside box")

            # Check sphere is inside the box
            if self.center[0] - self.radius < -boxX or self.center[0] + self.radius > boxX:
                self.logger.error(f"Sphere is outside the box in X")
                raise Exception("Sphere outside box")
            if self.center[1] - self.radius < -boxY or self.center[1] + self.radius > boxY:
                self.logger.error(f"Sphere is outside the box in Y")
                raise Exception("Sphere outside box")
            if self.center[2] - self.radius < -boxZ or self.center[2] + self.radius > boxZ:
                self.logger.error(f"Sphere is outside the box in Z")
                raise Exception("Sphere outside box")

            self.getRandomPoint = self.__randomSpherePoint
            self.checkDistance  = self.__sphereCheckDistance

        else:
            self.logger.error(f"Mode {self.mode} not recognized, available modes are 'box' and 'sphere'")
            raise Exception(f"Mode not recognized")

        avoidClashes = params.get("avoidClashes",0)

        ############################################################

        selectedIds = self.getSelection("selection")

        mods = np.asarray(self.getIdsStructure(selectedIds,"modelId"))
        pos  = np.asarray(self.getIdsState(selectedIds,"position"))
        rads = self.getIdsProperty(selectedIds,"radius")

        self.modelsPos = splitStateAccordingStructure(state=pos,
                                                      structure=mods)

        self.modelsRads = splitStateAccordingStructure(state=rads,
                                                       structure=mods)

        if self.randomRotation:
            for i in range(len(self.modelsPos)):

                mp = self.modelsPos[i]

                center = np.mean(mp,axis=0)
                mp -= center

                #Use scipy to generate a random rotation matrix
                R = Rotation.random().as_matrix()

                mp = np.dot(mp,R.T)

                mp += center

                self.modelsPos[i] = mp

        if not avoidClashes:
            newPositions = []
            for i in range(len(self.modelsPos)):
                center = np.mean(self.modelsPos[i],axis=0)
                # Generete a random 3D position
                mp = self.getRandomPoint()

                transVec = mp - center

                newPositions.append([list(p+transVec) for p in self.modelsPos[i]])

            newPositions = [p for mp in newPositions for p in mp]
        else:
            newPositions = distributeRandomlyGeneratorChecker(self.box,
                                                              self.modelsPos,self.modelsRads,
                                                              self.getRandomPoint,self.checkDistance,
                                                              avoidClashes,
                                                              1.05)

        self.setIdsState(selectedIds,"position",newPositions)

