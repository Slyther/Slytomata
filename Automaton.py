class Dfa:
    def __init__(self, start, finals, transitions):
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def evaluate(self, word):
        current = self.start
        for c in word:
            try:
                current = self.transitions[current][c][0]
            except Exception:
                return False
        return current in self.finals

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

class Nfa:
    def __init__(self, start, finals, transitions):
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def evaluate(self, word):
        current = [self.start]
        for c in word:
            try:
                current = self.evaluateSub(current, c)
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
            result.append(origin)
            for _, destinies in transitions.items():
                result.extend(destinies)
        return result

    def getAlphabet(self):
        alphabet = []
        for transition in self.transitions.values():
            for symbol in transition:
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
        return Dfa(self.start, new_finals, new_transitions)

    def superset(self, states):
        from itertools import chain, combinations
        s = list(states)
        return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))