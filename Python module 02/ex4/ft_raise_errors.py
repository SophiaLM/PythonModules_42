#!/usr/bin/env python3

def check_plant_health(plant_name, water_level, sunlight_hours):
    """Checks that the plant health parameters are within valid ranges."""
    if not plant_name or plant_name.strip() == "":
        raise ValueError("Error: Plant name cannot be empty!")

    if water_level < 1 or water_level > 10:
        raise ValueError(f"Error: Water level {water_level} "
                         "is invalid (must be 1-10)")

    if sunlight_hours < 2 or sunlight_hours > 12:
        raise ValueError(f"Error: Sunlight hours {sunlight_hours} is"
                         " too low/high (min 2, max 12)")

    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks():
    """Function to test the health checker with different values."""
    print("=== Garden Plant Health Checker ===\n")

    print("Testing good values...")
    try:
        result = check_plant_health("tomato", 5, 8)
        print(result)
    except ValueError as error:
        print(error)

    print("\nTesting empty plant name...")
    try:
        check_plant_health("", 5, 8)
    except ValueError as error:
        print(error)

    print("\nTesting bad water level...")
    try:
        check_plant_health("tomato", 15, 8)
    except ValueError as error:
        print(error)

    print("\nTesting bad sunlight hours...")
    try:
        check_plant_health("tomato", 5, 0)
    except ValueError as error:
        print(error)

    print("\nAll error raising tests completed successfully!")
