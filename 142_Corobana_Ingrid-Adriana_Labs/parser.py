# parser.py - LAB1

def parse_input_file(file_name):
    sigma = []
    states = []
    transitions = []
    current_section = None

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line == "Sigma:":
                current_section = "Sigma"
                continue
            elif line == "States:":
                current_section = "States"
                continue
            elif line == "Transitions:":
                current_section = "Transitions"
                continue
            elif line == "End":
                current_section = None
                continue

            if current_section == "Sigma":
                sigma.append(line)
            elif current_section == "States":
                state = tuple(line.split(","))
                states.append(state if len(state) > 1 else state[0])
            elif current_section == "Transitions":
                trans = tuple(line.split(","))
                transitions.append(trans)

    return sigma, states, transitions


def is_valid_dfa(sigma, states, transitions):
    # extrage numele stărilor
    state_names = [state[0] if isinstance(state, tuple) else state for state in states]
    # verif dacă există exact o stare de start
    start_states = [state for state in states if isinstance(state, tuple) and "S" in state[1]]
    if len(start_states) != 1:
        return False

    # verif tranziții valide
    for trans in transitions:
        if len(trans) != 3 or trans[0] not in state_names or trans[1] not in sigma or trans[2] not in state_names:
            return False
    return True


if __name__ == "__main__":
    sigma, states, transitions = parse_input_file("input.txt")
    if is_valid_dfa(sigma, states, transitions):
        print("DFA valid.")
    else:
        print("DFA invalid.")
