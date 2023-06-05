"""
Solution --- Day 7: No Space Left On Device ---

Assumption: in the command history, no directory is ever accessed before having
been discovered through the $ ls command (unless it is the root folder, which 
must therefore be accessed on the first line).
"""

import re

import aoc_tools as aoc

SMALL_SIZE = 100_000
AVAILABLE_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000


def main():
    filename = "input_07.txt"
    size_sum = sum_small_directory_sizes(filename)
    print(f"The sizes of all small directories sum to {size_sum}.")
    del_size = get_size_delete_directory(filename)
    print(f"The size of the smallest directory to delete is {del_size}.")


def sum_small_directory_sizes(filename):
    """Obtain the (size of) directories, and sum the small ones."""
    directories = get_directories(filename)
    if not all(d.count_ls >= 1 for d in directories):
        raise RuntimeError("Not all directories' contents have been checked!")
    return sum(d.size for d in directories if d.size <= SMALL_SIZE)


def get_size_delete_directory(filename):
    """Obtain the (size of) directories, and obtain smallest size to delete."""
    directories = get_directories(filename)
    if not all(d.count_ls >= 1 for d in directories):
        raise RuntimeError("Not all directories' contents have been checked!")
    directories.sort(key=lambda d: d.size)
    min_del_size = REQUIRED_SPACE - (AVAILABLE_SPACE - directories[-1].size)
    return next(d.size for d in directories if d.size >= min_del_size)


def get_directories(filename):
    """Read file input, and identify the directories and their size."""
    file_regex = re.compile(r"(\d+) (\S+)")
    command_history = aoc.read_stripped_lines(filename)
    if command_history[0] != "$ cd /":
        raise ValueError("First command does not access the root directory!")

    root = Directory("/")
    directories = [root]
    for command in command_history:
        if command == "$ cd /":
            cwd = root
        elif command == "$ cd ..":
            cwd = cwd.parent
        elif command.startswith("$ cd"):
            cwd = next(d for d in cwd.children if d.name == command[5:])
        elif command == "$ ls":
            cwd.count_ls += 1
        elif command.startswith("dir") and cwd.count_ls == 1:
            directories.append(Directory(command[4:], cwd))
        elif command[0].isdigit() and cwd.count_ls == 1:
            file_size = int(file_regex.search(command).group(1))
            cwd.update_size(file_size)
        else:
            raise ValueError(f"Unknown command {command} encountered!")
    return directories


class Directory:
    """Class to represent a directory."""

    def __init__(self, name, parent=None):
        """Create a directory with a parent, or a root directory."""
        self.name = name
        self.size = 0
        self.parent = parent
        self.children = []
        self.count_ls = 0
        if parent is not None:
            self.parent.add_directory(self)

    def add_directory(self, directory):
        """Add a child directory to this directory."""
        self.children.append(directory)

    def update_size(self, file_size):
        """Increase the size of this directory and all its ascendants."""
        self.size += file_size
        if self.parent is not None:
            self.parent.update_size(file_size)


if __name__ == "__main__":
    main()
