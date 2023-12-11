from VLMP.components.models import modelBase

import json
import copy

class FILE(modelBase):
    """
    Component name: FILE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Load model from file

    :param inputFilePath: Path to the input file
    :type inputFilePath: str
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"inputFilePath"},
                         requiredParameters  = {"inputFilePath"},
                         definedSelections   = {"particleId","forceField"},
                         **params)

        ############################################################

        self.inputFilePath = params["inputFilePath"]
        self.logger.info(f"[FILE] Loading model from file {self.inputFilePath}")

        ########################################################

        with open(self.inputFilePath) as f:
            inputJSON = json.load(f)

        # TYPES

        types = self.getTypes()

        typesLabels = inputJSON["global"]["types"]["labels"]
        for typ in inputJSON["global"]["types"]["data"]:
            typInfo = {l:typ[i] for i,l in enumerate(typesLabels)}
            types.addType(**typInfo)

        #Generate positions
        state = copy.deepcopy(inputJSON["state"])

        #Generate structure
        structure = copy.deepcopy(inputJSON["topology"]["structure"])

        #Generate forceField
        forceField = copy.deepcopy(inputJSON["topology"]["forceField"])

        ########################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        if "forceField" in params:
            sel += self.getForceFieldSelection(params["forceField"])

        return sel
