import random, string, copy
class Automaton:
    def __init__(self, start, finals, transitions):
        self.start = start
        self.finals = finals
        self.transitions = transitions
 
    def get_states(self):
        result = []
        for origin, transitions in self.transitions.items():
            if origin not in result:
                result.append(origin)
            for _, destinies in transitions.items():
                for destiny in destinies:
                    if type(destiny) != tuple and destiny not in result:
                        result.append(destiny)
                    elif type(destiny) == tuple and destiny[0] not in result:
                        result.append(destiny[0])
        if self.start not in result and self.start != None:
            result.append(self.start)
        return result

    def getAlphabet(self):
        alphabet = []
        for transition in self.transitions.values():
            for symbol in transition:
                if type(symbol) != tuple and symbol != "$":
                    alphabet.append(symbol)
                elif type(symbol) == tuple and symbol[1] != "$":
                    alphabet.append(symbol[1])
        return alphabet

    def createTransition(self, origin, destination, transitionName, isDfa=False):
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

class Nfa(Automaton):
    def __init__(self, start, finals, transitions):
        super().__init__(start, finals, transitions)

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

    def to_regex(self):
        states = self.get_states()
        alphabet = self.getAlphabet()
        B = [""] * len(states)
        for i in range(0, len(states)):
            if states[i] in self.finals:
                B[i] = "$"
        A = [[""]*len(states)] * len(states)
        for i in range(0, len(states)):
            for j in range(0, len(states)):
                for letter in alphabet:
                    if(states[j] in self.transitions.get(states[i], {}).get(letter, [])):
                        A[i][j] = letter
        print(B)
        for n in range(len(states)-1, -1, -1):
            if B[n]:
                B[n] = "(" + A[n][n] + ")*" + B[n]
            for j in range(0, n):
                if A[n][j]:
                    A[n][j] = "(" + A[n][n] + ")*" + A[n][j]
            for i in range(0, n):
                if B[i]:
                    B[i] = B[i] + "+" + A[i][n] + B[n]
                else:
                     B[i] = A[i][n] + B[n]
                for j in range(0, n):
                    if A[i][j]:
                        A[i][j] = A[i][j] + "+" + A[i][n] + A[n][j]
                    else:
                        A[i][j] = A[i][n] + A[n][j]
        print(B)
        print("-------")
        print(A)
        return B[0].replace("()*", "").replace("()", "")

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
        toReturn = with_deadend_state(self)
        toReturn = toReturn.minimized_internal()
        for state in toReturn.get_states():
            toReturn.deleteTransition("Deadend", state, "")
            toReturn.deleteTransition(state, "Deadend", "")
        return toReturn

    def minimized_internal(self):
        states = self.get_states()
        alphabet = self.getAlphabet()
        equivalence_table = {}

        for stateX in states:
            equivalence_table[stateX] = {}
            for stateY in states:
                if stateX == stateY:
                    equivalence_table[stateX][stateY] = False
                elif (stateX in self.finals and stateY not in self.finals) or (stateY in self.finals and stateX not in self.finals):
                    equivalence_table[stateX][stateY] = True
                else:
                    equivalence_table[stateX][stateY] = None
        restart = True
        while restart:
            restart = False
            for stateX in states:
                for stateY in states:
                    if (equivalence_table[stateX][stateY] == None) or (equivalence_table[stateY][stateX] == None):
                        for letter in alphabet:
                            try:
                                if (equivalence_table[self.transitions[stateX][letter][0]][self.transitions[stateY][letter][0]] == True) or (equivalence_table[self.transitions[stateY][letter][0]][self.transitions[stateX][letter][0]] == True):
                                    equivalence_table[stateX][stateY] = True
                                    equivalence_table[stateY][stateX] = True
                                    restart = True
                                    break
                            except Exception:
                                pass
                        if restart:
                            break
                if restart:
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
        for state in states:
            if not any(v == None for k, v in equivalence_table[state].items()):
                joined_states.append(state)
        toReturn = Nfa(self.start, [], {})
        for joined in joined_states:
            for letter in alphabet:
                destinations = self.evaluateSub(joined, letter) if type(joined) != str else self.transitions.get(joined, {}).get(letter, [])
                for destination in destinations:
                    someRandomBool = True
                    for joined_sub in joined_states:
                        if destination in joined_sub:
                            toReturn.createTransition(''.join(joined), ''.join(joined_sub), letter, True)
                            someRandomBool = False
                            break
                    if someRandomBool:
                        toReturn.createTransition(''.join(joined), destination, letter, True)
        for final in self.finals:
            for joined in joined_states:
                if final in joined and ''.join(joined) not in toReturn.finals:
                    toReturn.finals.append(''.join(joined))
        for joined in joined_states:
            if self.start in joined:
                toReturn.start = ''.join(joined)
        return toReturn

