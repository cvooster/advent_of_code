"""
Solution --- Day 11: Monkey in the Middle ---

Part 2 uses the observation that because modulo congruence is compatible with
translation, scaling, and exponentiation (which encompasses the operations of all
monkeys in the input file). It follows that subtracting an integer multiple of
the product of all monkey's divisors in the current round will in no future
round change the remainder of the modulo operation where the product of all
monkeys' divisors is used as modulus. As this divisor product is an integer
multiple of each individual monkey's divisor, neither will it in any future
round change the remainder of the modulo operation where an individual monkey's
divisor is used as modulus; therefore, inspection outcomes will not change.
"""

from collections import deque
import math

import aoc_tools as aoc


def main():
    filename = "input_11.txt"
    business_level = calculate_business_level(filename, 20, 1)
    print(f"The monkey business level after 20 rounds is {business_level}.")
    business_level = calculate_business_level(filename, 10_000, 2)
    print(f"The monkey business level after 10000 rounds is {business_level}.")


def calculate_business_level(filename, nr_rounds, worry_management):
    """Play keep away, and multiply inspections of two most active monkeys."""
    monkeys = initialize_monkeys(filename)
    if len(monkeys) < 2:
        raise ValueError("Too few monkeys to calculate business level!")
    play_keep_away(monkeys, nr_rounds, worry_management)
    return math.prod(sorted([mk.nr_inspections for mk in monkeys])[-2:])


def initialize_monkeys(filename):
    """Read file input, and initialize all monkeys."""
    monkey_lines = aoc.read_stripped_lines(filename)
    monkeys = []
    for idx in range(0, len(monkey_lines), 7):
        items = [int(level) for level in monkey_lines[idx + 1][18:].split(",")]
        operation_function_str = "lambda old: " + monkey_lines[idx + 2][19:]
        operation_function = eval(operation_function_str)
        test_divisor = int(monkey_lines[idx + 3][20:])
        true_idx = int(monkey_lines[idx + 4][28:])
        false_idx = int(monkey_lines[idx + 5][29:])
        test_outcomes = {False: false_idx, True: true_idx}
        monkeys.append(
            Monkey(items, operation_function, test_divisor, test_outcomes)
        )
    return monkeys


def play_keep_away(monkeys, nr_rounds, worry_management):
    """Simulate a number of rounds of keep away."""
    factor_out = math.prod([mk.test_divisor for mk in monkeys])
    for _ in range(nr_rounds):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                worry_level = monkey.throw_item()
                worry_level = monkey.operation_function(worry_level)
                if worry_management == 1:
                    worry_level //= 3
                elif worry_management == 2:
                    worry_level %= factor_out
                is_divisible = (worry_level % monkey.test_divisor) == 0
                receiver_idx = monkey.test_outcomes[is_divisible]
                monkeys[receiver_idx].catch_item(worry_level)


class Monkey:
    """Class to represent a monkey."""

    def __init__(self, items, operation_function, test_divisor, test_outcomes):
        """Create a monkey with an item queue, and operation/test functions."""
        self.items = deque(items)
        self.operation_function = operation_function
        self.test_divisor = test_divisor
        self.test_outcomes = test_outcomes
        self.nr_inspections = 0

    def throw_item(self):
        """Throw an item to another monkey."""
        self.nr_inspections += 1
        return self.items.popleft()

    def catch_item(self, worry_level):
        """Catch an item thrown by another monkey."""
        self.items.append(worry_level)


if __name__ == "__main__":
    main()
