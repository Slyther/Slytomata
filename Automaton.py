import random, string, copy
class Nfa:
    def __init__(self, start, finals, transitions):
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def createTransition(self, origin, destination, transitionName, isDfa):
        values = self.transitions.get(origin, {})
        if transitionName in values and not isDfa:
            vals = values[transitionName]
            if destination not in values[transitionName]:
                newVals = [destination]
                newVals.extend(vals)
                values[transitionName] = newVals
            else:
                return False
        else:
            values[transitionName] = [destination]
        self.transitions[origin] = values
        return True

    def deleteTransition(self, origin, destination, transitionName):
        try:
            if transitionName == "":
                for trans, _ in self.transitions[origin].items():
                    self.transitions[origin][trans] = [x for x in self.transitions[origin][trans] if x != destination]
                    self.transitions[origin] = dict((x, v) for x, v in self.transitions[origin].items() if v)
            elif destination == "":
                self.transitions[origin] = dict((key, value) for key, value in self.transitions[origin] if value and transitionName != key)
            elif origin == "":
                for orig, _ in self.transitions.items():
                    self.transitions[orig][transitionName] = [x for x in self.transitions[orig][transitionName] if x != destination]
                    self.transitions[orig] = dict((x, v) for x, v in self.transitions[orig].items() if v)
            else:
                if destination not in self.transitions[origin][transitionName]:
                    return False
                self.transitions[origin][transitionName] = [x for x in self.transitions[origin][transitionName] if x != destination]
                self.transitions[origin] = dict((x, v) for x, v in self.transitions[origin].items() if v)
            self.transitions = dict((x, v) for x, v in self.transitions.items() if v)
            return True
        except Exception:
            return False

    def modifyTransition(self, origin, destination, transitionName, newText, toModify):
        newInfo = {"origin": origin, "destination": destination, "transitionName": transitionName}
        self.deleteTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"])
        newInfo[toModify] = newText
        self.createTransition(newInfo["origin"], newInfo["destination"], newInfo["transitionName"], False)

    def reduceTransitions(self):
        toReturn = {}
        for origin, transitionDict in self.transitions.items():
            toReturn[origin] = {}
            for transitionName, destinations in transitionDict.items():
                for destination in destinations:
                    transitionList = [transitionName]
                    for tn, dts in transitionDict.items():
                        if tn == transitionName:
                            continue
                        for dt in dts:
                            if dt == destination:
                                transitionList.append(tn)
                    transitionList.sort()
                    newTransitionName = '|'.join(transitionList)
                    values = toReturn[origin].get(newTransitionName, [])
                    values.append(destination)
                    toReturn[origin][newTransitionName] = values
        return toReturn

    def emptyMoves(self, states):
        temp = list(states)
        exits = list(states)
        while temp:
            current = temp.pop()
            next_exits = self.evaluateSub([current], "$")
            temp.extend(state for state in next_exits if state not in exits)
            exits.extend(state for state in next_exits if state not in exits)
        return exits

    def evaluate(self, word):
        current = self.emptyMoves([self.start])
        for c in word:
            try:
                current = self.emptyMoves(self.evaluateSub(current, c))
            except Exception:
                return False
        for curr in current:
            if curr in self.finals:
                return True
        return False

    def evaluateSub(self, statesList, c):
        result = []
        for state in statesList:
            try:
                result.extend(destiny for destiny in self.transitions[state][c] if destiny not in result)
            except KeyError:
                pass
        return result

    def get_states(self):
        result = []
        for origin, transitions in self.transitions.items():
            if origin not in result:
                result.append(origin)
            for _, destinies in transitions.items():
                for destiny in destinies:
                    if destiny not in result:
                        result.append(destiny)
        return result

    def getAlphabet(self):
        alphabet = []
        for transition in self.transitions.values():
            for symbol in transition:
                if symbol != "$":
                    alphabet.append(symbol)
        return alphabet

    def as_dfa(self):
        alphabet = self.getAlphabet()
        state_table = self.superset(self.get_states())
        new_transitions = {}
        new_finals = set()
        for state_set in state_table:
            state_set_str = ''.join(sorted(state_set))
            new_transitions[state_set_str] = {}
            if any(state in self.finals for state in state_set):
                new_finals.add(state_set_str)
            for symbol in alphabet:
                destinies = self.evaluateSub(state_set, symbol)
                new_transitions[state_set_str][symbol] = [''.join(sorted(destinies))]
        return Nfa(self.start, new_finals, new_transitions)

    def clearing_epsilon(self):
        start = self.emptyMoves([self.start])
        states = [start]
        temp = list(states)
        transitions = {}
        finals = []
        for state in start:
            if state in self.finals:
                finals.append(''.join(str(e) for e in sorted(start)))
                break
        while temp:
            current_set = temp.pop()
            if len(current_set) == 0:
                continue
            transitions[''.join(str(e) for e in sorted(current_set))] = {}
            for symbol in self.getAlphabet():
                new_set = self.emptyMoves(self.evaluateSub(current_set, symbol))
                if len(new_set) == 0:
                    continue
                transitions[''.join(str(e) for e in sorted(current_set))][symbol] = [''.join(str(e) for e in sorted(new_set))]
                for state in new_set:
                    if state in self.finals:
                        new_set_str = ''.join(str(e) for e in sorted(new_set))
                        if new_set_str not in finals:
                            finals.append(new_set_str)
                        break
                if new_set not in states:
                    states.append(new_set)
                    temp.append(new_set)
        return Nfa(''.join(str(e) for e in sorted(start)), finals, transitions)

    def superset(self, states):
        from itertools import chain, combinations
        s = list(states)
        return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    def regex(self):
        initial = object()
        final = object()
        expr = {}
        states = [initial, final]
        states.extend(self.get_states())
        for x in states:
            for y in states:
                expr[x, y] = None
        for x in self.get_states():
            if x == self.start:
                expr[initial, x] = ''
            if x in self.finals:
                expr[x, final] = ''
            expr[x, x] = ''
        for x in self.get_states():
            for c in self.getAlphabet():
                for y in self.transitions.get(x, {}).get(c, []):
                    if expr[x, y]:
                        expr[x, y] += '+' + str(c)
                    else:
                        expr[x, y] = str(c)

        for s in self.get_states():
            states.remove(s)
            for x in states:
                for y in states:
                    if expr[x, s] is not None and expr[s, y] is not None:
                        xsy = []
                        if expr[x, s]:
                            xsy += self._add_parentheses(expr[x, s])
                        if expr[s, s]:
                            xsy += self._add_parentheses(expr[s, s], True) + ['*']
                        if expr[s, y]:
                            xsy += self._add_parentheses(expr[s, y])
                        if expr[x, y] is not None:
                            xsy += ['+', expr[x, y] or '()']
                        expr[x, y] = ''.join(xsy)
        return expr[initial, final]

    def _add_parentheses(self, expr, starring=False):
        if len(expr) == 1 or (not starring and '+' not in expr):
            return [expr]
        elif starring and expr.endswith('+()'):
            return ['(', expr[:-3], ')']
        else:
            return ['(', expr, ')']
    
    def standardized(self):
        self.clear_conflicts([])
        states = self.get_states()
        for i, state in enumerate(states):
            new_name = "Q"+str(i)
            self.modify_state_name(state, new_name)
        return self

    def clear_conflicts(self, second_states):
        for state in self.get_states():
            new_name = state
            while new_name in self.get_states() or new_name in second_states:
                new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.modify_state_name(state, new_name)

    def modify_state_name(self, state, new_name):
        if state == self.start:
            self.start = new_name
        if state in self.finals:
            self.finals = [st for st in self.finals if st != state]
            self.finals.append(new_name)
        for origin, transitionDict in self.transitions.items():
            for transitionName, destinations in transitionDict.items():
                for destination in destinations:
                    if origin == state and destination == state:
                        self.modifyTransition(state, state, transitionName, new_name, "origin")
                        self.modifyTransition(new_name, state, transitionName, new_name, "destination")
                    elif origin == state:
                        self.modifyTransition(state, destination, transitionName, new_name, "origin")
                    elif destination == state:
                        self.modifyTransition(origin, state, transitionName, new_name, "destination")

    def complement(self):
        return Nfa(self.start, list(x for x in self.get_states() if x not in self.finals), copy.deepcopy(self.transitions))

    def difference(self, second):
        return self.intersection(second.complement())

    def intersection(self, second):
        return self.complement().union(second.complement()).complement()

    def union(self, second):
        return union_expression(self, second).clearing_epsilon()

    def reversal(self):
        if len(self.finals) > 1:
            self = with_final_epsilon(self)
        toReturn = Nfa(self.finals[0], self.start, {})
        for origin, transitionDict in self.transitions.items():
            for transitionName, destinations in transitionDict.items():
                for destination in destinations:
                    toReturn.createTransition(destination, origin, transitionName, False)
        return toReturn

    def minimized(self):
        states = self.get_states()
        alphabet = self.getAlphabet()
        equivalence_table = {}

        for stateX in states:
            equivalence_table[stateX] = {}
            for stateY in states:
                if (stateX in self.finals and stateY not in self.finals) or (stateY in self.finals and stateX not in self.finals) or (stateX == stateY):
                    equivalence_table[stateX][stateY] = True
                else:
                    equivalence_table[stateX][stateY] = None
        for i in range(0, 3):
            for stateX in states:
                for stateY in states:
                    if (equivalence_table[stateX][stateY] == None) or (equivalence_table[stateY][stateX] == None):
                        for letter in alphabet:
                            try:
                                if (equivalence_table[self.transitions[stateX][letter]][self.transitions[stateY][letter]] == True) or (equivalence_table[self.transitions[stateY][letter]][self.transitions[stateX][letter]] == True):
                                    equivalence_table[stateX][stateY] = True
                                    equivalence_table[stateY][stateX] = True
                                    break
                            except Exception:
                                pass
                        if (equivalence_table[stateX][stateY] == True) or (equivalence_table[stateY][stateX] == True):
                            i = -1
                            break
        joined_states = []
        for stateX in states:
            for stateY in states:
                if (equivalence_table[stateX][stateY] == None) or (equivalence_table[stateY][stateX] == None):
                    add = True
                    for st in joined_states:
                        if stateX in st or stateY in st:
                            if stateX not in st:
                                st.append(stateX)
                            if stateY not in st:
                                st.append(stateY)
                            add = False
                            break
                    if add:
                        joined_states.append([stateX, stateY])
        truly_joined = []
        toReturn = Nfa(self.start, [], {})
        for joined in joined_states:
            truly_joined.append(''.join(joined))
        for joined in joined_states:
            for letter in alphabet:
                for destination in self.evaluateSub(joined, letter):
                    someRandomBool = True
                    for truly in truly_joined:
                        if destination in truly:
                            toReturn.createTransition(''.join(joined), truly, letter, True)
                            someRandomBool = False
                            break
                    if someRandomBool:
                        toReturn.createTransition(''.join(joined), destination, letter, True)
        for final in self.finals:
            for joined in joined_states:
                if final in joined and ''.join(joined) not in toReturn.finals:
                    toReturn.finals.append(''.join(joined))
                if self.start in joined:
                    toReturn.start = joined
        return toReturn

