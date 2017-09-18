from Automaton import *

globalProperties = {"nodes": [], "transitions": {}, "isDfa": True, "isPda": False, "isTuring": False, "nodeCount": 0, "fileURL":""}


def createTransition(origin, destination, transitionName):
    values = globalProperties["transitions"].get(origin, {})
    if transitionName in values and not globalProperties["isDfa"]:
        vals = values[transitionName]
        if destination not in values[transitionName]:
            newVals = [destination]
            newVals.extend(vals)
            values[transitionName] = newVals
        else:
            return False
    else:
        values[transitionName] = [destination]
    globalProperties["transitions"][origin] = values
    return True

def deleteTransition(origin, destination, transitionName):
    try:
        if transitionName == "":
            for trans, _ in globalProperties["transitions"][origin].items():
                globalProperties["transitions"][origin][trans] = [x for x in globalProperties["transitions"][origin][trans] if (destination not in x if (type(x) == tuple and type(destination) == str) else destination != x)]
                globalProperties["transitions"][origin] = dict((x, v) for x, v in globalProperties["transitions"][origin].items() if v)
        elif destination == "":
            globalProperties["transitions"][origin] = dict((key, value) for key, value in globalProperties["transitions"][origin] if value and (transitionName not in key if (type(key) == tuple and type(transitionName) == str) else transitionName != key))
        elif origin == "":
            for orig, _ in globalProperties["transitions"].items():
                globalProperties["transitions"][orig][transitionName] = [x for x in globalProperties["transitions"][orig][transitionName] if (destination not in x if (type(x) == tuple and type(destination) == str) else destination != x)]
                globalProperties["transitions"][orig] = dict((x, v) for x, v in globalProperties["transitions"][orig].items() if v)
        else:
            if destination not in globalProperties["transitions"][origin][transitionName]:
                return False
            globalProperties["transitions"][origin][transitionName] = [x for x in globalProperties["transitions"][origin][transitionName] if (destination not in x if (type(x) == tuple and type(destination) == str) else destination != x)]
            globalProperties["transitions"][origin] = dict((x, v) for x, v in globalProperties["transitions"][origin].items() if v)
        globalProperties["transitions"] = dict((x, v) for x, v in globalProperties["transitions"].items() if v)
        return True
    except Exception:
        return False

def modifyTransition(origin, destination, transitionName, newText, toModify):
    newInfo = {"origin": origin, "destination": destination, "transitionName": transitionName}
    deleteTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"])
    newInfo[toModify] = newText
    createTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"])

def reduceTransitions():
    toReturn = {}
    for origin, transitionDict in globalProperties["transitions"].items():
        toReturn[origin] = {}
        for transitionName, destinations in transitionDict.items():
            for destination in destinations:
                if globalProperties["isPda"]:
                    try:
                        transitionList = ['/'.join([','.join(transitionName), destination[1] if type(destination[1]) != list else destination[1][0] ])]
                    except Exception as e:
                        pass
                elif globalProperties["isTuring"]:
                    try:
                        transitionList = ['/'.join([transitionName, destination[1], destination[2]])]
                    except Exception as e:
                        pass
                else:
                    transitionList = [transitionName]
                for tn, dts in transitionDict.items():
                    if tn == transitionName and not (globalProperties["isPda"] or globalProperties["isTuring"]):
                        continue
                    for dt in dts:
                        if globalProperties["isPda"]:
                            if (dt[0] == destination[0] and dt[1] != destination[1]) or (dt == destination and tn != transitionName):
                                transitionList.append('/'.join([','.join(tn), dt[1] if type(dt[1]) != list else dt[1][0]]))
                        elif globalProperties["isTuring"]:
                            if (dt[0] == destination[0] and ((dt[1] != destination[1]) or dt[2] != destination[2])) or (dt == destination and tn != transitionName):
                                transitionList.append('/'.join([tn, dt[1], dt[2]]))
                        else:
                            if dt == destination:
                                transitionList.append(tn)
                transitionList.sort()
                newTransitionName = '|'.join(transitionList)
                values = toReturn[origin].get(newTransitionName, [])
                values.append(destination)
                toReturn[origin][newTransitionName] = values
    return toReturn

def polishGrammar(grammar):
    toReturn = []
    for el in grammar:
        toReturn.append('->'.join([el[0], ' '.join(el[1])]))
    return '\n'.join(toReturn)