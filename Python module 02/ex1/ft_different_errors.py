#!/usr/bin/env python3

def not_valid_value(user_number):
    """Check that the value is a valid number."""
    try:
        number = int(user_number)
    except ValueError:
        print("Caught ValueError: invalid literal for int()")
        return None

    if number < 0:
        print("Too cold!")
        return None
    elif number > 40:
        print("Too hot!")
        return None
    else:
        print("Valid temperature!")
        return (number)


def safe_division(first_number, second_number):
    """Verify that we are not multiplying by 0 (it is not possible)."""
    try:
        number = first_number / second_number
        return (number)
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero")
        return None


def find_file(user_file):
    """Check that the file exists and catch the error"""
    try:
        file = open(user_file)
        content = file.read()
        file.close()
        return (content)
    except FileNotFoundError:
        print(f"Caught FileNotFoundError: No such file '{user_file}'")
        return None


def key_not_found(value):
    """Check that the key we need exists within a dictionary, list, etc"""
    try:
        dic = {"plant": "tomato"}
        return (dic[value])
    except KeyError:
        print(f"Caught KeyError: '{value}'")
        return None


def multiple_errors(value):
    """Test the errors we used previously together."""
    try:
        number = int(value)
        number / 0
        open("missing.txt")
    except (ValueError, ZeroDivisionError, FileNotFoundError):
        print("Caught an error, but program continues!")


def garden_operations():
    """Call the errors created to test them."""
    print("\nTesting ValueError...")
    not_valid_value("abc")
    print("\nTesting ZeroDivisionError...")
    safe_division(10, 0)
    print("\nTesting FileNotFoundError...")
    find_file('missing.txt')
    print("\nTesting KeyError...")
    key_not_found("missing: plant")
    print("\nTesting multiple errors together...")
    multiple_errors("abc")


def test_error_types():
    """Print the script showing the errors"""
    print("=== Garden Error Types Demo ===")
    garden_operations()
    print("\nAll error types tested successfully!")
