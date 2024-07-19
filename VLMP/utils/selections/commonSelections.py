import copy

import logging

from VLMP.utils.input import getLabelIndex
from VLMP.utils.input.stringUtils import string2integerList

availableCommonSelections = [
        'id',
        'type',
        'res',
        'chain',
        'model',
        'forceField'
]

def modelStructureSelection(model, selectionType, selectionOptions, applyOffset=False):

    logger = logging.getLogger("VLMP")

    rename = {
        'id': 'id',
        'type': 'type',
        'res': 'resId',
        'chain': 'chainId',
        'model': 'modelId',
    }

    if selectionType not in rename:
        logger.error(f"[ModelStructureSelection] Requested selection type {selectionType}"
                          f" as an structure selection type. But it is not available")
        raise Exception(f"Selection type not available")

    selectionType = rename[selectionType]

    structure = model.getStructure()
    sel = []

    if selectionType == "id":
        # Selection options is a list of integers (as string)
        selectedIDs = string2integerList(selectionOptions)
        # Check if all selectedIDs are in model.getLocalIds()
        localIds = model.getLocalIds()
        if set(selectedIDs).issubset(localIds):
            sel = selectedIDs
    else:
        idLabelIndex  = getLabelIndex("id",structure["labels"])
        strLabelIndex = getLabelIndex(selectionType,structure["labels"])

        if selectionType in ["resId","chainId","modelId"]:
            selectionOptions = string2integerList(selectionOptions)
        else: # selectionType == "type"
            selectionOptions = selectionOptions.split()
            selectionOptions = [x.strip() for x in selectionOptions]

        for i in range(len(structure["data"])):
            if structure["data"][i][strLabelIndex] in selectionOptions:
                sel.append(structure["data"][i][idLabelIndex])

    ##############################################################

    if applyOffset:
        sel = [model.getIdOffset() + i for i in sel]
    return sel

def forceFieldSelection(model, selectionType, selectionOptions, applyOffset=False):

    logger = logging.getLogger("VLMP")

    forceFieldEntriesName = selectionOptions.split()
    forceFieldEntriesName = [x.strip() for x in forceFieldEntriesName]

    sel = []

    forceField = model.getForceField()
    # Check if forceFieldEntriesName is in forceField
    for ff in forceFieldEntriesName:
        if ff not in forceField:
            logger.error(f"[Model] ({model.getName()}) Force field entry {ff} not in force field")
            raise Exception(f"Force field entry not in force field")
        else:
            entryType = forceField[ff]["type"][0]

            entryLabels = forceField[ff]["labels"]
            entryData   = forceField[ff]["data"]

            if entryType == "Bond1":
                id1Index = getLabelIndex("id_i",entryLabels)
                for i in range(len(entryData)):
                    id1 = int(entryData[i][id1Index])
                    sel.append(id1)

            elif entryType == "Bond2":
                id1Index = getLabelIndex("id_i",entryLabels)
                id2Index = getLabelIndex("id_j",entryLabels)
                for i in range(len(entryData)):
                    id1 = int(entryData[i][id1Index])
                    id2 = int(entryData[i][id2Index])
                    sel.append([id1,id2])

            elif entryType == "Bond3":
                id1Index = getLabelIndex("id_i",entryLabels)
                id2Index = getLabelIndex("id_j",entryLabels)
                id3Index = getLabelIndex("id_k",entryLabels)
                for i in range(len(entryData)):
                    id1 = int(entryData[i][id1Index])
                    id2 = int(entryData[i][id2Index])
                    id3 = int(entryData[i][id3Index])
                    sel.append([id1,id2,id3])

            elif entryType == "Bond4":
                id1Index = getLabelIndex("id_i",entryLabels)
                id2Index = getLabelIndex("id_j",entryLabels)
                id3Index = getLabelIndex("id_k",entryLabels)
                id4Index = getLabelIndex("id_l",entryLabels)
                for i in range(len(entryData)):
                    id1 = int(entryData[i][id1Index])
                    id2 = int(entryData[i][id2Index])
                    id3 = int(entryData[i][id3Index])
                    id4 = int(entryData[i][id4Index])
                    sel.append([id1,id2,id3,id4])

            else:
                logger.error(f"[Model] ({model.getName()}) Force field entry {ff} has not an available type."
                              "Available types are: Bond1, Bond2, Bond3, Bond4")
                raise Exception(f"Force field entry has not an available type")

    if applyOffset:
        if len(sel[0]) == 1:
            sel = [model.getIdOffset() + i for i in sel]
        else:
            sel = [[model.getIdOffset() + i for i in bond] for bond in sel]
    return sel




def processCommonSelection(models, selectionType, selectionOptions, applyOffset=False):

    logger = logging.getLogger("VLMP")

    if not isinstance(models,list):
        models = [models]

    sel = []
    if selectionType in ["id","type","res","chain","model"]:
        for model in models:
            selBuffer = modelStructureSelection(model, selectionType, selectionOptions, applyOffset)
            if len(selBuffer) > 0:
                sel += selBuffer
            else:
                logger.warning(f"[CommonSelection] Selection type {selectionType} with options {selectionOptions} "
                               f"is empty for model {model.getName()}")
    if selectionType == "forceField":
        for model in models:
            selBuffer = forceFieldSelection(model, selectionType, selectionOptions, applyOffset)
            if len(selBuffer) > 0:
                sel += selBuffer
            else:
                logger.warning(f"[CommonSelection] Selection type {selectionType} with options {selectionOptions} "
                               f"is empty for model {model.getName()}")

    if len(sel) == 0:
        modelsNames = [model.getName() for model in models]
        logger.warning(f"[CommonSelection] Selection type {selectionType} with options {selectionOptions} "
                       f"is empty for models {modelsNames}")

    return sel
