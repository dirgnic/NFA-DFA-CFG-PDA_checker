# cfg.py - LAB4
import sys
def parse_cfg(file_name):
    non_terminals = []
    terminals = []
    productions = {}
    start_symbol = None
    current_section = None

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line == "Non-terminals:":
                current_section = "Non-terminals"
                continue
            elif line == "Terminals:":
                current_section = "Terminals"
                continue
            elif line == "Productions:":
                current_section = "Productions"
                continue
            elif line == "Start-symbol:":
                current_section = "Start-symbol"
                continue
            elif line == "End":
                current_section = None
                continue

            if current_section == "Non-terminals":
                non_terminals.append(line)
            elif current_section == "Terminals":
                terminals.append(line)
            elif current_section == "Productions":
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                rhs = [r.strip() for r in rhs.split("|")]
                productions[lhs] = rhs
            elif current_section == "Start-symbol":
                start_symbol = line

    return non_terminals, terminals, productions, start_symbol


def validate_cfg(non_terminals, terminals, productions, start_symbol):
    if start_symbol not in non_terminals:
        return False
    for lhs, rhs_list in productions.items():
        if lhs not in non_terminals:
            return False
        for rhs in rhs_list:
            for symbol in rhs.split():
                if symbol not in non_terminals and symbol not in terminals and symbol != "ε":
                    return False
    return True


if __name__ == "__main__":
    cfg_file = "input1cfg.txt"
    non_terminals, terminals, productions, start_symbol = parse_cfg(cfg_file)
    if validate_cfg(non_terminals, terminals, productions, start_symbol):
        print("The CFG configuration is valid.")
    else:
        print("The CFG configuration is invalid.")
