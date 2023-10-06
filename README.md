## REGEX-NFA-ENGINE
This program converts Regular Expressions (RE) provided in postfix notation into their equivalent Non-deterministic Finite Automaton (NFA) and displays the transitions between states of the generated NFA. The program reads REs from a specified input file, where each line represents a distinct RE. It then processes each RE, generates its corresponding NFA, and outputs the start state, accept state, and transitions of the NFA.

## Creator Info
- **Name:** Daniel Basarab
- **Email:** daniel.basarab@wsu.edu


### File List
- **REtoNFA.py:** The main Python script which contains the code to convert regular expressions to NFAs.

### Compiler/Interpreter Version Used
- Python 3.11.3

### Compile Instructions
- The project is written in Python and does not need to be compiled. 

### Run Instructions
- The script takes a single command line argument, which is the path to a text file containing the regular expressions (each on a new line) that you want to convert to NFAs.
- Ensure that you have Python 3 installed on your machine.
- Open a terminal or command prompt.
- Navigate to the directory containing `REtoNFA.py`.
- Run the script with the path to your input file as an argument:
  ```
  python REtoNFA.py <path_to_your_file>
  ```
  Replace `<path_to_your_file>` with the path to your input file.
- The script will print the NFAs corresponding to the input regular expressions to the standard output.

#### Note
- Ensure that the input file is properly formatted, with one regular expression per line.
- The script will attempt to convert each line of the input file into an NFA and will print the resultant NFAs. If a line cannot be converted (due to being an invalid regular expression), the script will output an error message and terminate.

## Input File Format
The input file should contain one postfix Regular Expression per line. The supported operands are `a`, `b`, `c`, `d`, and `e`, and the supported operators are `|` (union), `*` (Kleene star), and `&` (concatenation). The epsilon character is represented by `E`.

Example input file content:
```
ab&
a*b|c&
```

## Output
The program outputs the resulting NFA for each input RE, displaying the start state, accept state, and transitions. Transitions are displayed in the format `(q[current_state], [symbol]) -> q[next_state]`.

Example output:
```
RE: ab&
Start: q0
Accept: q2
(q0, a) -> q1
(q1, b) -> q2
```

## Implementation Details
- **Transition Class**: Represents a transition in the NFA, containing the current state, symbol, and next state.
- **Automaton Class**: Represents an NFA, containing the start state, accept state, and a list of transitions.
- **REtoNFA Function**: Converts a postfix RE to its equivalent NFA.
- **convert_file_lines Function**: Reads REs from the input file and utilizes `REtoNFA` to generate and display NFAs.

