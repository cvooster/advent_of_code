"""Solution --- Day 25: Full of Hot Air ---"""

import math

import aoc_tools as aoc


def main():
    filename = "input_25.txt"
    snafu_total = compute_snafu_total(filename)
    print(f"The fuel requirement, expressed as SNAFU number, is {snafu_total}.")


def compute_snafu_total(filename):
    """Convert file input to decimal numbers, and the total back to SNAFU."""
    snafu_lines = aoc.read_stripped_lines(filename)
    total_requirement = sum(convert_to_decimal(line) for line in snafu_lines)
    return convert_to_snafu(total_requirement)


def convert_to_decimal(snafu):
    """Convert a given SNAFU number (string) to a decimal number."""
    fuel_requirement = 0
    for i, snafu_digit in enumerate(snafu[-1::-1]):
        if snafu_digit == "=":
            fuel_requirement -= 2 * (5**i)
        elif snafu_digit == "-":
            fuel_requirement -= 1 * (5**i)
        elif snafu_digit == "0":
            pass
        elif snafu_digit == "1":
            fuel_requirement += 1 * (5**i)
        elif snafu_digit == "2":
            fuel_requirement += 2 * (5**i)
        else:
            raise ValueError("Unknown SNAFU digit encountered!")
    return fuel_requirement


def convert_to_snafu(decimal):
    """
    Convert a given decimal number to a SNAFU number (string).

    Note that the highest decimal number that can be formed using n SNAFU digits
    is \sum_{i=0}^{n-1} 2 * 5^{i} = (5^{n} - 1)/2. Hence, the number of digits
    needed to represent a given decimal number can be obtained by taking a
    logarithm and rounding up to the nearest integer.

    To obtain values of the SNAFU digits, make the following observation: If
    there are i remaining digits to represent (the remainder of) a decimal
    number, which must be in the range [-(5^{i}-1)/2, (5^{i}-1)/2], there exists
    a unique multiple of 5^{i-1} that can be subtracted to end up in the
    subrange [-(5^{i-1}-1)/2, (5^{i-1}-1)/2], as the latter range covers exactly
    5^{i-1}-1 decimal numbers. This multiplier will then be the value of the
    i-th SNAFU digit.
    """
    snafu_total = ""
    nr_digits = math.ceil((math.log(2 * decimal + 1, 5)))
    for i in range(nr_digits, 0, -1):
        diff = decimal - (5 ** (i - 1) - 1) / 2
        digit_value = math.ceil(diff / (5 ** (i - 1)))
        if digit_value == -2:
            snafu_total += "="
        elif digit_value == -1:
            snafu_total += "-"
        elif digit_value == 0:
            snafu_total += "0"
        elif digit_value == 1:
            snafu_total += "1"
        elif digit_value == 2:
            snafu_total += "2"
        decimal -= digit_value * (5 ** (i - 1))
    return snafu_total


if __name__ == "__main__":
    main()
