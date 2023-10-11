import sys

#transition class for Automaton
class Transition:
    def __init__(self, current_state, symbol, next_state):
        self.current_state = current_state
        self.symbol = symbol
        self.next_state = next_state
    
    #comparator function needed to sort when outputing automaton
    def __lt__(self, other):
        if self.current_state != other.current_state:
            return self.current_state < other.current_state
        elif self.symbol != other.symbol:
            return self.symbol < other.symbol
        else:
            return self.next_state < other.next_state
        
    #to string method
    def __str__(self):
        return f"(q{self.current_state}, {self.symbol}) -> q{self.next_state}"

#Automaton Class
class Automaton:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state
        self.transitions = []
    
    #use transition class to add transitions
    def add_transition(self, current_state, symbol, next_state):
        self.transitions.append(Transition(current_state, symbol, next_state))
    
    #function to print the automaton
    def display(self):
        print(f"Start: q{self.start_state}")
        print(f"Accept: q{self.accept_state}")
        for transition in sorted(self.transitions):
            print(transition)

#this function takes in a input regular expression in postfix and prints its automaton
#returns 1 if the expression is malformed. 0 on sucess.
def REtoNFA(inputRE):
    stack = []
    operands = "abcde"
    epsilon = "E"
    num_of_states = 0

    #go through each char in the inputRE
    for char in inputRE:
        if char == epsilon or char == " ": continue #skip epsilons and spaces
        #if its a symbol then make a new automaton for it.
        if char in operands:
            my_automaton = Automaton(start_state=num_of_states+1, accept_state=num_of_states+2)
            my_automaton.add_transition(num_of_states+1, char, num_of_states+2)
            stack.append(my_automaton)
            num_of_states += 2

        elif char == "|":

            if len(stack) < 2:return 1 #ensure there is enough automatons in stack

            #pop 2 of the automatons from the stack
            automaton_a = stack.pop()
            automaton_b = stack.pop()

            #make new atomaton
            automaton_a_or_b = Automaton(start_state=num_of_states+1, accept_state=num_of_states+2)

            #all transition of a and b
            automaton_a_or_b.transitions.extend(automaton_a.transitions)
            automaton_a_or_b.transitions.extend(automaton_b.transitions)
            
            # Add epsilon transitions
            automaton_a_or_b.add_transition(automaton_a_or_b.start_state, 'E', automaton_a.start_state)
            automaton_a_or_b.add_transition(automaton_a_or_b.start_state, 'E', automaton_b.start_state)
            automaton_a_or_b.add_transition(automaton_a.accept_state, 'E', automaton_a_or_b.accept_state)
            automaton_a_or_b.add_transition(automaton_b.accept_state, 'E', automaton_a_or_b.accept_state)

            #push back to stack
            stack.append(automaton_a_or_b)
            num_of_states += 2

        elif char == "*":
            if len(stack) < 1:return 1

            automaton_a = stack.pop()

            automaton_star = Automaton(start_state=num_of_states+1, accept_state=num_of_states+1)
            automaton_star.transitions.extend(automaton_a.transitions)

            #transitions from new start/accept to old start and from old accept to new start/accept
            automaton_star.add_transition(automaton_star.start_state, "E", automaton_a.start_state)
            automaton_star.add_transition(automaton_a.accept_state, "E", automaton_star.start_state)

            stack.append(automaton_star)
            num_of_states += 1

        elif char == "&":

            if len(stack) < 2:return 1

            automaton_a = stack.pop()
            automaton_b = stack.pop()

            automaton_ab = Automaton(start_state=automaton_b.start_state, accept_state=automaton_a.accept_state)
            #all transition of a and b
            automaton_ab.transitions.extend(automaton_a.transitions)
            automaton_ab.transitions.extend(automaton_b.transitions)

            #transition from accept of b to start of a
            automaton_ab.add_transition(automaton_b.accept_state, "E", automaton_a.start_state)

            stack.append(automaton_ab)
        else: return 2

    if len(stack) != 1: return 1

    ##show final automaton
    print("RE: "+inputRE)
    final_automaton = stack.pop()
    final_automaton.display()
    print()
    return 0

#function for converting the postfix RE on each line of a file to NFA
def convert_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                result = REtoNFA(line.strip())
                if result == 1: #if there was an error in the RE
                    print("Error, malformed input on line "+ str(line_number))
                    print("exiting...")
                    exit(1)
                elif result == 2:
                    print("Error, unrecognized input on line "+ str(line_number))
                    print("exiting...")
                    exit(1)

                
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e: #handle other errors
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2: #ensure the file path argument was provided
        print("Usage: python "+ sys.argv[0] +" <file_path>")
        exit(1)
    
    convert_file_lines(sys.argv[1])
