"""
Solution --- Day 21: Monkey Math ---

The current solution assumes that, in part 2, the monkeys' numbers will turn out
to be linear functions of the number yelled by monkey 'humn.' If not, this code
will not provide an answer.
"""

import aoc_tools as aoc


def main():
    filename = "input_21.txt"
    root_number = calculate_number(filename, False)
    print(f"The monkey named root will yell {root_number}.")
    humn_number = calculate_number(filename, True)
    print(f"To pass the equality test, yell {humn_number}.")


def calculate_number(filename, override_humn=False):
    """Initialize monkeys, and simulate their yelling until answer is known."""
    monkeys, root_monkey = initialize_monkeys(filename, override_humn)
    return yell_numbers(monkeys, root_monkey, override_humn)


def initialize_monkeys(filename, override_humn):
    """Read file input, initialize the monkeys, and identify the root monkey."""
    monkey_lines = aoc.read_stripped_lines(filename)
    monkeys = []
    for line in monkey_lines:
        name = line[0:4]
        if override_humn and name == "humn":
            monkeys.append(Monkey(name, 0, 1))
        elif line[6].isdecimal():
            monkeys.append(Monkey(name, int(line[6:]), 0))
        elif line[6].isalpha():
            monkeys.append(Monkey(name))
    lookup = {m.name: m for m in monkeys}
    for line, monkey in zip(monkey_lines, monkeys):
        if line[6].isalpha():
            input_1 = lookup[line[6:10]]
            input_2 = lookup[line[13:17]]
            operation = line[11]
            monkey.set_calculation(input_1, input_2, operation)
    root_monkey = lookup["root"]
    return monkeys, root_monkey


def yell_numbers(monkeys, root_monkey, override_humn):
    """Simulate yelling of linear expressions until root inputs are known."""
    while any(i.constant is None for i in root_monkey.inputs):
        for monkey in monkeys:
            if monkey.constant is None:
                if all(i.constant is not None for i in monkey.inputs):
                    monkey.perform_calculation()

    # The root inputs are known, and the answer can be computed:
    if not override_humn:
        root_monkey.perform_calculation()
        answer = root_monkey.constant
    elif override_humn:
        num = root_monkey.inputs[1].constant - root_monkey.inputs[0].constant
        denom = root_monkey.inputs[0].slope - root_monkey.inputs[1].slope
        answer = num / denom
    return int(answer) if answer.is_integer() else answer


class Monkey:
    """Class to represent a monkey."""

    def __init__(self, name, constant=None, slope=None):
        """Create a named monkey with (possibly) a constant or coefficient."""
        self.name = name
        self.constant = constant
        self.slope = slope
        self.inputs = [None, None]
        self.operation = ""

    def set_calculation(self, input_1, input_2, operation):
        """Set the inputs and operator of the basic math operation."""
        self.inputs[0] = input_1
        self.inputs[1] = input_2
        self.operation = operation

    def perform_calculation(self):
        """Perform the basic math operation."""
        if self.operation == "+":
            self._perform_addition()
        elif self.operation == "-":
            self._perform_subtraction()
        elif self.operation == "*":
            self._perform_multiplication()
        elif self.operation == "/":
            self._perform_division()

    def _perform_addition(self):
        """Perform an addition."""
        self.constant = self.inputs[0].constant + self.inputs[1].constant
        self.slope = self.inputs[0].slope + self.inputs[1].slope

    def _perform_subtraction(self):
        """Perform a subtraction."""
        self.constant = self.inputs[0].constant - self.inputs[1].constant
        self.slope = self.inputs[0].slope - self.inputs[1].slope

    def _perform_multiplication(self):
        """Perform a multiplication."""
        self.constant = self.inputs[0].constant * self.inputs[1].constant
        if self.inputs[0].slope == 0:
            self.slope = self.inputs[0].constant * self.inputs[1].slope
        elif self.inputs[1].slope == 0:
            self.slope = self.inputs[0].slope * self.inputs[1].constant
        else:
            raise ValueError("This results in a non-linear expression!")

    def _perform_division(self):
        """Perform a division."""
        if self.inputs[1].slope == 0:
            self.constant = self.inputs[0].constant / self.inputs[1].constant
            self.slope = self.inputs[0].slope / self.inputs[1].constant
        elif (
            self.inputs[1].slope != 0
            and self.inputs[0].constant * self.inputs[1].slope
            == self.inputs[1].constant * self.inputs[0].slope
        ):
            self.constant = self.inputs[0].slope / self.inputs[1].slope
            self.slope = 0
        else:
            raise ValueError("This results in a non-linear expression!")


if __name__ == "__main__":
    main()
