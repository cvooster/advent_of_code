"""Solution --- Day 1: Calorie Counting ---"""

import aoc_tools as aoc


def main():
    filename = "input_01.txt"
    max_total = sum_top_totals(filename, 1)
    print(f"The maximum calorie total carried by an elf is {max_total}.")
    top_totals_sum = sum_top_totals(filename, 3)
    print(f"The sum of the top-three calorie totals is {top_totals_sum}.")


def sum_top_totals(filename, cut_off_rank):
    """Read file input, and sum the {cut_off_rank}-highest totals."""
    calorie_lines = aoc.read_stripped_lines(filename, add_line="")
    sorted_totals = sorted(calculate_elf_totals(calorie_lines))
    if cut_off_rank <= len(sorted_totals):
        return sum(sorted_totals[-cut_off_rank:])
    else:
        raise IndexError("Cut-off rank exceeds the number of elves!")


def calculate_elf_totals(calorie_lines):
    """Calculate the total number of calories for all elves."""
    all_totals = []
    elf_total = 0
    for calorie_line in calorie_lines:
        if calorie_line:
            elf_total += int(calorie_line)
        else:
            all_totals.append(elf_total)
            elf_total = 0
    return all_totals


if __name__ == "__main__":
    main()
