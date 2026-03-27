#!/usr/bin/env python3

class GardenError(Exception):
    """Base exception for all garden problems."""
    def __init__(self, msg: str = "Garden Error"):
        super().__init__(msg)


class PlantError(GardenError):
    """Exception raised for problems with individual plants."""
    def __init__(self, health: str = "Plant Error"):
        super().__init__(health)


class WaterError(GardenError):
    """Exception raised for problems with the watering system."""
    def __init__(self, tank: str = "Water Error"):
        super().__init__(tank)


def test_plant_error() -> None:
    """Raise and catch a PlantError."""
    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as error:
        print(f"Caught PlantError: {error}\n")


def test_water_error() -> None:
    """Raise and catch a WaterError."""
    print("Testing PlantError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as error:
        print(f"Caught a WaterError: {error}\n")


def test_all_errors() -> None:
    """Show that GardenError catch all specific errors"""
    print("Testing catching all garden errors...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as error:
        print(f"Caught a garden error: {error}")
    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as error:
        print(f"Caught a garden error: {error}\n")


def main():
    """Run the complete program"""
    print("=== Custom Garden Errors Demo ===\n")
    test_plant_error()
    test_water_error()
    test_all_errors()
    print("All custom error types work correctly!")
