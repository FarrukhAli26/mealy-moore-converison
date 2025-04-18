
import matplotlib.pyplot as plt
import networkx as nx

class Moore:
    def __init__(self):
        self.number = 0
        self.inp = 0
        self.choice = 0
        self.ch = 0
        self.final = []
        self.noutput = []
        self.transaction = []
        self.ninputs = []
        self.cinputs = []
        self.language = ""
        self.lang = []

    def create(self):
        self.number = int(input("Enter the number of states you want: "))
        self.inp = int(input("Enter the number of inputs you want for each state: "))
        self.ch = int(input("Press 1 for numerical inputs. Press 2 for alphabetical inputs: "))

        if self.ch == 1:
            self.ninputs = [int(input("Enter your input: ")) for _ in range(self.inp)]
        elif self.ch == 2:
            self.cinputs = [input("Enter your input: ") for _ in range(self.inp)]

        self.choice = int(input("Press 1 for numerical gamma. Press 2 for alphabetical gamma: "))
        self.language = input("Enter your gamma for the language: ")

        if self.choice == 1:
            self.lang = [int(char) for char in self.language.split()]
        else:
            self.lang = [ord(char) for char in self.language]

        self.final = [0 for _ in range(1)]
        self.noutput = [0 for _ in range(self.number)]
        self.transaction = [[0 for _ in range(self.inp)] for _ in range(self.number)]

        for i in range(self.number):
            self.noutput[i] = self.get_valid_output(f"Enter the output for q{i}: ")
            for j in range(self.inp):
                self.transaction[i][j] = int(input(f"Enter the transaction state from q{i} at input {self.ninputs[j] if self.ch == 1 else self.cinputs[j]}: "))

    def get_valid_output(self, prompt):
        while True:
            output = input(prompt)
            try:
                output = int(output) if self.choice == 1 else ord(output)
                if output in self.lang:
                    return output
                else:
                    print("Your entered output does not match the gamma. Kindly enter again.")
            except ValueError:
                print("Invalid input. Please enter a valid value based on your gamma choice.")

    def transition_string(self):
        input_string = input("Enter a string to transition through the automaton: ")
        current_state = 0
        outputs = []
        transitions = []
        invalid_characters = []

        for char in input_string:
            try:
                input_val = int(char) if self.ch == 1 else char
                if input_val in (self.ninputs if self.ch == 1 else self.cinputs):
                    index = (self.ninputs if self.ch == 1 else self.cinputs).index(input_val)
                    next_state = self.transaction[current_state][index]
                    output = chr(self.noutput[next_state]) if self.choice == 2 else self.noutput[next_state]
                    transitions.append((current_state, input_val, next_state, output))
                    outputs.append(output)
                    current_state = next_state
                else:
                    invalid_characters.append(char)
            except ValueError:
                invalid_characters.append(char)

        print("Transition Path:")
        for tran in transitions:
            print(f"q{tran[0]} -({tran[1]})-> q{tran[2]} / Output: {tran[3]}")

        if invalid_characters:
            print(f"Invalid characters detected: {', '.join(invalid_characters)}.")
            return False
        return True

    def convert_to_mealy(self):
        mealy_transitions = {}
        for state in range(self.number):
            for input_index in range(self.inp):
                current_input = self.ninputs[input_index] if self.ch == 1 else self.cinputs[input_index]
                next_state = self.transaction[state][input_index]
                output = chr(self.noutput[next_state]) if self.choice == 2 else self.noutput[next_state]
                mealy_transitions[(state, current_input)] = (next_state, output)
        return mealy_transitions

    def visualize_moore(self):
        G = nx.DiGraph()
        labels = {i: f"q{i}/{chr(self.noutput[i]) if self.choice == 2 else self.noutput[i]}" for i in range(self.number)}
        for i in range(self.number):
            for j in range(self.inp):
                G.add_edge(i, self.transaction[i][j], label=self.ninputs[j] if self.ch == 1 else self.cinputs[j])  # Changed here
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 12))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='skyblue', font_size=15, font_weight='bold', arrowstyle='-|>', arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)
        plt.title("Moore Machine Visualization")
        plt.axis('off')
        plt.show()

    def visualize_mealy(self, mealy_transitions):
        G = nx.DiGraph()
        labels = {}
        for (state, input_val), (next_state, output) in mealy_transitions.items():
            G.add_node(state)
            G.add_node(next_state)
            edge_label = f"{input_val} / {output}"
            G.add_edge(state, next_state, label=edge_label)
            labels[state] = f"q{state}"
            labels[next_state] = f"q{next_state}"
        pos = nx.circular_layout(G)
        plt.figure(figsize=(12, 12))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=15, font_weight='bold', arrowstyle='-|>', arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)
        plt.title("Converted Mealy Machine Visualization")
        plt.axis('off')
        plt.show()

    def run(self):
        #self.create()
        print("\nOriginal Moore Machine:")
        self.visualize_moore()
        mealy_transitions = self.convert_to_mealy()
        print("\nConverted Mealy Machine:")
        self.visualize_mealy(mealy_transitions)


