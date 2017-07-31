globalProperties = {"nodes": [], "transitions": {}, "isDfa": True, "nodeCount": 0, "fileURL":""}


def createTransition(origin, destination, transitionName):
    values = globalProperties["transitions"].get(origin.name, {})
    if transitionName in values and not globalProperties["isDfa"]:
        vals = values[transitionName]
        if destination.name not in values[transitionName]:
            newVals = [destination.name]
            newVals.extend(vals)
            values[transitionName] = newVals
    else:
        values[transitionName] = [destination.name]
    globalProperties["transitions"][origin.name] = values

def deleteTransition(origin, destination, transitionName_):
    values = globalProperties["transitions"].get(origin.name, {})
    if transitionName_ in values:
        for transitionName, destinations in values.items():
            if transitionName == transitionName_:
                for i, destin in enumerate(destinations):
                    if destin == destination.name:
                        del destinations[i]
                        foundTransition = True
                        if not destinations:
                            del values[transitionName]
                        return True
    return False