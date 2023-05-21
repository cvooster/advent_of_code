"""Solution --- Day 6: Tuning Trouble ---"""

import aoc_tools as aoc


def main():
    filename = "input_06.txt"
    nr_characters = get_first_start_marker(filename, 4)
    print(f"The first start-of-packet marker is at character {nr_characters}.")
    nr_characters = get_first_start_marker(filename, 14)
    print(f"The first start-of-message marker is at character {nr_characters}.")


def get_first_start_marker(filename, pattern_length):
    """Determine the number of characters before a start marker is detected."""
    signal = aoc.read_stripped(filename)

    run_length = 0
    for idx, char in enumerate(signal):
        try:
            # Note: char is guaranteed to occur at most once in this slice.
            run_length -= signal[idx - run_length : idx].index(char)
        except ValueError:
            # Because char differs from elements in slice, run length increases.
            run_length += 1
            if run_length == pattern_length:
                return idx + 1
    raise ValueError("No start marker was detected!")


if __name__ == "__main__":
    main()
