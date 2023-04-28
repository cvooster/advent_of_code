"""This module determines the character of the first start-of-packet marker."""

import sys

EXAMPLE_FILENAMES = [
    "input_06_example_1.txt",
    "input_06_example_2.txt",
    "input_06_example_3.txt",
    "input_06_example_4.txt",
    "input_06_example_5.txt",
]
EXAMPLE_ANSWERS = [7, 5, 6, 10, 11]

PATTERN_LENGTH = 4


def main():
    """Test example inputs, and then process the actual puzzle input."""
    for i, example_file in enumerate(EXAMPLE_FILENAMES):
        test_outcome(EXAMPLE_ANSWERS[i], example_file)
    filename = "input_06.txt"
    nr_characters = get_first_start_marker(filename)
    print(f"\nThe first start-of-packet marker arrives at {nr_characters}.")


def get_first_start_marker(filename):
    """Read the signal, and locate the first start-of-packet marker."""
    with open(filename) as file_object:
        signal = file_object.read().rstrip()
    if len(signal) < PATTERN_LENGTH:
        sys.exit("No start-of-packet marker found: signal too short!")

    for i in range(PATTERN_LENGTH, len(signal)):
        slice = signal[i - PATTERN_LENGTH : i]
        if len(slice) == len(set(slice)):
            return i
    sys.exit("No start-of-packet marker found!")


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = get_first_start_marker(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
