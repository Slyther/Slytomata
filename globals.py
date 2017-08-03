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
    if origin == "":
        for orig, transDict in globalProperties["transitions"].items():
            for trans, destList in transDict.items():
                for dest in destList:
                    if(trans == transitionName):
                        globalProperties["transitions"][orig][trans] = [x for x in globalProperties["transitions"][orig][trans] if not x == destination]
                        break
            globalProperties["transitions"][orig] = dict((x, v) for x, v in globalProperties["transitions"][orig].items() if v)
    elif destination == "":
        globalProperties["transitions"][origin] = dict((key, value) for key, value in globalProperties["transitions"][origin] if value and not transitionName == key)
    elif transitionName == "":
        for orig, transDict in globalProperties["transitions"].items():
            for trans, destList in transDict.items():
                for dest in destList:
                    globalProperties["transitions"][orig][trans] = [x for x in globalProperties["transitions"][orig][trans] if not x == destination]
            globalProperties["transitions"][orig] = dict((x, v) for x, v in globalProperties["transitions"][orig].items() if v)
    else:
        globalProperties["transitions"][origin][transitionName] = [x for x in globalProperties["transitions"][origin][transitionName] if not x == destination]
        globalProperties["transitions"][origin] = dict((x, v) for x, v in globalProperties["transitions"][origin].items() if v)
    globalProperties["transitions"] = dict((x, v) for x, v in globalProperties["transitions"].items() if v)
    return True

def modifyTransition(origin, destination, transitionName, newText, toModify):
    newInfo = {"origin": origin, "destination": destination, "transitionName": transitionName}
    deleteTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"])
    newInfo[toModify] = newText
    createTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"])