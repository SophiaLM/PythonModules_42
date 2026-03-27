#!/usr/bin/env python3

plant = ["tomato", "letuce", "carrots"]


def water_plant(plant_list):
    """
    We verify that the list of plants provided is valid
    by checking whether they are included in the plant list.
    """
    try:
        print("Opening watering system")
        for veg in plant_list:
            if veg not in plant:
                raise ValueError(f"Error: cannot water {veg} - invalid plant!")
            else:
                print(f"Watering {veg}")
    except ValueError as error:
        print(error)
    finally:
        print("Closing waterinf system (cleanup)")


def test_watering_system():
    """
    We test with a correct list and an incorrect one.
    """
    print("=== Garden Watering System ===\n")

    good_list = ["tomato", "letuce", "carrots"]
    bad_list = ["tomato", "None", "carrots"]

    print("Testing normal watering . . .")
    water_plant(good_list)
    print("Waterinf complete successfully\n")

    print("Testing with error . . .")
    water_plant(bad_list)
    print("\nCleanup always happens, even with errors!")
