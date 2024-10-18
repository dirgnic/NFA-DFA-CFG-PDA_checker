
def isvalid(transitions, sigma, states):
    for value in transitions:
        statesNew = [state[0] if type(state) is tuple else state for state in states]
        print(statesNew)
        if value[0] not in statesNew or value[2] not in sigma or value[1] not in statesNew:
            return False

        return True

def statesGet(states):
    statesNew = [state[0] if type(state) is tuple else state for state in states]
  #  print(statesNew)
    return statesNew
def parse():
    sigma = []
    states = []
    transitions = []
    with open("input.txt", 'r') as file:
       line = file.readline().strip("\n")
       while line != "Sigma:":
           line = file.readline().strip("\n")
       # store alphabet
       while line != "End":
           line = file.readline().strip("\n")
           sigma.append(line)
       sigma.pop()
       print(sigma)

       line = file.readline().strip("\n")
       while line != "States:":
           line = file.readline().strip("\n")
       # store possible states as keys
       while line != "End":
           line = file.readline().strip("\n")
           state = tuple(line.split(","))
           if len(state)==1:
               states.append(line)
           else:
               states.append(state)
       states.pop()
       print(states)
       line = file.readline().strip("\n")
       while line != "Transitions:":
           line = file.readline().strip("\n")

       while line != "End":
           line = file.readline().strip("\n")
           trans = tuple(line.split(","))
           transitions.append(trans)
       transitions.pop()
       print(transitions)
       print(isvalid(transitions, sigma, states))
       v = ['']*10
       i=0
       eps = []
       print(eps_closure(transitions, sigma, statesGet(states), v, eps, i))




def load_file(file_name):
    content = {}
    k = 1
    currentKey = ""
    with open(file_name, 'r') as file:
     line = file.readline().strip("\n")
     while line:
        if line[0] == "#":
            line = file.readline().strip("\n")
            continue
        if line == "End":
            k =0
            line = file.readline().strip("\n")
            continue
        # store alphabet
        if currentKey == "" or k==0:
            currentKey = line
            k=1
        else:
            content[currentKey] = content.get(currentKey, [])
            state = tuple(line.split(","))
            if len(state) == 1:
                content[currentKey].append(line)
            else:
                content[currentKey].append(state)
        line = file.readline().strip("\n")
     print(content)
     return content

def eps_closure(transitions, sigma, statesNew, v, eps, i):

     for state in statesNew:
         if i==0:
             v[i] = state
             if state not in eps:
                 eps.append(state)
             eps_closure(transitions, sigma, statesNew, v, eps, i+1)
         else:
             for trans in transitions:
               #  print(trans[2] + v[i-1] + str(i))
                 if trans[2] == state and trans[0] == v[i-1]:
                     v[i] = state
                     if state not in eps:
                         eps.append(state)
                     eps_closure(transitions, sigma, statesNew, v, eps, i+1)
     return eps




if __name__ == '__main__':
    parse()
    load_file("input.txt")


