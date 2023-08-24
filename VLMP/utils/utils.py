import logging
import copy

import numpy as np

from scipy.spatial.transform import Rotation as R
from pyquaternion import Quaternion

#Parameters processing

def readVariant(parameters):

    logger = logging.getLogger("VLMP")

    variant = parameters.get("variant",{})

    variantName   = None
    variantParams = {}

    if len(variant) == 0:
        return variantName, variantParams
    if len(variant) > 1:
        logger.error("Only one variant can be specified")
        raise Exception("Only one variant can be specified")

    variantName = list(variant.keys())[0]
    variantParams = variant[variantName]

    return variantName, variantParams

#Units utils

def picosecond2KcalMol_A_time():
    return 20/0.978


################################################################

def getLabelIndex(l,labels):
    logger = logging.getLogger("VLMP")

    if l in labels:
        return labels.index(l)
    else:
        logger.error("Label %s not found in labels list" % l)
        raise Exception("Label not found")

def getValuesAndPaths(d, key, path=None):
    """
    Recursively search a nested dictionary for all values associated with a given key,
    along with the path to each value.
    """

    if path is None:
        path = ()

    values = []
    for k, v in d.items():
        new_path = path + (k,)
        if k == key:
            values.append((v, new_path))
        elif isinstance(v, dict):
            values.extend(getValuesAndPaths(v, key, new_path))

    return values

def getSelections(models,selectionsList,**param):

    logger = logging.getLogger("VLMP")

    #Check params
    for p in param.keys():
        if p not in selectionsList:
            continue
        else:
            for k in param[p].keys():
                if k not in ["models","expression"]:
                    logger.error(f"[getSelections] Parameter {k} not recognized for selection {p},"
                                  " available parameters are: models, expression")
                    raise Exception("Unknown parameter")

    selections = {}

    for sel in [s for s in param.keys() if s in selectionsList]:
        selections[sel] = []

        if "models" in param[sel]:
            selectedModels = [ m for m in models if m.getName() in param[sel]["models"]]
        else:
            selectedModels = models

        for mdl in selectedModels:
            if "expression" in param[sel]:
                mdlSelIds = mdl.getSelection(**param[sel]["expression"])
            else:
                mdlSelIds = mdl.getSelection()

            offSet    = mdl.getIdOffset()
            mdlSelIds = [i+offSet for i in mdlSelIds]

            selections[sel] += mdlSelIds
        selections[sel] = list(set(selections[sel]))

    #Selection is a set of global ids
    return copy.deepcopy(selections)