class Mealy:
    def __init__(self):
        self.number = 0
        self.inputs = []
        self.outputs = []
        self.transactions = []

    def create(self):
        self.number = int(input("Enter the number of states: "))
        self.inputs = input("Enter inputs separated by space: ").split()
        self.outputs = input("Enter outputs separated by space: ").split()

        self.transactions = []
        for i in range(self.number):
            transitions_for_state = []
            for inp in self.inputs:
                next_state = int(input(f"Enter the next state from state {i} on input '{inp}': "))
                output = input(f"Enter the output for state q{i} on input '{inp}': ")
                while output not in self.outputs:
                    print("Invalid output. Please enter a valid output from the list provided.")
                    output = input(f"Enter the output for state q{i} on input '{inp}': ")
                transitions_for_state.append((next_state, output))
            self.transactions.append(transitions_for_state)

    def visualize_mealy(self):
        G = nx.DiGraph()
        for state in range(self.number):
            for input_idx, inp in enumerate(self.inputs):
                next_state, output = self.transactions[state][input_idx]
                G.add_edge(f"q{state}", f"q{next_state}", label=f"{inp}/{output}")
        self._draw_graph(G, "Mealy Machine Visualization")

    def visualize_moore(self, moore_outputs):
        G = nx.DiGraph()
        for state in range(self.number):
            G.add_node(f"q{state}", label=f"q{state}/{moore_outputs[state]}")
            for input_idx, inp in enumerate(self.inputs):
                next_state, _ = self.transactions[state][input_idx]
                G.add_edge(f"q{state}", f"q{next_state}", label=f"{inp}")
        self._draw_graph(G, "Moore Machine Visualization", use_node_labels=True)

    def _draw_graph(self, G, title, use_node_labels=False):
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
        node_labels = nx.get_node_attributes(G, 'label') if use_node_labels else {node: node for node in G.nodes()}
        nx.draw(G, pos, labels=node_labels, node_color='skyblue', node_size=2000, font_size=15, font_weight='bold', arrowstyle='-|>', arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)
        plt.title(title)
        plt.axis('off')
        plt.show()

    def convert_to_moore(self):
        moore_outputs = [None] * self.number
        for state in range(self.number):
            for input_index in range(len(self.inputs)):
                next_state, output = self.transactions[state][input_index]
                moore_outputs[next_state] = output
        return moore_outputs

    def transition_string(self):
        input_string = input("Enter a string to simulate: ")
        current_state = 0
        valid = True
        print("Transition Path:")
        for char in input_string:
            if char in self.inputs:
                input_index = self.inputs.index(char)
                next_state, output = self.transactions[current_state][input_index]
                print(f"q{current_state} -({char})-> q{next_state} / Output: {output}")
                current_state = next_state
            else:
                print(f"Invalid input '{char}'. No transitions available.")
                valid = False
                break
        return valid

    def run(self):
        self.create()
        self.visualize_mealy()
        moore_outputs = self.convert_to_moore()
        self.visualize_moore(moore_outputs)
        while True:
            if not self.transition_string():
                break
            if input("Do you want to enter another string? (y/n): ").lower() != 'y':
                break

if __name__ == "__main__":
  exit = 0
  print("\t\t        -Theory Of Automata Project-        ")
  print("\t\t         -Mealy/Moore Conversions-         \n")
  print("\t\tName             Roll Number")
  print("\t\tFarrukh Ali      2KK-4279\n\t\tAreeb Ahmed      22K-4623\n\t\tPranjal          22K-4503\n")


  while exit != 1:
    option = int(input(" 1. create moore\n 2. create mealay\n 3. exit\n"))

    if option == 1:
      mo = Moore()
      mo.create()
      while not mo.transition_string():
          print("Please re-enter the entire string correctly.")
      #mo.visualize()
      mo.run()
    elif option == 2 :
      mealy_machine = Mealy()
      mealy_machine.run()

    elif option == 3:
      exit = 1
