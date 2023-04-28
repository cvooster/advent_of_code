"""This module calculates the total score if play follows the strategy guide."""

EXAMPLE_FILENAME = "input_02_example.txt"
EXAMPLE_ANSWER = 15

SCORE_ACTION = {"X": 1, "Y": 2, "Z": 3}
SCORE_OUTCOME = {"W": 6, "D": 3, "L": 0}
OUTCOME_ROUND = {
    "W": ["A Y", "B Z", "C X"],
    "D": ["A X", "B Y", "C Z"],
    "L": ["A Z", "B X", "C Y"],
}

SCORE_ROUND = {}
for outcome in OUTCOME_ROUND.keys():
    for round in OUTCOME_ROUND[outcome]:
        SCORE_ROUND[round] = SCORE_OUTCOME[outcome] + SCORE_ACTION[round[2]]

# Much simpler would have been to specify the scoring rule explicitly:
#
# SCORE_ROUND = {'A X': 3 + 1, 'A Y': 6 + 2, 'A Z': 0 + 3,
#                'B X': 0 + 1, 'B Y': 3 + 2, 'B Z': 6 + 3,
#                'C X': 6 + 1, 'C Y': 0 + 2, 'C Z': 3 + 3}


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
