"""Find the top-three total number of calories carried by elves."""

filename = "puzzle_input_01.txt"


def main():
    with open(filename) as file_object:
        calorie_lines = file_object.readlines()

    if not calorie_lines:
        print("The elves have provided an empty list!")
    else:
        calorie_lines.append("")  # Set empty string at end of file.
        elf_totals = get_elf_totals(calorie_lines)

        max_total, top_three_sum = get_top_totals(elf_totals)
        print(f"The maximum calorie total carried by an elf is {max_total}.")
        print(f"The sum of the top-three calorie totals is {top_three_sum}")


def get_elf_totals(calorie_lines):
    """Compute the calorie total for each elf"""
    elf_inventories = []
    elf_totals = []
    elf_inventory = []

    for calorie_line in calorie_lines:
        if calorie_line.rstrip():
            elf_inventory.append(int(calorie_line.rstrip()))
        else:  # Blank line between elves' inventories or end of file.
            elf_inventories.append(elf_inventory)
            elf_totals.append(sum(elf_inventory))
            elf_inventory = []
    return elf_totals


def get_top_totals(elf_totals):
    """Determine the highest calorie totals, and sum the top three"""

    elf_numbers, sorted_totals = sort_elf_totals(elf_totals)
    max_total = sorted_totals[0]

    if len(sorted_totals) < 3:
        print("NOTE: there are less than three elves!")
        top_three_elves = elf_numbers
        top_three = sorted_totals
        print_top_three(top_three_elves, top_three)
        top_three_sum = sum(top_three)
    else:
        top_three_elves = elf_numbers[:3]
        top_three = sorted_totals[:3]
        print_top_three(top_three_elves, top_three)
        top_three_sum = sum(top_three)
    return max_total, top_three_sum


def sort_elf_totals(elf_totals):
    """Sort elf totals and identify the corresponding elves."""
    elf_numbers = []
    sorted_totals = []

    for index_and_total in sorted(
        enumerate(elf_totals), key=lambda itot: itot[1], reverse=True
    ):
        elf_numbers.append(index_and_total[0] + 1)
        sorted_totals.append(index_and_total[1])
    return elf_numbers, sorted_totals


def print_top_three(top_three_elves, top_three):
    """Print the (up to) three highest calorie totals"""
    print(f"The top-three total calorie amounts are {top_three}.")
    print(f"The corresponding elves are numbera {top_three_elves}.\n")


if __name__ == "__main__":
    main()
