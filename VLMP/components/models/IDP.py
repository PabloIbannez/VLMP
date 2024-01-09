import sys, os

import copy

import logging

import numpy as np

from . import modelBase

from pyGrained.utils.data import getData

class IDP(modelBase):
    """
    Component name: IDP
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/03/2023

    Intrinsic disorder protein model.

    Reference: https://journals.aps.org/pre/pdf/10.1103/PhysRevE.90.042709

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"sequence"},
                         requiredParameters  = {"sequence"},
                         definedSelections   = {"particleId"},
                         **params)

        EXCLUSION_DST = 3

        HYDROPHOBICITY_MONERA = {
            'ALA': 0.62,  # Alanine
            'ARG': 0.26,  # Arginine
            'ASN': 0.17,  # Asparagine
            'ASP': 0.0,   # Aspartic Acid
            'CYS': 0.67,  # Cysteine
            'GLN': 0.28,  # Glutamine
            'GLU': 0.15,  # Glutamic Acid
            'GLY': 0.35,  # Glycine
            'HIS': 0.4,   # Histidine
            'ILE': 0.99,  # Isoleucine
            'LEU': 0.98,  # Leucine
            'LYS': 0.2,   # Lysine
            'MET': 0.83,  # Methionine
            'PHE': 1.0,   # Phenylalanine
            'PRO': 0.05,  # Proline
            'SER': 0.32,  # Serine
            'THR': 0.43,  # Threonine
            'TRP': 0.97,  # Tryptophan
            'TYR': 0.75,  # Tyrosine
            'VAL': 0.84   # Valine
        }

        ############################################################


        sequence = params["sequence"]

        kT = self.getEnsemble().getEnsembleComponent("temperature")*self.getUnits().getConstant("KBOLTZ")

        Kb = kT/((0.046)**2)
        r0 = 3.9

        Ka     = kT/((0.26)**2)
        theta0 = 2.12

        self.logger.info(f"kT = {kT}")
        self.logger.info(f"Kb = {Kb}, r0 = {r0}")
        self.logger.info(f"Ka = {Ka}, theta0 = {theta0}")

        sigma       = 4.8
        debyeLength = 9.0
        dielectricConstant = 80.0

        # Energy parameters

        #alphaCG = 0.52
        alphaCG = 0.50

        kes = 1.485 # This is computed for dielectricConstant = 80.0, and sigma = 4.8 !!!

        epsilon_r = 1.0*kT # It does not change.
        epsilon_a = alphaCG*kes*kT

        #

        debyeCutOffFactor = 1.2 # "and the screened Coulomb potential V es is negligible beyond the screening length λ" from reference

        ############################################################
        ######################  Set up model  ######################
        ############################################################

        units = self.getUnits()

        if units.getName() != "KcalMol_A":
            self.logger.error(f"[MADna] Units are not set correctly. Please set units to \"KcalMol_A\" (selected: {units.getName()})")
            raise Exception("Not correct units")

        ############################################################
        # Set up types

        names   = getData("aminoacids")
        masses  = getData("aminoacidMasses")
        radii   = getData("aminoacidRadii")
        charges = getData("aminoacidCharges")

        # In this model the charge of HIS is 0.1
        charges["HIS"] = 0.1

        #Invert names dict
        aminoacids_3to1 = {v: k for k, v in names.items()}

        ############################################################

        types = self.getTypes()
        for nm in names:
            types.addType(name = nm,
                          mass = masses[nm],
                          radius = radii[nm],
                          charge = charges[nm])

        ############################################################

        # State

        state = {}
        state["labels"] = ["id","position"]
        state["data"]   = []

        for i,s in enumerate(sequence):
            pos = [0,0,r0*i]
            # We add small random noise to avoid dihedral singularities
            pos = np.array(pos) + np.random.normal(0,0.01,3)
            pos = pos.tolist()
            state["data"].append([i,pos])

        # Structure

        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"]   = []

        for i,s in enumerate(sequence):
            try:
                structure["data"].append([i,aminoacids_3to1[s]])
            except:
                self.logger.error(f"[IDP] Aminoacid {s} not recognized")
                raise Exception("Aminoacid not recognized")

        # Forcefield

        forcefield = {}

        forcefield["bonds"] = {}
        forcefield["bonds"]["type"]             = ["Bond2","HarmonicCommon_K_r0"]
        forcefield["bonds"]["parameters"]       = {}
        forcefield["bonds"]["parameters"]["K"]  = Kb
        forcefield["bonds"]["parameters"]["r0"] = r0
        forcefield["bonds"]["labels"]           = ["id_i","id_j"]
        forcefield["bonds"]["data"]             = []

        for i in range(len(sequence)-1):
            forcefield["bonds"]["data"].append([i,i+1])

        forcefield["angles"] = {}
        forcefield["angles"]["type"]                 = ["Bond3","HarmonicAngularCommon_K_theta0"]
        forcefield["angles"]["parameters"]           = {}
        forcefield["angles"]["parameters"]["K"]      = Ka
        forcefield["angles"]["parameters"]["theta0"] = theta0
        forcefield["angles"]["labels"]               = ["id_i","id_j","id_k"]
        forcefield["angles"]["data"]                 = []

        for i in range(len(sequence)-2):
            forcefield["angles"]["data"].append([i,i+1,i+2])

        forcefield["dihedrals"] = {}
        forcefield["dihedrals"]["type"]                 = ["Bond4","IDP_Fourier"]
        forcefield["dihedrals"]["parameters"]           = {}
        forcefield["dihedrals"]["labels"]               = ["id_i","id_j","id_k","id_l"]
        forcefield["dihedrals"]["data"]                 = []

        for i in range(len(sequence)-3):
            forcefield["dihedrals"]["data"].append([i,i+1,i+2,i+3])

        # Non bonded

        exclusions = {}
        for i in range(len(sequence)):
            for j in range(i+1,len(sequence)):
                if np.abs(i-j) <= EXCLUSION_DST:
                    exclusions.setdefault(i,[]).append(j)
                    exclusions.setdefault(j,[]).append(i)

        for exc in exclusions:
            exclusions[exc] = sorted(list(set(exclusions[exc])))

        #NL
        forcefield["nl"] = {}
        forcefield["nl"]["type"]       = ["VerletConditionalListSet", "nonExcluded"]
        forcefield["nl"]["parameters"] = {"cutOffVerletFactor": 1.5}
        forcefield["nl"]["labels"]     = ["id", "id_list"]
        forcefield["nl"]["data"] = []

        if EXCLUSION_DST != 0:
            for i in range(len(sequence)):
                forcefield["nl"]["data"].append([i,exclusions[i]])

        # HYDROPHOBIC
        forcefield["hydrophobic"] = {}
        forcefield["hydrophobic"]["type"]       = ["NonBonded", "SplitLennardJones"]
        forcefield["hydrophobic"]["parameters"] = {"cutOffFactor": 2.5,
                                                   "epsilon_r": epsilon_r,
                                                   "epsilon_a": epsilon_a,
                                                   "condition":"nonExcluded"}

        forcefield["hydrophobic"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forcefield["hydrophobic"]["data"]   = []

        for t1 in names:
            for t2 in names:
                eps = np.sqrt(HYDROPHOBICITY_MONERA[t1]*HYDROPHOBICITY_MONERA[t2])
                forcefield["hydrophobic"]["data"].append([t1,t2,eps,sigma])

        #DH
        forcefield["DH"] = {}
        forcefield["DH"]["type"]       = ["NonBonded", "DebyeHuckel"]
        forcefield["DH"]["parameters"] = {"cutOffFactor": debyeCutOffFactor,
                                          "debyeLength": debyeLength,
                                          "dielectricConstant": dielectricConstant,
                                          "condition":"nonExcluded"}

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forcefield)

    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
