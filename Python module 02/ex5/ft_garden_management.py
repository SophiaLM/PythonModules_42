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


class GardenManager:
    """
    Main class to manage garden operations
    """
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.plants = []

    def add_plant(self, name: str, height: int) -> None:
        """Add a plant and raise ValueError if name is empty."""
        if not name.strip():
            raise ValueError("Error adding plant: Plant name cannot be empty!")

        self.plants.append({"name": name, "height": height})
        print(f"Added {name} successfully")

    def water_plants(self) -> None:
        """Water all plants with mandatory cleanup."""
        print("\nOpening watering system")
        try:
            if not self.plants:
                raise WaterError("Error: No plants to water")
            for plant in self.plants:
                print(f"Watering {plant['name']} - success")

        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self, name: str, water: int, sun: int) -> str:
        """Check health and raise PlantError if values are bad."""
        if water > 10:
            raise PlantError(f"Error checking {name}:"
                             f" Water level {water} is too high (max 10)")
        if sun < 2:
            raise PlantError(f"Error: Sunlight hours {sun} is too low (min 2)")

        return (f"{name}: healthy (water: {water}, sun: {sun})")


def test_garden_management():
    """
    Test different scenarios and possible errors.
    """
    print("=== Garden Management System ===\n")

    manager = GardenManager("Sophy")

    print("Adding plants to garden...")
    try:
        manager.add_plant("tomato", 25)
        manager.add_plant("lettuce", 10)
        manager.add_plant("", 0)
    except ValueError as e:
        print(e)

    print("\nWatering plants...")
    try:
        manager.water_plants()
    except WaterError as e:
        print(e)

    print("\nChecking plant health...")
    try:
        status = manager.check_plant_health("tomato", 5, 8)
        print(status)
    except PlantError as e:
        print(e)

    try:
        manager.check_plant_health("lettuce", 15, 8)
    except PlantError as e:
        print(e)

    print("\nTesting error recovery...")
    try:
        raise GardenError("Not enough water in tank")
    except GardenError as error:
        print(f"Caught GardenError: {error}")
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")
