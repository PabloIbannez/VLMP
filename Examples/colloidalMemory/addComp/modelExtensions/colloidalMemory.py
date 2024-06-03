import sys, os, tempfile

import JFIO

import logging

from VLMP.components.modelExtensions import modelExtensionBase

import numpy as np
from scipy.integrate import quad

def df1(alpha,mu):
    return 1/(1-mu*np.cos(alpha))**(3/2)

def df2(alpha,mu):
    return np.cos(alpha)/(1-mu*np.cos(alpha))**(3/2)

def energyTabulated(X,Y,Z,r_ring=1.5,z_ring=0):
    # Define the limits of integration
    a = 0
    b = np.pi

    #reserve the space for the electric fields

    F1 = X*0
    F2 = X*0
    R = np.sqrt(X*X+(Z-z_ring)*(Z-z_ring)+Y*Y)
    Theta = np.arccos((Z-z_ring)/R)
    Theta[R==0] = 0
    Xi = R/r_ring
    Mu = (2*Xi)/(1+Xi*Xi)*np.sin(Theta)
    for i in range(len(Z)):
        mu = Mu[i]
        #perform the integration
        f1, error = quad(df1, a, b,args=(mu))
        F1[i] = f1
        f2, error = quad(df2, a, b,args=(mu))
        F2[i] = f2

    Er = 1/(np.pi*r_ring**2)*(Xi*np.sin(Theta)*F1/((1+Xi*Xi)**(3/2))-F2/((1+Xi*Xi)**(3/2)))
    Ez = 1/(np.pi*r_ring**2)*(Xi*np.cos(Theta)*F1/((1+Xi*Xi)**(3/2)))
    #Avoid division by zero
    XXYY = X*X+Y*Y
    XXYY[XXYY==0] = 1
    Ex = Er*X/XXYY
    Ey = Er*Y/XXYY
    e  = Ex*Ex+Ey*Ey+Ez*Ez
    return e

class colloidalMemory(modelExtensionBase):
    """
    Component name: colloidalMemory
    Component type: modelExtension

    Author: Pablo Diez-Silva
    Date: 05/16/2024

    Interactions of the model colloidalMemory. This model has two main interactions:

    1. Dielectrophoresis-interaction between porazable-particles and two ring-shaped electrodes.

    2. Surface WCA-interaction between particles and a system formed by a plain z=plainPosition and a cylinder-shaped well centered at x,y = 0,0.

    :param interactionMatrix: Matrix of interaction parameters between different types of particles and the surface.
    :type interactionMatrix: list of lists. Each list is a row of the matrix. Format particleType,epsilon,sigma
    :param plainPosition: Position of the plain in the system
    :type plainPositin: float, optional, default=0.0
    :param cylinderRadius: Radius of the cylinder-shaped well
    :type cylinderRadiues: float
    :param cellNumber: Number of cells in the tabulated energy
    :type cellNumber: list of integers
    :param : List of radii of the ring-shaped electrodes
    :type : list of floats
    :param ringHeight: List of Z-Positions of the ring-shaped electrodes
    :type ringPosition: list of floats
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters  = {"interactionMatrix","plainPosition","cylinderRadius","cellNumber","ringRadius","ringHeight"},
                         requiredParameters = {"interactionMatrix","cylinderRadius","cellNumber","ringRadius","ringHeight"},
                         availableSelections = set(),
                         requiredSelections = set(),
                         **params)

        extension = {}
        ############################################################
        ################# Plain Cylinder Surface ###################
        ############################################################

        interactionMatrix = params.get("interactionMatrix")
        cylinderRadius    = params.get("cylinderRadius")
        plainPosition     = params.get("plainPosition",0.0)

        extension[name] = {}
        extension[name]["type"] = ["Surface","WCA_PlainCylinder"]
        extension[name]["parameters"] = {"plainPosition":plainPosition,
                                         "cylinderRadius":cylinderRadius}
        extension[name]["labels"] = ["name","epsilon","sigma"]
        extension[name]["data"] = interactionMatrix.copy()


        ############################################################
        ################# Dielectrophoresis Forces #################
        ############################################################

        temporalFolder = tempfile.gettempdir()

        box = self.getEnsemble().getEnsembleComponent("box")
        cellNumber = params.get("cellNumber")
        ringRadius = params.get("ringRadius")
        ringHeight = params.get("ringHeight")

        if len(ringRadius) != len(ringHeight):
            raise ValueError("The number of ringRadius and ringHeight must be the same")

        for ring in range(len(ringRadius)):
            ringName = name+"_Dielectrophoresis_"+str(ring)
            pathTabulated = os.path.join(temporalFolder,ringName+".json")
            extension[ringName]={}
            extension[ringName]["type"]=["External","PolarizationTabulated"]
            extension[ringName]["parameters"]={"nx":cellNumber[0],"ny":cellNumber[1],"nz":cellNumber[2]}
            extension[ringName]["labels"]=["i","j","k","energy","force"]
            extension[ringName]["data"]=[]
            calculateData = True #Flag to calculate the data

            if os.path.exists(pathTabulated):
                existingData = JFIO.read(pathTabulated)
                if (existingData["parameters"]["nx"] == cellNumber[0] and existingData["parameters"]["ny"] == cellNumber[1] and existingData["parameters"]["nz"] == cellNumber[2]
                    and existingData["auxiliarParameters"]["diff"] == [box[i]/cellNumber[i]/2 for i in range(3)]
                    and existingData["auxiliarParameters"][""] == ringRadius[ring] and existingData["auxiliarParameters"]["ringHeight"] == ringHeight[ring]):

                    logging.warning("Reading tabulated dielectrophoresis forces from "+pathTabulated)
                    extension[ringName]["data"] = existingData["data"]
                    calculateData = False #Flag to avoid calculating the data

            if calculateData: #Calculate the data
                diff = [box[i]/cellNumber[i]/2 for i in range(3)]
                x_array, y_array, z_array = [np.linspace(-box[i]/2+diff[i],box[i]/2-diff[i],cellNumber[i]) for i in range(3)]
                X,Y,Z = np.meshgrid(x_array,y_array,z_array,indexing='ij')
                E = energyTabulated(X.flatten(),Y.flatten(),Z.flatten(),r_ring=ringRadius[ring],z_ring=ringHeight[ring])
                E = E.reshape(X.shape)
                F = np.gradient(E,diff[0],diff[1],diff[2])
                F = [-F[0],-F[1],-F[2]]

                for i in range(cellNumber[0]):
                    for j in range(cellNumber[1]):
                        for k in range(cellNumber[2]):
                            extension[ringName]["data"].append([i,j,k,E[i,j,k],[F[0][i,j,k],F[1][i,j,k],F[2][i,j,k]]])

                saved_json = extension[ringName].copy()
                saved_json["auxiliarParameters"] = {"diff":diff,"":ringRadius[ring],"ringHeight":ringHeight[ring]}
                JFIO.write(pathTabulated,saved_json)

        self.setExtension(extension)
