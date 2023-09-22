import logging

########################################################

from ..utils.input import getLabelIndex

class idsHandler:

    _models     = None

    _id2model   = None
    _id2localId = None

    def __getModelLocalId(self, i):
        return idsHandler._id2model[i], idsHandler._id2localId[i]

    def __init__(self,
                 models):

        logger = logging.getLogger("VLMP")

        if idsHandler._models is None or idsHandler._models != models:

            logger.debug("Initializing idsHandler")

            idsHandler._models = models

            N = sum([mdl.getNumberOfParticles() for mdl in idsHandler._models])

            idsHandler._id2model   = [None]*N
            idsHandler._id2localId = [None]*N

            offset = 0
            for mdlIndex,mdl in enumerate(idsHandler._models):
                for i in range(mdl.getNumberOfParticles()):
                    idsHandler._id2model[i+offset]   = mdlIndex
                    idsHandler._id2localId[i+offset] = i

                offset += mdl.getNumberOfParticles()

            logger.debug("Done initializing idsHandler")
        else:
            logger.debug("idsHandler already initialized")

    ######################## GETTERS #######################

    def _getIdsProperty(self,globalIds,propertyName):
        idsProperty = []

        for i in globalIds:
            mdlIndex, localId = self.__getModelLocalId(i)

            mdl = idsHandler._models[mdlIndex]

            typeIndex = getLabelIndex("type",mdl.getStructure()["labels"])
            itype     = mdl.getStructure()["data"][localId][typeIndex]

            idsProperty.append(mdl.getTypes().getTypes()[itype][propertyName])

        return idsProperty

    def _getIdsState(self,globalIds,stateName):
        idsState = []

        for i in globalIds:
            mdlIndex, localId = self.__getModelLocalId(i)

            mdl = idsHandler._models[mdlIndex]

            stateIndex = getLabelIndex(stateName,mdl.getState()["labels"])
            stateValue = mdl.getState()["data"][localId][stateIndex]

            idsState.append(stateValue)

        return idsState

    def _getIdsStructure(self,globalIds,structureName):

        totalParticles = sum([mdl.getNumberOfParticles() for mdl in idsHandler._models])

        id2struct = [None]*totalParticles
        structOffset = 0
        for mdl in idsHandler._models:
            structLabels = mdl.getStructure()["labels"]
            for i in mdl.getGlobalIds():
                mdlIndex, localId = self.__getModelLocalId(i)
                mdl = idsHandler._models[mdlIndex]

                maxStruct = structOffset
                if structureName in structLabels:
                    structIndex  = getLabelIndex(structureName,structLabels)
                    structValue  = mdl.getStructure()["data"][localId][structIndex]

                    id2struct[i] = structValue+structOffset
                else:
                    id2struct[i] = structOffset

                maxStruct = max(maxStruct,id2struct[i])

            structOffset += maxStruct+1

        ########################################################

        idsStructure = []

        for i in globalIds:
            idsStructure.append(id2struct[i])

        return idsStructure

    ######################## SETTERS #######################

    def _setIdsState(self,globalIds,stateName,states):

        logger = logging.getLogger("VLMP")

        if len(globalIds) != len(states):
            logger.error(f"[ModelOperation] Number of ids and states ({stateName}) do not match")
            raise Exception(f"Number of ids and states do not match")

        for i,s in zip(globalIds,states):
            mdlIndex, localId = self.__getModelLocalId(i)
            mdl = idsHandler._models[mdlIndex]

            stateIndex = getLabelIndex(stateName,mdl.getState()["labels"])

            #Check if state is valid
            if type(s) != type(mdl.getState()["data"][localId][stateIndex]):
                logger.error(f"[ModelOperation] State value {s} for state \"{stateName}\" is not valid."
                             f" State value type is {type(s)} but should be {type(mdl.getState()['data'][localId][stateIndex])}")
                raise Exception(f"State is not valid")
            else:
                if type(s) == list:
                    if len(s) != len(mdl.getState()["data"][localId][stateIndex]):
                        logger.error(f"[ModelOperation] State value {s} for state \"{stateName}\" is not valid, length does not match")
                        raise Exception(f"State is not valid")

                mdl.getState()["data"][localId][stateIndex] = s
