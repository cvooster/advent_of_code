"""Solution --- Day 13: Distress Signal ---"""

from functools import cmp_to_key

import aoc_tools as aoc

DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]


def main():
    filename = "input_13.txt"
    indices_sum = sum_indices(filename)
    print(f"The indices of correctly ordered pairs sum to {indices_sum}.")
    decoder_key = compute_decoder_key(filename)
    print(f"The decoder key for the stress signal is {decoder_key}.")


def sum_indices(filename):
    """Read file input, and sum the indices of correctly ordered pairs."""
    packet_lines = aoc.read_stripped_lines(filename)
    packets = [eval(line) for line in packet_lines if line]
    left_packets = packets[0 : len(packets) : 2]
    right_packets = packets[1 : len(packets) : 2]
    indices_sum = 0
    for idx, (left, right) in enumerate(zip(left_packets, right_packets)):
        is_correct, is_incorrect = check_order(left, right)
        if is_correct:
            indices_sum += idx + 1
        elif not (is_correct or is_incorrect):
            raise ValueError("Further instructions are needed to handle ties!")
    return indices_sum


def compute_decoder_key(filename):
    """Read file input, add the divider packets, order, and multiply indices."""
    packet_lines = aoc.read_stripped_lines(filename)
    packets = [eval(line) for line in packet_lines if line]
    packets.append(DIVIDER_PACKET_1)
    packets.append(DIVIDER_PACKET_2)
    packets.sort(key=cmp_to_key(compare))
    idx_1 = packets.index(DIVIDER_PACKET_1)
    idx_2 = packets.index(DIVIDER_PACKET_2)
    return (idx_1 + 1) * (idx_2 + 1)


def compare(left, right):
    """Return negative (positive) number if left comes before (after) right."""
    is_correct, is_incorrect = check_order(left, right)
    if not (is_correct or is_incorrect):
        raise ValueError("Further instructions are needed to handle ties!")
    return -1 if is_correct else 1


def check_order(left, right):
    """Recursively check whether nested lists (packets) are in right order."""
    is_correct = False
    is_incorrect = False
    paired_lists = zip(left, right)

    while not (is_correct or is_incorrect):
        try:
            # Obtain next elements if both lists have not run out of elements:
            elem_left, elem_right = next(paired_lists)
        except StopIteration:
            # Check which list ran out; return to outer level if both did:
            if len(left) == len(right):
                break
            elif len(left) < len(right):
                is_correct = True
            elif len(left) > len(right):
                is_incorrect = True
        else:
            # Check whether elements are integers or lists. If both elements are
            # integers, make a direct comparison:
            if isinstance(elem_left, int) and isinstance(elem_right, int):
                if elem_left == elem_right:
                    continue
                elif elem_left < elem_right:
                    is_correct = True
                elif elem_left > elem_right:
                    is_incorrect = True
            # Otherwise, convert the integer element (if any) to a list, and
            # move into the comparison of two lists:
            elif isinstance(elem_left, list) and isinstance(elem_right, int):
                is_correct, is_incorrect = check_order(elem_left, [elem_right])
            elif isinstance(elem_left, int) and isinstance(elem_right, list):
                is_correct, is_incorrect = check_order([elem_left], elem_right)
            elif isinstance(elem_left, list) and isinstance(elem_right, list):
                is_correct, is_incorrect = check_order(elem_left, elem_right)
    return is_correct, is_incorrect


if __name__ == "__main__":
    main()
