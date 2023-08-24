import logging
import copy

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

