import logging
import copy

from .commonSelections import availableCommonSelections
from .commonSelections import processCommonSelection

def selectionListType(selectionList):

    logger = logging.getLogger("VLMP")

    # Return 0 if selectionList is empty
    # Return 1 if selectionList is a list of integers
    # Return 2 if selectionList is a list of lists of integers
    # Return 3 if selectionList is a list of lists of lists of integers
    # ...
    # In general, return n if selectionList is a list of n-tuples of integers

    if isinstance(selectionList,list):
        if len(selectionList) == 0:
            return 0
    else:
        logger.error(f"[ProcessSelections] Selection list \"{selectionList}\" is not correct. Only lists are allowed")

    if isinstance(selectionList[0],int) or isinstance(selectionList[0],list):
        if isinstance(selectionList[0],int):
            return 1
        elif isinstance(selectionList[0],list):
            return 1 + selectionListType(selectionList[0])
    else:
        logger.error(f"[ProcessSelections] Selection list \"{selectionList}\" is not correct. Only lists of integers are allowed")
        raise Exception("Selection list is not correct")

def extractDeepestParentheses(tokens):

    logger = logging.getLogger("VLMP")

    maxDepth     = 0
    currentDepth = 0

    for tk in tokens:
        if tk == '(':
            currentDepth += 1
            if currentDepth > maxDepth:
                maxDepth = currentDepth
        elif tk == ')':
            currentDepth -= 1

    if currentDepth != 0:
        logger.error("[ExtractDeepestParentheses] Parentheses are not balanced")
        raise Exception("Parentheses are not balanced")

    currentDepth = 0

    deepestStart = -1
    deepestEnd   = -1

    for i, tk in enumerate(tokens):
        if tk == '(':
            currentDepth += 1
            if currentDepth == maxDepth:
                deepestStart = i
        elif tk == ')':
            if currentDepth == maxDepth:
                deepestEnd = i
                break
            currentDepth -= 1

    if deepestStart != -1 and deepestEnd != -1:
        return tokens[deepestStart:deepestEnd+1], deepestStart, deepestEnd

    return None, -1, -1

def evaluateTokens(tokens,allIds):

    logger = logging.getLogger("VLMP")

    logger.debug(f"[EvaluateTokens] Evaluating tokens: {tokens}")

    evalTokens = []
    if tokens[0] == "(" and tokens[-1] == ")":
        evalTokens = tokens[1:-1]
    else:
        evalTokens = tokens

    if len(evalTokens) == 1:
        return evalTokens[0]

    # Apply global not modifier if present
    for i in range(len(evalTokens)-1):
        if evalTokens[i] == "not":
            if not isinstance(evalTokens[i+1],list):
                logger.error(f"[EvaluateTokens] \"not\" modifier is not valid for token \"{evalTokens[i+1]}\"")
                raise Exception("Selection syntax error")
            if selectionListType(evalTokens[i+1]) != 1:
                logger.error(f"[EvaluateTokens] \"not\" modifier is only valid for particle selections (no pairs, triples, ...)")
                raise Exception("Selection syntax error")
            evalTokens[i+1] = list(set(allIds).difference(set(evalTokens[i+1])))
    # Remove not modifiers
    evalTokens = [tk for tk in evalTokens if tk != "not"]

    if len(evalTokens) == 1:
        return evalTokens[0]

    if len(evalTokens) > 3:
        logger.error(f"[EvaluateTokens] Logical expression \"{evalTokens}\" is not correct, too many tokens")
        raise Exception("Logical expression is not correct")
    else:
        op1 = evalTokens[0]
        op2 = evalTokens[2]
        op  = evalTokens[1]

        if op == "and":
            return list(set(op1).intersection(set(op2)))
        elif op == "or":
            return list(set(op1).union(set(op2)))
        else:
            logger.error(f"[EvaluateTokens] Operator \"{op}\" is not valid")
            raise Exception("Operator is not valid")

    logger.error(f"[EvaluateTokens] Tokens are not correct, the following tokens are not valid: {tokens}")
    raise Exception("Tokens are not correct")

def getAllIds(models):
    allIds = [mdl.getGlobalIds() for mdl in models]
    # Convert list of lists to a single list
    allIds = [i for sublist in allIds for i in sublist]

    return allIds

