#!/usr/bin/env python3

def check_temperature(temp_str: str) -> int | None:
    """
    Check the temperature and catch the error
    arg: temp_str → user's temperature
    """
    try:
        print(f"\nTesting temperature: {temp_str}")
        temp = int(temp_str)
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")
        return None

    if temp < 0:
        raise ValueError(f"Error: {temp}°c is too cold! (min 0°c)")
    elif temp > 40:
        raise ValueError(f"Error: {temp}°c is too hot for plants! (max 40°c)")
    else:
        print(f"Temperature {temp}°c is perfect for plants!")
        return (temp)


def test_temperature_input():
    """
    Test different temperatures or posibily errors
    """
    print("=== Garden Temperature Checker ===")
    for value in ["25", "abc", "100", "-50"]:
        try:
            check_temperature(value)
        except ValueError as error:
            print(error)
    print("\nAll tests completed - program didn't crash!")
