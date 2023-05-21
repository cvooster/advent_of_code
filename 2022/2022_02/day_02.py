"""Solution --- Day 2: Rock Paper Scissors ---"""

import aoc_tools as aoc


def main():
    filename = "input_02.txt"
    total_score = evaluate_strategy_guide(filename, 1)
    print(f"The part-1 score following the strategy guide is {total_score}.")
    total_score = evaluate_strategy_guide(filename, 2)
    print(f"The part-2 score following the strategy guide is {total_score}.")


def evaluate_strategy_guide(filename, part):
    """Read file input, and calculate the total score of the strategy guide."""
    round_lines = aoc.read_stripped_lines(filename)
    return sum(get_round_score(part)[line] for line in round_lines)


def get_round_score(part):
    """Get scoring rule for a round, for the specified part of the puzzle."""
    if part == 1:
        action_score = {"X": 1, "Y": 2, "Z": 3}
        outcome_score = {"W": 6, "D": 3, "L": 0}
        round_outcome = {
            "A X": "D",
            "A Y": "W",
            "A Z": "L",
            "B X": "L",
            "B Y": "D",
            "B Z": "W",
            "C X": "W",
            "C Y": "L",
            "C Z": "D",
        }
        round_score = {}
        for key, value in round_outcome.items():
            round_score[key] = action_score[key[2]] + outcome_score[value]
    elif part == 2:
        action_score = {"R": 1, "P": 2, "S": 3}
        outcome_score = {"X": 0, "Y": 3, "Z": 6}
        round_action = {
            "A X": "S",
            "A Y": "R",
            "A Z": "P",
            "B X": "R",
            "B Y": "P",
            "B Z": "S",
            "C X": "P",
            "C Y": "S",
            "C Z": "R",
        }
        round_score = {}
        for key, value in round_action.items():
            round_score[key] = action_score[value] + outcome_score[key[2]]
    return round_score


if __name__ == "__main__":
    main()