def from_regex(regex):
    regex = regex.replace(" ", "")
    if regex.count('(') != regex.count(')'):
        return None
    valid = "+.()*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    for c in regex:
        if c not in valid:
            return None
    invalid = ['+*', '.+', '+.', '()', '+)', '(+', '.)', '.*', '.)', '++', '..', "**"]
    final_chars = "+.*"
    expressions = []
    for inv in invalid:
        if inv in regex:
            return None
    if "(" not in regex:
        if len(regex) == 1 and type(regex) == str:
            expressions.append(from_single_char(regex[0]))
        else:
            for x in regex:
                expressions.append(x)
    else:
        i = 0
        pos = 0
        it = 0
        while it < len(regex):
            if regex[it] == '(':
                if i == 0:
                    pos = it
                i += 1
            if regex[it] == ')':
                if i == 1:
                    subs = regex[pos+1: it]
                    expressions.append(regex.split("("+subs+")", 1)[0])
                    expressions.append(subs)
                    expressions.append(regex.split("("+subs+")", 1)[1])
                    break
                i -= 1
            it += 1
        expressions = [x for x in expressions if x != '' and x]
    it = 0
    while it < len(expressions):
        exp = expressions[it]
        if type(exp) == Nfa or exp in final_chars:
            it+=1
            continue
        newExp = expressions[:it]
        result = from_regex(exp)
        if type(result) == Nfa:
            newExp.append(result)
        else:
            newExp.extend(result)
        newExp.extend(expressions[it+1:])
        expressions = newExp
        it=0
    if len(expressions) == 1:
        return expressions[0]
    else:
        while len(expressions) > 1:
            if '*' in expressions:
                n = expressions.index('*')
                if(n == 0):
                    return expressions
                res = kleene_star_expression(expressions[n-1])
                del expressions[n]
                expressions[n-1] = res
            else:
                n = expressions[0]
                n2 = expressions[1]
                if type(n2) != Nfa and len(expressions) > 2:
                    n3 = expressions[2]
                    res = ""
                    if(n2 == '+'):
                        res = union_expression(n, n3)
                    elif(n2 == '.'):
                        res = concatenation_expression(n, n3)
                    del expressions[2]
                    del expressions[1]
                    expressions[0] = res
                    continue
                if type(n) != Nfa or type(n2) != Nfa:
                    return expressions
                res = concatenation_expression(n, n2)
                del expressions[1]
                expressions[0] = res
        return expressions[0].standardized()


