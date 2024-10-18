# dfa_check.py - LAB2

import sys
from parser import parse_input_file, is_valid_dfa

# dfa_check.py


class DFA:
    def __init__(self, sigma, states, transitions, start_state=0, accept_states=0):
        self.sigma = sigma
        # creez dicț stări și tranziții
        self.states = {state[0]: state[1:] for state in states if isinstance(state, tuple)}
        self.states.update({state: [] for state in states if not isinstance(state, tuple)})
        self.transitions = {(trans[0], trans[1]): trans[2] for trans in transitions}
        # det starea de start și stările accept
        self.start_state = next(state for state in states if isinstance(state, tuple) and "S" in state[1])[0]
        self.accept_states = {state[0] for state in states if isinstance(state, tuple) and "F" in state[1]}
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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: dfa_engine.py dfa_config_file input_string")
        sys.exit(1)

    config_file = sys.argv[1]
    input_string = sys.argv[2]

    sigma, states, transitions = parse_input_file(config_file)

    if not is_valid_dfa(sigma, states, transitions):
        print("DFA invalid")
        sys.exit(1)

    dfa = DFA(sigma, states, transitions)

    if dfa.accepts(input_string):
        print("accept")
    else:
        print("reject")
