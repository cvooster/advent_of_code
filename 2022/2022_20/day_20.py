"""Solution --- Day 20: Grove Positioning System ---"""

import copy

import aoc_tools as aoc


def main():
    filename = "input_20.txt"
    coordinate_sum = sum_grove_coordinates(filename, 1, 1)
    print(f"The three grove coordinates sum to {coordinate_sum}.")
    coordinate_sum = sum_grove_coordinates(filename, 811589153, 10)
    print(f"The three grove coordinates sum to {coordinate_sum}.")


def sum_grove_coordinates(filename, decryption_key, nr_mixes):
    """Obtain original list, mix repeatedly, and get the grove coordinates."""
    original_list = initialize_list(filename, decryption_key)
    current_list = copy.copy(original_list)
    for _ in range(nr_mixes):
        mix_numbers(original_list, current_list)
    return sum(get_grove_coordinates(current_list))


def initialize_list(filename, decryption_key):
    """Read file input, and generate the original list."""
    number_lines = aoc.read_stripped_lines(filename)
    if number_lines.count("0") != 1:
        raise ValueError("There is not one value '0' in the input file!")
    original_list = []
    for idx, line in enumerate(number_lines):
        original_list.append(MovingNumber(int(line) * decryption_key, idx))
    return original_list


def mix_numbers(original_list, current_list):
    """
    Move all numbers in the order they originally appear in the file.

    Note that the circularity in this process implies that if a number moves off
    the left end of the list, it never ends up in the right-most place of the
    list, and vice versa.
    """
    for moving_number in original_list:
        # Obtain the new index of this number:
        new_index = moving_number.index + moving_number.number
        if new_index < 0:
            new_index = new_index % (len(original_list) - 1)
        elif new_index > 0:
            new_index = ((new_index - 1) % (len(original_list) - 1)) + 1
        # Update the indices of numbers that will shift in response:
        if new_index > moving_number.index:
            for i in range(moving_number.index + 1, new_index + 1):
                current_list[i].index -= 1
        elif new_index < moving_number.index:
            for i in range(new_index, moving_number.index):
                current_list[i].index += 1
        # Make the move:
        current_list.insert(new_index, current_list.pop(moving_number.index))
        moving_number.index = new_index


def get_grove_coordinates(current_list):
    """Identify the three numbers that form the grove coordinates."""
    index_0 = [mn.number for mn in current_list].index(0)
    coordinate_1 = current_list[(index_0 + 1000) % len(current_list)].number
    coordinate_2 = current_list[(index_0 + 2000) % len(current_list)].number
    coordinate_3 = current_list[(index_0 + 3000) % len(current_list)].number
    return [coordinate_1, coordinate_2, coordinate_3]


class MovingNumber:
    """Class to represent a number that is being moved in the mixing process."""

    def __init__(self, number, index):
        """Create a moving number, defined by a number and current index."""
        self.number = number
        self.index = index


if __name__ == "__main__":
    main()
