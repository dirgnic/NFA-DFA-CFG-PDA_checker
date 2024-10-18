#nfa - LAB3

import sys
from parser import parse_input_file

class DFA:
    def __init__(self, sigma, states, transitions, start_state, accept_states):
        self.sigma = sigma
        # dict states + trans
        self.states = {state: [] for state in states}
        self.transitions = {(trans[0], trans[1]): trans[2] for trans in transitions}
        # start state + accept states
        self.start_state = start_state
        self.accept_states = accept_states
        print(f"Start state: {self.start_state}")
        print(f"Accept states: {self.accept_states}")

    def accepts(self, input_string):
        current_state = self.start_state
        print(f"Initial state: {current_state}")
        for char in input_string:
            print(f"Current state: {current_state}, input: {char}")
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
                print(f"Transition to: {current_state}")
            else:
                print("No transition found")
                return False
        print(f"Final state: {current_state}")
        return current_state in self.accept_states

class NFA:
    def __init__(self, sigma, states, transitions):
        self.sigma = [symbol.strip() for symbol in sigma]
        self.states = {state[0].strip(): state[1:] for state in states if isinstance(state, tuple)}
        self.states.update({state.strip(): [] for state in states if not isinstance(state, tuple)})
        self.transitions = {}
        for trans in transitions:
            trans = tuple(t.strip() for t in trans)  # Strip each element in the transition tuple
            if len(trans) != 3:
                print(f"Invalid transition format: {trans}")
                continue
            if (trans[0], trans[1]) not in self.transitions:
                self.transitions[(trans[0], trans[1])] = []
            self.transitions[(trans[0], trans[1])].append(trans[2])
        self.start_state = next(state for state in states if isinstance(state, tuple) and "S" in state[1])[0].strip()
        self.accept_states = {state[0].strip() for state in states if isinstance(state, tuple) and "F" in state[1]}
        print(f"Initial accept states: {self.accept_states}")

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if (state, '') in self.transitions:
                for next_state in self.transitions[(state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        print(f"Epsilon closure for {states}: {closure}")
        return closure

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if (state, symbol) in self.transitions:
                next_states.update(self.transitions[(state, symbol)])
        print(f"Move from {states} on {symbol}: {next_states}")
        return next_states

    def to_dfa(self):
        dfa_states = {}
        dfa_transitions = []
        unmarked_states = [self.epsilon_closure({self.start_state})]
        dfa_states[frozenset(unmarked_states[0])] = 'A'
        state_mapping = {'A': unmarked_states[0]}
        new_state_count = 1

        while unmarked_states:
            current_states = unmarked_states.pop()
            current_state_name = [k for k, v in state_mapping.items() if v == current_states][0]
            print(f"Current DFA state: {current_state_name}, NFA states: {current_states}")

            for symbol in self.sigma:
                if symbol == '':
                    continue
                next_states = self.epsilon_closure(self.move(current_states, symbol))
                if not next_states:
                    continue

                if frozenset(next_states) not in dfa_states:
                    new_state_name = chr(65 + new_state_count)
                    dfa_states[frozenset(next_states)] = new_state_name
                    state_mapping[new_state_name] = next_states
                    unmarked_states.append(next_states)
                    new_state_count += 1
                else:
                    new_state_name = dfa_states[frozenset(next_states)]

                dfa_transitions.append((current_state_name, symbol, new_state_name))
                print(f"Added DFA transition: ({current_state_name}, {symbol}, {new_state_name})")

        dfa_final_states = {state for state, closure in state_mapping.items() if
                            self.accept_states.intersection(closure)}
        print(f"DFA final states: {dfa_final_states}")

        return DFA(self.sigma, list(dfa_states.keys()), dfa_transitions, 'A', dfa_final_states)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: nfa_to_dfa_converter.py nfa_config_file dfa_config_file")
        sys.exit(1)

    nfa_config_file = sys.argv[1]
    dfa_config_file = sys.argv[2]

    sigma, states, transitions = parse_input_file(nfa_config_file)

    # Debugging output for parsed transitions
    print(f"Parsed transitions: {transitions}")

    nfa = NFA(sigma, states, transitions)
    dfa = nfa.to_dfa()

    with open(dfa_config_file, 'w') as file:
        file.write("Sigma:\n")
        for symbol in dfa.sigma:
            file.write(f"{symbol}\n")
        file.write("End\nStates:\n")
        for state in dfa.states:
            state_line = state
            if state in dfa.accept_states:
                state_line += ",F"
            if state == dfa.start_state:
                state_line += ",S"
            file.write(f"{state_line}\n")
        file.write("End\nTransitions:\n")
        for trans in dfa.transitions:
            if len(trans) != 3:
                print(f"Skipping invalid transition: {trans}")
                continue
            print(f"Writing transition: {trans}")
            file.write(f"{trans[0]},{trans[1]},{trans[2]}\n")
        file.write("End\n")