class Pushdown(Automaton):
    def __init__(self, start, finals, transitions):
        super().__init__(start, finals, transitions)

    def evaluate(self, word, stack_start='Z', method="empty"):
        return self._evaluate(word, [stack_start], self.start, method, word)

    def _evaluate(self, word, stack, current, method="empty", originalWord=""):
        if not word and ((method == 'empty' and not stack) or (method == 'not empty' and current in self.finals)):
            return True
        word_input = '$'
        try:
            word_input = next(iter(word))
        except StopIteration:
            pass
        try:
            exits = self.transitions[current][(stack[-1], word_input)] if stack else []
        except KeyError as e:
            exits = []
            pass
        altered_word = '' if word_input == '$' else word[1:]
        for destiny, push in exits:
            altered_stack = stack[:-1]
            altered_stack.extend(reversed(push))
            if len(originalWord) >= len(altered_stack) and  self._evaluate(altered_word, altered_stack, destiny, method, originalWord):
                return True
        try:
            exits = self.transitions[current][(stack[-1], "$")] if stack else []
        except KeyError as e:
            exits = []
            pass
        for destiny, push in exits:
            altered_stack = stack[:-1]
            altered_stack.extend(reversed(push))
            if len(originalWord) >= len(altered_stack) and self._evaluate(word, altered_stack, destiny, method, originalWord):
                return True
        return False

    def get_tupled_transitions(self):
        tupled_transitions = []
        for origin, transitionDict in self.transitions.items():
            for transitionTuple, destinations in transitionDict.items():
                for destination in destinations:
                    tupled_transitions.append((origin, transitionTuple[0], transitionTuple[1], destination[0], destination[1]))
        return tupled_transitions

    def grammar(self, method="empty"):
        grammars = []
        if method == 'empty':
            s1States = self.get_states()
        else:
            s1States = self.finals
        for state in s1States:
            newInput = self.start + 'Z' + state
            grammars.append(('Z', [newInput]))
        for (start, pop, value, destiny, push) in self.get_tupled_transitions():
            if push == '':
                grammars.append((start + pop + destiny, [value]))
        import itertools
        for (start, pop, value, destiny, push) in self.get_tupled_transitions():
            if not push:
                continue
            table =  itertools.product(self.get_states(), repeat=len(push))
            for tuple_ in table:
                toAdd_str = ""
                toAdd_list = []
                toAdd_str = ('' + start + pop + str(tuple_[len(push)-1]))
                if value != '$':
                    toAdd_list.append(value)
                toAdd_list.append(destiny + push[0] + str(tuple_[0]))
                for i in range(0, len(push)-1):
                    toAdd_list.append(str(tuple_[i]) + push[i+1] + str(tuple_[i+1]))
                grammars.append((toAdd_str, toAdd_list))
        return grammars

class Turing(Automaton):
    def __init__(self, start, finals, transitions):
        super().__init__(start, finals, transitions)

    def evaluate(self, tape):
        tapeDict = {}
        for i, item in enumerate(tape):
            tapeDict[i] = item
        current = self.start
        pointer = 0
        while current:
            if current in self.finals:
                return (True, tape)
            pop = tapeDict.get(pointer, 'B')
            (destiny, push, direction) = next(iter(self.transitions.get(current, {}).get(pop, [(None, None, None)])))
            if destiny != None:
                tapeDict[pointer] = push
                if direction == 'R':
                    pointer += 1
                elif direction == 'L':
                    pointer -= 1
            current = destiny
        return (False, None)

