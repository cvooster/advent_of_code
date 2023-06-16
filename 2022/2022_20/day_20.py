"""Solution --- Day 20: Grove Positioning System ---"""

import aoc_tools as aoc

COORDINATE_OFFSETS = (1000, 2000, 3000)


def main():
    filename = "input_20.txt"
    coordinate_sum = sum_grove_coordinates(filename, 1, 1)
    print(f"The three grove coordinates sum to {coordinate_sum}.")
    coordinate_sum = sum_grove_coordinates(filename, 811589153, 10)
    print(f"The three grove coordinates sum to {coordinate_sum}.")


def sum_grove_coordinates(filename, decryption_key, nr_mixes):
    """Obtain original list, mix repeatedly, and get the grove coordinates."""
    original_list, node_zero = initialize_numbers(filename, decryption_key)
    for _ in range(nr_mixes):
        mix_numbers(original_list)
    return sum(get_grove_coordinates(node_zero, len(original_list)))


def initialize_numbers(filename, decryption_key):
    """Read file input, and initialize the mixing process."""
    lines = aoc.read_stripped_lines(filename)
    if lines.count("0") != 1:
        raise ValueError("There is not one value '0' in the input file!")
    idx_zero = lines.index("0")

    # Link the numbers and store their original order:
    original_list = [MovingNumber(int(line) * decryption_key) for line in lines]
    list_len = len(original_list)
    for idx, node in enumerate(original_list):
        node.right = original_list[(idx + 1) % list_len]
        node.left = original_list[(idx - 1) % list_len]
        node.set_shift(list_len)

    # Return their original order and a reference to the value 0:
    return original_list, original_list[idx_zero]


def mix_numbers(original_list):
    """Move all numbers in the order they originally appear in the file."""
    for node in original_list:
        if node.shift == 0:
            continue

        # Obtain the new neighbor nodes:
        if node.shift > 0:
            new_left = node
            for _ in range(node.shift):
                new_left = new_left.right
            new_right = new_left.right
        elif node.shift < 0:
            new_right = node
            for _ in range(-node.shift):
                new_right = new_right.left
            new_left = new_right.left

        # Remove the node:
        cur_left = node.left
        cur_right = node.right
        cur_left.right = cur_right
        cur_right.left = cur_left

        # Reinsert the node:
        node.left = new_left
        new_left.right = node
        node.right = new_right
        new_right.left = node


def get_grove_coordinates(node_zero, list_len):
    """Identify the three numbers that form the grove coordinates."""
    node = node_zero
    coordinates = []
    for i in range(3):
        subtrahend = COORDINATE_OFFSETS[i - 1] if i > 0 else 0
        difference = COORDINATE_OFFSETS[i] - subtrahend
        for _ in range(difference % list_len):
            node = node.right
        coordinates.append(node.number)
    return coordinates


class MovingNumber:
    """Class to represent a number that is being moved in the mixing process."""

    def __init__(self, number):
        """Create a moving number to use as node in a circularly linked list."""
        self.number = number
        self.left = None
        self.right = None
        self.shift = None

    def set_shift(self, list_len):
        """
        Set the number of positions to shift this number in the mixing process.

        Note that a number is back at its original position when it has moved
        (list_len - 1) places to the left or to the right.
        """
        shift = self.number % (list_len - 1)
        if shift > (list_len - 1) / 2:
            shift -= list_len - 1
        self.shift = shift


if __name__ == "__main__":
    main()