def processSelections(models,selections):

    logger = logging.getLogger("VLMP")

    specialSelections = ["all","none"]
    modifiers         = ["not"]
    logicalOperators  = ["and","or","(",")"]

    availableModels     = {mdl.getName():mdl for mdl in models}
    availableSelections = {mdl.getName():mdl.definedSelections for mdl in models}

    # Buffering for allIds
    allIds = None

    #Statr selection processing
    processedSelections = {}
    for sel,expr in selections.items():

        if sel in processedSelections.keys():
            logger.error(f"[ProcessSelections] Selection \"{sel}\" already processed")
            raise Exception("Selection already processed")
        else:
            processedSelections[sel] = []

        procExpr = expr
        procExpr = procExpr.replace("("," ( ")
        procExpr = procExpr.replace(")"," ) ")

        tokens = procExpr.split()
        procTokens = []
        ignoreTokens = 0
        for tk in tokens:
            tk = tk.strip()
            if ignoreTokens > 0:
                ignoreTokens -= 1
                continue
            if tk in logicalOperators or tk in modifiers:
                procTokens.append(tk)
            elif tk in specialSelections:
                if tk == "all":
                    if allIds is None:
                        allIds = getAllIds(models)
                    procTokens.append(allIds)
                elif tk == "none":
                    procTokens.append([])
            elif tk in availableModels.keys():

                try:
                    # Get all next tokens which are not logical operators nor special selections
                    currentModelSelection = []
                    for i in range(tokens.index(tk)+1,len(tokens)):
                        if tokens[i] in logicalOperators or tokens[i] in specialSelections:
                            break
                        else:
                            currentModelSelection.append(tokens[i])

                    if len(currentModelSelection) == 0:
                        # All model
                        procTokens.append(availableModels[tk].getGlobalIds())
                        continue

                    ignoreTokens = len(currentModelSelection)

                    isModified = (currentModelSelection[0].strip() in modifiers)
                    if isModified:
                        modifier = currentModelSelection[0].strip()
                        selectionType    = currentModelSelection[1]
                        selectionOptions = currentModelSelection[2:]
                    else:
                        selectionType    = currentModelSelection[0]
                        selectionOptions = currentModelSelection[1:]

                    if selectionType not in availableSelections[tk] and selectionType not in availableCommonSelections:
                        logger.error(f"[ProcessSelections] Neither model \"{tk}\" nor common selections have selection \"{selectionType}\"")
                        raise Exception("Selection not recognized")

                    selectionOptions = " ".join(selectionOptions)

                    if selectionType in availableCommonSelections and selectionType not in availableSelections[tk]:
                        ids = processCommonSelection(availableModels[tk],selectionType,selectionOptions,applyOffset=False)
                        # Offset is applied after
                    else:
                        if selectionType in availableCommonSelections:
                            logger.debug(f"[ProcessSelections] Model \"{tk}\" is overriding common selection \"{selectionType}\"")
                        ids = availableModels[tk].processSelection(selectionType,selectionOptions)

                    if ids is None:
                        logger.error(f"[ProcessSelections] Model \"{tk}\" does not process selection \"{selectionType}\" with options \"{selectionOptions}\"")
                        raise Exception("Selection not recognized")

                    #Apply offset
                    listType = selectionListType(ids)
                    if listType == 1:
                        ids = [i+availableModels[tk].getIdOffset() for i in ids]
                    else:
                        for i in range(len(ids)):
                            ids[i] = [j+availableModels[tk].getIdOffset() for j in ids[i]]

                    if isModified:
                        if modifier == "not":
                            #Not modifier only works for listType 1
                            if listType != 1:
                                logger.error(f"[ProcessSelections] Modifier \"{modifier}\" only works for particle selections (no pairs, triples, ...)")
                                raise Exception("Selection syntax error")
                            ids = list(set(availableModels[tk].getGlobalIds()).difference(set(ids)))
                        else:
                            logger.error(f"[ProcessSelections] Modifier \"{modifier}\" is not recognized")
                            raise Exception("Selection syntax error")

                    procTokens.append(ids)
                except Exception as e:
                    failedSelection = tk + " " + " ".join(currentModelSelection)
                    logger.error(f"[ProcessSelections] Selection \"{sel}\" has a syntax error. Error processing model selection \"{failedSelection}\"")
                    raise Exception("Selection syntax error")
            else:
                logger.error(f"[ProcessSelections] Selection \"{sel}\" refers to an unknown model \"{tk}\"")
                raise Exception("Model not recognized")

        # At this point, procTokens is a list of lists and logical operators
        # We check here if all list are the same type
        # Lists can be a list of integers: [1,2,3,4,...]
        # List of pairs of integers: [[1,2],[3,4],...]
        # List of triples of integers: [[1,2,3],[4,5,6],...]
        # ...
        # In general, a list of n-tuples of integers
        # But all lists must have the same type

        listType = -1
        for i in range(len(procTokens)):
            if procTokens[i] in logicalOperators or procTokens[i] in modifiers:
                continue
            else:
                if listType == -1:
                    listType = selectionListType(procTokens[i])
                elif listType != selectionListType(procTokens[i]):
                    logger.error(f"[ProcessSelections] Selection \"{sel}\" has different types of lists")
                    raise Exception("Selection has different types of lists")

        # If not is present we preprer the list of all ids
        for i in range(len(procTokens)):
            if procTokens[i] == "not":
                if allIds is None:
                    allIds = getAllIds(models)
                    break

        try:
            while len(procTokens) > 1:
                toProcess, start, end = extractDeepestParentheses(procTokens)
                if toProcess is None:
                    # Full expression is processed
                    toProcess = copy.deepcopy(procTokens)
                    start = 0
                    end   = len(procTokens)-1
                processed = evaluateTokens(toProcess,allIds)
                # Replace tokens
                procTokens = procTokens[:start] + [processed] + procTokens[end+1:]
        except Exception as e:
            logger.error(f"[ProcessSelections] Selection \"{sel}\" has a syntax error")
            raise Exception("Selection syntax error")

        # Clean up
        procTokens = procTokens[0]
        if selectionListType(procTokens) == 1:
            procTokens = list(set(procTokens))
        else:
            # Sort every sublist and convert to tuple
            for i in range(len(procTokens)):
                procTokens[i] = tuple(sorted(procTokens[i]))
            # Remove duplicates
            procTokens = list(set(procTokens))
            # Convert back to list
            for i in range(len(procTokens)):
                procTokens[i] = list(procTokens[i])


        processedSelections[sel] = procTokens
        logger.debug(f"[ProcessSelections] Selection \"{sel}\" processed: {processedSelections[sel]}")

    return copy.deepcopy(processedSelections)

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