def from_single_char(character):
    return Nfa("Q0", ["Q1"], {"Q0": {character: ["Q1"]}})

def union_expression(first, second):
    if len(first.finals) > 1:
        first = with_final_epsilon(first)
    if len(second.finals) > 1:
        second = with_final_epsilon(second)
    first.clear_conflicts(second.get_states())
    second.clear_conflicts(first.get_states())
    new_transitions = {}
    new_transitions.update(first.transitions)
    new_transitions.update(second.transitions)
    toReturn = Nfa("Ei", ["Ef"], new_transitions)
    toReturn.createTransition(first.finals[0], "Ef", "$", False)
    toReturn.createTransition(second.finals[0], "Ef", "$", False)
    toReturn.createTransition("Ei", first.start, "$", False)
    toReturn.createTransition("Ei", second.start, "$", False)
    return toReturn

def concatenation_expression(first, second):
    if len(first.finals) > 1:
        first = with_final_epsilon(first)
    if len(second.finals) > 1:
        second = with_final_epsilon(second)
    first.clear_conflicts(second.get_states())
    second.clear_conflicts(first.get_states())
    new_transitions = {}
    new_transitions.update(first.transitions)
    new_transitions.update(second.transitions)
    toReturn = Nfa(first.start, [second.finals[0]], new_transitions)
    toReturn.createTransition(first.finals[0], second.start, "$", False)
    return toReturn

def kleene_star_expression(automaton):
    if len(automaton.finals) > 1:
        automaton = with_final_epsilon(automaton)
    new_transitions = {}
    new_transitions.update(automaton.transitions)
    toReturn = Nfa("Ei", ["Ef"], new_transitions)
    toReturn.createTransition(automaton.finals[0], "Ef", "$", False)
    toReturn.createTransition(automaton.finals[0], automaton.start, "$", False)
    toReturn.createTransition("Ei", automaton.start, "$", False)
    toReturn.createTransition("Ei", "Ef", "$", False)
    return toReturn

def with_final_epsilon(automaton):
    new_transitions = {}
    new_transitions.update(automaton.transitions)
    toReturn = Nfa(automaton.start, ["Ef"], new_transitions)
    for final in automaton.finals:
        toReturn.createTransition(final, "Ef", "$", False)
    return toReturn
