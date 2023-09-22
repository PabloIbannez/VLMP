import sys, os

import logging

from . import modelBase

import numpy as np

class WLC(modelBase):
    """
    Component name: WLC
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Worm-like chain model. See https://en.wikipedia.org/wiki/Worm-like_chain

    :param N: Number of particles
    :type N: int
    :param mass: Mass of the particles
    :type mass: float, optional. Default: 1.0
    :param b: Distance between two consecutive particles
    :type b: float, optional. Default: 1.0
    :param Kb: Spring constant for bonds
    :type Kb: float, optional. Default: 1.0
    :param Ka: Spring constant for angles
    :type Ka: float, optional. Default: 1.0
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"N","mass","b","Kb","Ka","typeName","stericInteraction"},
                         requiredParameters  = {"N"},
                         definedSelections   = {"particleId","polymerIndex"},
                         **params)

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        #Read the number of particles
        self.N = params["N"]

        #Read the particle mass and the distance between two consecutive particles
        mass = params.get("mass",1.0)
        b    = params.get("b",1.0)

        #Read values for the spring constant for bonds and angles
        Kb = params.get("Kb",1.0)
        Ka = params.get("Ka",1.0)

        typeName = params.get("typeName","A")

        stericInteraction = params.get("stericInteraction",False)

        self.logger.debug(f"[WLC] Generating a WLC model with {self.N} particles")
        self.logger.debug(f"[WLC] Parameters: mass={mass}, b={b}, Kb={Kb}, Ka={Ka}")

        ########################################################
        ############### Generate the WLC model #################
        ########################################################

        #Add particle types
        types = self.getTypes()
        radius = 0.5*b
        types.addType(name=typeName,mass=mass,radius=radius)

        #Generate positions, a line along the z axis
        state = {}
        state["labels"] = ["id","position"]
        state["data"]   = []
        for i in range(self.N):
            state["data"].append([i, [0.0,0.0,i*b]])

        #Generate structure
        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"]   = []
        for i in range(self.N):
            structure["data"].append([i,typeName])

        #Generate forceField
        forceField = {}

        forceField["bonds"] = {}
        forceField["bonds"]["type"]       = ["Bond2","Harmonic"]
        forceField["bonds"]["parameters"] = {}
        forceField["bonds"]["labels"]     = ["id_i","id_j","K","r0"]
        forceField["bonds"]["data"]       = []

        for i in range(self.N-1):
            forceField["bonds"]["data"].append([i,i+1,Kb,b])

        forceField["angles"] = {}
        forceField["angles"]["type"]       = ["Bond3","KratkyPorod"]
        forceField["angles"]["parameters"] = {}
        forceField["angles"]["labels"]     = ["id_i","id_j","id_k","K"]
        forceField["angles"]["data"]       = []

        for i in range(self.N-2):
            forceField["angles"]["data"].append([i,i+1,i+2,Ka])

        ########################################################

        if stericInteraction:

            forceField["steric_nl"]={}
            forceField["steric_nl"]["type"]       =  ["VerletConditionalListSet", "nonExclIntra_nonExclInter"]
            forceField["steric_nl"]["parameters"] =  {"cutOffVerletFactor":1.1}
            forceField["steric_nl"]["labels"]     =  ["id","id_list"]
            forceField["steric_nl"]["data"]       =  []

            forceField["steric_nl"]["data"].append([0,[1]])
            for i in range(1,self.N-1):
                forceField["steric_nl"]["data"].append([i,[i-1,i+1]])
            forceField["steric_nl"]["data"].append([self.N-1,[self.N-2]])

            forceField["steric"] = {}
            forceField["steric"]["type"]       = ["NonBonded","WCAType2"]
            forceField["steric"]["parameters"] = {"cutOffFactor":1.0,"condition":"intra"}
            forceField["steric"]["labels"]     = ["name_i","name_j","epsilon","sigma"]
            forceField["steric"]["data"]       = [[typeName,typeName,1.0,2.0*radius]]

        ########################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        if "polymerIndex" in params:
            for pIndex in params["polymerIndex"]:
                if pIndex < -self.N or pIndex > self.N or pIndex == 0:
                    self.logger.error(f"[WLC] Invalid polymer index {pIndex}")
                    raise Exception("Invalid polymer index")

                if pIndex > 0:
                    sel.append(pIndex-1)
                if pIndex < 0:
                    sel.append(self.N+pIndex)

        return sel