def from_grammar(grammar):
    passvariables = [g[0] for g in grammar]
    start = 'q'
    finals = [start]
    transitions = {start: {}}
    for variable, prod in grammar:
        existing = transitions[start].get((variable, '$'), [])
        if (start, prod) not in existing:
            existing.append((start, prod))
        transitions[start][(variable, '$')] = existing
        for p in prod:
            if p not in passvariables:
                existing = transitions[start].get((p, p), [])
                if (start, '') not in existing:
                    existing.append((start, ''))
                transitions[start][(p, p)] = existing
    return Pushdown(start, finals, transitions)

def from_regex(regex):
    regex = regex.replace(" ", "")
    if regex.count('(') != regex.count(')'):
        return None
    valid = "+.()*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$ "
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

def with_deadend_state(automaton):
    alphabet = automaton.getAlphabet()
    states = automaton.get_states()
    toReturn = Nfa(automaton.start, copy.deepcopy(automaton.finals), copy.deepcopy(automaton.transitions))
    has_deadend = False
    for state in states:
        for letter in alphabet:
            if not automaton.transitions.get(state, {}).get(letter, []):
                has_deadend = True
                toReturn.createTransition(state, "Deadend", letter, False)
    if has_deadend:
        for letter in alphabet:
            toReturn.createTransition("Deadend", "Deadend", letter, False)
    return toReturn

# testPda = Pushdown("Q0", ["Q2"], {})
# origin, (destination, push), (pop, value)
# testPda.createTransition("Q0", ("Q0", "0Z"), ("Z", "0"))
# testPda.createTransition("Q0", ("Q0", "1Z"), ("Z", "1"))
# testPda.createTransition("Q0", ("Q0", "00"), ("0", "0"))
# testPda.createTransition("Q0", ("Q0", "01"), ("1", "0"))
# testPda.createTransition("Q0", ("Q0", "10"), ("0", "1"))
# testPda.createTransition("Q0", ("Q0", "11"), ("1", "1"))
# testPda.createTransition("Q0", ("Q1", "Z"), ("Z", "$"))
# testPda.createTransition("Q0", ("Q1", "0"), ("0", "$"))
# testPda.createTransition("Q0", ("Q1", "1"), ("1", "$"))
# testPda.createTransition("Q1", ("Q1", ""), ("1", "1"))
# testPda.createTransition("Q1", ("Q1", ""), ("0", "0"))
# testPda.createTransition("Q1", ("Q2", "Z"), ("Z", "$"))

# testPda = Pushdown("q", ["r"], {})
# testPda.createTransition("q", ("q", "XX"), ("X", "0"))
# testPda.createTransition("q", ("q", "XZ"), ("Z", "0"))
# testPda.createTransition("q", ("r", ""), ("X", "1"))
# testPda.createTransition("r", ("r", ""), ("X", "1"))
# testPda.createTransition("r", ("r", ""), ("Z", "$"))
# grammar = testPda.grammar()
# for el in grammar:
#     print(el)
# print("---------")
# for tuple_ in testPda.get_tupled_transitions():
#     print(tuple_)
# fromgrammar = from_grammar(grammar)
# print("---------")
# for tuple_ in fromgrammar.get_tupled_transitions():
#     print(tuple_)
# print("---------")
# sgrammar = fromgrammar.grammar()
# for el in sgrammar:
#     print(el)
# print(testPda.evaluate("0011"))
# print(fromgrammar.evaluate("0011"))

grammar = [
    ("Z", ["Z", "+", "T"]),
    ("Z", ["Z", "-", "T"]),
    ("Z", ["T"]),
    ("T", ["F"]),
    ("F", ["digit"]),
    ("digit", ["0"]),
    ("digit", ["1"])
]

# pdanew = from_grammar(grammar)
# for tuple_ in pdanew.get_tupled_transitions():
#      print(tuple_)
# print(pdanew.evaluate("1+1+1/0/0*1*1-0+1-0-1-1-1-1-1"))