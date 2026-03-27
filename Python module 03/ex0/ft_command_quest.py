#!/usr/bin/env python3
import sys


def print_argument():
    """
    Checks the number of arguments and prints them.
    """
    len_argv = len(sys.argv)
    i = 0
    if len_argv > 1:
        for arg in sys.argv:
            if i == 0:
                print(f"Program name: {sys.argv[0]}\n"
                      f"Arguments received: {len_argv - 1}")
                i += 1
            else:
                print(f"Argument {i}: {arg}")
                i += 1
    else:
        print(f"No arguments provided!\nProgram name: {sys.argv[0]}")
    print(f"Total arguments: {len_argv}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    print_argument()
