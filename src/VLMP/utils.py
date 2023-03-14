import logging
import copy

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

def getSelections(models,requiredSelections,**param):

    selections = {}

    for sel in [s for s in param.keys() if s in requiredSelections]:
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

            offSet = mdl.getIdOffset()
            mdlSelIds = [i+offSet for i in mdlSelIds]

            selections[sel] += mdlSelIds
        selections[sel] = list(set(selections[sel]))

    return copy.deepcopy(selections)


