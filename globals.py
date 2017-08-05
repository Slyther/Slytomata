globalProperties = {"nodes": [], "transitions": {}, "isDfa": True, "nodeCount": 0, "fileURL":""}


def createTransition(origin, destination, transitionName):
    values = globalProperties["transitions"].get(origin, {})
    if transitionName in values and not globalProperties["isDfa"]:
        vals = values[transitionName]
        if destination not in values[transitionName]:
            newVals = [destination]
            newVals.extend(vals)
            values[transitionName] = newVals
    else:
        values[transitionName] = [destination]
    globalProperties["transitions"][origin] = values

def deleteTransition(origin, destination, transitionName):
    try:
        if transitionName == "":
            for trans, _ in globalProperties["transitions"][origin].items():
                globalProperties["transitions"][origin][trans] = [x for x in globalProperties["transitions"][origin][trans] if x != destination]
                globalProperties["transitions"][origin] = dict((x, v) for x, v in globalProperties["transitions"][origin].items() if v)
        elif destination == "":
            globalProperties["transitions"][origin] = dict((key, value) for key, value in globalProperties["transitions"][origin] if value and transitionName != key)
        elif origin == "":
            for orig, _ in globalProperties["transitions"].items():
                globalProperties["transitions"][orig][transitionName] = [x for x in globalProperties["transitions"][orig][transitionName] if x != destination]
                globalProperties["transitions"][orig] = dict((x, v) for x, v in globalProperties["transitions"][orig].items() if v)
        else:
            globalProperties["transitions"][origin][transitionName] = [x for x in globalProperties["transitions"][origin][transitionName] if x != destination]
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
