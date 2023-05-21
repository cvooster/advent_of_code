"""This module provides useful tools for solving advent-of-code puzzles."""


def read(filename):
    """Read file content, return as string."""
    with open(filename) as file_object:
        file_string = file_object.read()
    if not file_string:
        raise ValueError("The input file is empty!")
    return file_string


def read_lines(filename, add_line=None):
    """Read file content, return as list of lines."""
    with open(filename) as file_object:
        file_lines = [line for line in file_object]
    if not file_lines:
        raise ValueError("The input file is empty!")
    elif not add_line is None:
        file_lines.append(add_line)
    return file_lines


def read_stripped(filename):
    """Read file content, return as string without trailing spaces."""
    with open(filename) as file_object:
        file_string = file_object.read().rstrip()
    if not file_string:
        raise ValueError("The input file is empty!")
    return file_string


def read_stripped_lines(filename, add_line=None):
    """Read file content, return as list of lines without trailing spaces."""
    with open(filename) as file_object:
        file_lines = [line.rstrip() for line in file_object]
    if not file_lines:
        raise ValueError("The input file is empty!")
    elif not add_line is None:
        file_lines.append(add_line)
    return file_lines
