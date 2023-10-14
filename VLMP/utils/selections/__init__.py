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

        currentSelIdsLen = None
        for mdl in selectedModels:
            if "expression" in param[sel]:
                mdlSelIds = mdl.getSelection(**param[sel]["expression"])
            else:
                mdlSelIds = mdl.getSelection()

            offSet    = mdl.getIdOffset()

            #Check if mdlSelIds[0] is a list
            if isinstance(mdlSelIds[0],list):
                selIdsLen = len(mdlSelIds[0])
            else:
                selIdsLen = 1

            if currentSelIdsLen is None:
                currentSelIdsLen = selIdsLen
            elif currentSelIdsLen != selIdsLen:
                logger.error(f"[getSelections] Selection {sel} has different lengths")
                raise Exception("Selection has different lengths")

            for i in range(len(mdlSelIds)):
                if selIdsLen == 1:
                    mdlSelIds[i] += offSet
                else:
                    for j in range(selIdsLen):
                        mdlSelIds[i][j] += offSet

            selections[sel] += mdlSelIds

        if currentSelIdsLen == 1:
            selections[sel] = list(set(selections[sel]))
        else:
            selections[sel] = list(set([tuple(s) for s in selections[sel]]))

#            offSet    = mdl.getIdOffset()
#            mdlSelIds = [i+offSet for i in mdlSelIds]
#
#            selections[sel] += mdlSelIds
#        selections[sel] = list(set(selections[sel]))

    #Selection is a set of global ids
    return copy.deepcopy(selections)

def splitStateAccordingStructure(state,structure):

    logger = logging.getLogger("VLMP")

    #Check state and structure have the same length
    if len(state) != len(structure):
        logger.error("[splitStateAccordingStructure] State and structure have different lengths")
        raise Exception("State and structure have different lengths")

    # Structure has to have the following format:
    # [A,A,A,...,B,B,B,...,C,C,C,...,...]
    # Each letter represents a different structure
    # Check structure is correct
    appearedStructures = []
    for s in structure:
        if s not in appearedStructures:
            appearedStructures.append(s)
        elif s != appearedStructures[-1]:
            logger.error("[splitStateAccordingStructure] Structure is not correct")
            raise Exception("Structure is not correct")
        else:
            continue

    # Split pos according the different models
    splittedState = []

    currentStruct      = structure[0]
    currentStructState = []
    for i in range(len(structure)):
        if structure[i] == currentStruct:
            currentStructState.append(state[i])
        else:
            splittedState.append(currentStructState)
            currentStruct      = structure[i]
            currentStructState = [state[i]]

    splittedState.append(currentStructState)

    # At this point, splittedState is a list of lists,
    # each list contains the state of a model
    #                       struct[0]          struct[1]   ...
    # splittedState = [[state1_0,state2_0,...],[state1_0,state2_0,...],...]
    # It is ensured that the order is kept.
    # splittedState is the state list splitted according the structure

    return splittedState



