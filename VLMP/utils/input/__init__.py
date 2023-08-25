import logging

def getLabelIndex(l,labels):
    logger = logging.getLogger("VLMP")

    if l in labels:
        return labels.index(l)
    else:
        logger.error("Label %s not found in labels list" % l)
        raise Exception("Label not found")

def getSubParameters(prmName,parameters):

    logger = logging.getLogger("VLMP")

    param = parameters.get(prmName,{})
    if not isinstance(param,dict):
        #Check if the parameter is a string
        if isinstance(param,str):
            param = {param:{}}
        else:
            logger.error(f"Parameter {prmName} is not a dictionary nor a string")
            raise Exception("Parameter is not a dictionary")

    parameterName   = None
    subParameters   = {}

    if len(param) == 0:
        return parameterName, subParameters
    if len(param) > 1:
        logger.error("Only one subparameter can be specified")
        raise Exception("Only one subparameter can be specified")

    parameterName = list(param.keys())[0]
    subParameters = param[parameterName]

    return parameterName, subParameters
