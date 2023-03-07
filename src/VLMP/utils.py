def getLabelIndex(l,labels):
    logger = logging.getLogger("VLMP")

    if l in labels:
        return labels.index(l)
    else:
        logger.error("Label %s not found in labels list" % l)
        raise Exception("Label not found")

