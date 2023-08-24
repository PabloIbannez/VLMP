import logging

def getLabelIndex(l,labels):
    logger = logging.getLogger("VLMP")

    if l in labels:
        return labels.index(l)
    else:
        logger.error("Label %s not found in labels list" % l)
        raise Exception("Label not found")

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
