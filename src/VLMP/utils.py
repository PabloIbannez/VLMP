
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

