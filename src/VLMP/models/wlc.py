import sys, os

import logging

from . import modelBase

import numpy as np

class wlc(modelBase):
    """
    Worm-like chain model. See https://en.wikipedia.org/wiki/Worm-like_chain
    :class:`wlc` is a subclass of :class:`modelBase`.

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

    def __init__(self,name,**kwargs):
        super().__init__(_type="WLC",
                         _name= name,
                         availableParameters  = {"N","mass","b","Kb","Ka"},
                         compulsoryParameters = {"N"},
                         availableSelectors   = {"particleId"},
                         **kwargs)

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        #Read the number of particles
        self.N = kwargs.get("N")

        #Read the particle mass and the distance between two consecutive particles
        self.mass = kwargs.get("mass",1.0)
        self.b    = kwargs.get("b",1.0)

        #Read values for the spring constant for bonds and angles
        self.Kb = kwargs.get("Kb",1.0)
        self.Ka = kwargs.get("Ka",1.0)

        self.logger.debug(f"[WLC] Generating a WLC model with {self.N} particles")
        self.logger.debug(f"[WLC] Parameters: mass={self.mass}, b={self.b}, Kb={self.Kb}, Ka={self.Ka}")

        ########################################################
        ############### Generate the WLC model #################
        ########################################################

        #Add particle types
        self.types = {}
        self.types["labels"] = ["name", "mass", "radius", "charge"]
        self.types["data"]   = [
            ["A", self.mass, 0.5*self.b, 0.0]
        ]

        #Generate positions, a line along the z axis
        self.state = {}
        self.state["labels"] = ["id","position"]
        self.state["data"]   = []
        for i in range(self.N):
            self.state["data"].append([i, [0.0,0.0,i*self.b]])

        #Generate structure
        self.structure = {}
        self.structure["labels"] = ["id","type"]
        self.structure["data"]   = []
        for i in range(self.N):
            self.structure["data"].append([i,"A"])

        #Generate forceField
        self.forceField = {}

        self.forceField["bonds"] = {}
        self.forceField["bonds"]["type"]       = ["Bond2","HarmonicCommon_K_r0"]
        self.forceField["bonds"]["parameters"] = {"K":self.Kb, "r0":self.b}
        self.forceField["bonds"]["labels"]     = ["id_i","id_j"]
        self.forceField["bonds"]["data"]       = []

        for i in range(self.N-1):
            self.forceField["bonds"]["data"].append([i,i+1])

        self.forceField["angles"] = {}
        self.forceField["angles"]["type"]       = ["Bond3","KratkyPorodCommon_K"]
        self.forceField["angles"]["parameters"] = {"K":self.Ka}
        self.forceField["angles"]["labels"]     = ["id_i","id_j","id_k"]
        self.forceField["angles"]["data"]       = []

        for i in range(self.N-2):
            self.forceField["angles"]["data"].append([i,i+1,i+2])

    def processSelection(self,**kwargs):
        if "particleId" in kwargs:
            return kwargs["particleId"]
