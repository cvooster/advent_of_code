"""Solution --- Day 10: Cathode-Ray Tube ---"""

import aoc_tools as aoc

START_VALUE = 1
CYCLES = list(range(20, 260, 40))
PIXEL_WIDTH = 40
PIXEL_HEIGHT = 6
NR_PIXELS = PIXEL_WIDTH * PIXEL_HEIGHT


def main():
    filename = "input_10.txt"
    signal_strength_sum, pixel_pattern = simulate_crt(filename)
    print(f"The six signal strengths sum to {signal_strength_sum}.\n")
    draw_on_screen(pixel_pattern)


def simulate_crt(filename):
    """Determine register values, and derive signal strengths and pixels."""
    register_values = compute_register_values(filename)
    signal_strength_sum = sum_signal_strengths(register_values)
    pixel_pattern = generate_pixel_pattern(register_values)
    return signal_strength_sum, pixel_pattern


def compute_register_values(filename):
    """Read file input, and compute the value of the X register."""
    program_lines = aoc.read_stripped_lines(filename)
    current_value = START_VALUE
    register_values = [current_value]
    for instruction in program_lines:
        register_values.append(current_value)
        instruction_parts = instruction.split(" ")
        if instruction_parts[0] == "addx":
            current_value += int(instruction_parts[1])
            register_values.append(current_value)
    return register_values


def sum_signal_strengths(register_values):
    """Sum the six signal strengths of special interest."""
    try:
        return sum(register_values[cycle - 1] * cycle for cycle in CYCLES)
    except IndexError as e:
        raise IndexError(f"Program took less than {CYCLES[-1]} cycles!") from e


def generate_pixel_pattern(register_values):
    """Construct the pattern of dark and lit pixels."""
    try:
        pixel_pattern = ""
        for idx in range(NR_PIXELS):
            if -1 <= register_values[idx] - (idx % PIXEL_WIDTH) <= 1:
                pixel_pattern += "#"
            else:
                pixel_pattern += "."
    except IndexError as e:
        raise IndexError(f"Program took less than {NR_PIXELS} cycles!") from e
    else:
        return pixel_pattern


def draw_on_screen(pixel_pattern):
    """Draw a screen of size PIXEL_HEIGHT by PIXEL_WIDTH pixels."""
    for i in range(0, NR_PIXELS, PIXEL_WIDTH):
        print(pixel_pattern[i : i + PIXEL_WIDTH])
    print()


if __name__ == "__main__":
    main()
