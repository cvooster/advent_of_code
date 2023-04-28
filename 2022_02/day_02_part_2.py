"""This module calculates the total score if play follows the strategy guide."""

EXAMPLE_FILENAME = "input_02_example.txt"
EXAMPLE_ANSWER = 12

SCORE_ACTION = {"A": 1, "B": 2, "C": 3}
SCORE_OUTCOME = {"X": 0, "Y": 3, "Z": 6}
ACTION_ROUND = {
    "A": ["A Y", "B X", "C Z"],
    "B": ["A Z", "B Y", "C X"],
    "C": ["A X", "B Z", "C Y"],
}

SCORE_ROUND = {}
for action in ACTION_ROUND.keys():
    for round in ACTION_ROUND[action]:
        SCORE_ROUND[round] = SCORE_ACTION[action] + SCORE_OUTCOME[round[2]]

# Much simpler would have been to specify the scoring rule explicitly:
#
# SCORE_ROUND = {'A X': 0 + 3, 'A Y': 3 + 1, 'A Z': 6 + 2,
#                'B X': 0 + 1, 'B Y': 3 + 2, 'B Z': 6 + 3,
#                'C X': 0 + 2, 'C Y': 3 + 3, 'C Z': 6 + 1}


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_02.txt"
    total_score = evaluate_strategy_guide(filename)
    print(f"\nThe total score following the strategy guide is {total_score}.")


def evaluate_strategy_guide(filename):
    """Read a strategy guide from a file, and evaluate the total score."""
    with open(filename) as file_object:
        return sum([SCORE_ROUND[line.rstrip()] for line in file_object])


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = evaluate_strategy_guide(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
