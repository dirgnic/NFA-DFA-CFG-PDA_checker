# pda.py

from cfg import validate_cfg


class PDA:
    def __init__(self, states, input_symbols, stack_symbols, transitions, start_state, accept_states,
                 initial_stack_symbol):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.initial_stack_symbol = initial_stack_symbol

    def to_cfg(self):
        non_terminals = set()
        terminals = set(self.input_symbols)
        productions = {}
        start_symbol = f"[{self.start_state},{self.initial_stack_symbol},{self.start_state}]"

        for (state, input_symbol, stack_top), new_states in self.transitions.items():
            for (new_state, new_stack_top) in new_states:
                non_terminal = f"[{state},{stack_top},{new_state}]"
                non_terminals.add(non_terminal)
                if input_symbol != "ε":
                    rhs = f"{input_symbol} [{new_state},{new_stack_top},{new_state}]"
                else:
                    rhs = f"[{new_state},{new_stack_top},{new_state}]"
                productions.setdefault(non_terminal, []).append(rhs)

        return list(non_terminals), list(terminals), productions, start_symbol


if __name__ == "__main__":
    pda_file = "pda_input.txt"
    cfg_file = "cfg_output.txt"

    # Date reale pentru PDA-ul de paranteze echilibrate
    pda_states = ["q0", "q1", "q2"]
    input_symbols = ["(", ")"]
    stack_symbols = ["Z", "("]
    transitions = {
        ("q0", "(", "Z"): [("q1", "(")],
        ("q1", "(", "("): [("q1", "(")],
        ("q1", ")", "("): [("q1", "ε")],
        ("q1", "ε", "Z"): [("q2", "ε")]
    }
    start_state = "q0"
    accept_states = {"q2"}
    initial_stack_symbol = "Z"

    pda = PDA(pda_states, input_symbols, stack_symbols, transitions, start_state, accept_states, initial_stack_symbol)
    non_terminals, terminals, productions, start_symbol = pda.to_cfg()

    if validate_cfg(non_terminals, terminals, productions, start_symbol):
        with open(cfg_file, 'w') as file:
            file.write("Non-terminals:\n")
            for nt in non_terminals:
                file.write(f"{nt}\n")
            file.write("End\nTerminals:\n")
            for t in terminals:
                file.write(f"{t}\n")
            file.write("End\nProductions:\n")
            for lhs, rhs_list in productions.items():
                file.write(f"{lhs} -> {' | '.join(rhs_list)}\n")
            file.write("End\nStart-symbol:\n")
            file.write(f"{start_symbol}\nEnd\n")
        print("Converted PDA to CFG succesfully.")
    else:
        print("CFG from PDA invalid.")
