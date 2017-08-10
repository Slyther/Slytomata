class Nfa:
    def __init__(self, start, finals, transitions):
        self.start = start
        self.finals = finals
        self.transitions = transitions

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
                print(current)
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
                finals.append(''.join(sorted(start)))
                break
        while temp:
            current_set = temp.pop()
            transitions[''.join(sorted(current_set))] = {}
            for symbol in self.getAlphabet():
                new_set = self.emptyMoves(self.evaluateSub(current_set, symbol))
                transitions[''.join(sorted(current_set))][symbol] = [''.join(sorted(new_set))]
                for state in new_set:
                    if state in self.finals:
                        new_set_str = ''.join(sorted(new_set))
                        if new_set_str not in finals:
                            finals.append(new_set_str)
                        break
                if new_set not in states:
                    states.append(new_set)
                    temp.append(new_set)
        return Nfa(''.join(sorted(start)), finals, transitions)

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

# A = buildAutomataER(DFA)
# er = ''
# for f in F:
#     estadosBorrar = getEstadosBorrar(f)
#     for estadoBorrar in estadosBorrar:
#         tabla = buildTabla(estadoBorrar)
#         del A[estadoBorrar]
#         for transicion in tabla:
#             A.append(transicion)
#         ERf = getERfromDFABase(A)
#         add ERf a er
#https://en.wikipedia.org/wiki/Glushkov's_construction_algorithm
