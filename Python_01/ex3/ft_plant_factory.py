#!/usr/bin/env python3

def ft_plant_factory():
    class Plant:
        def __init__(self, name: str, height: int, day: int) -> None:
            self.name = name
            self.height = height
            self.day = day

    Rose = Plant("Rose", 25, 30)
    Oak = Plant("Oak", 200, 365)
    Cactus = Plant("Cactus", 5, 90)
    Sunflower = Plant("Sunflower", 80, 45)
    Fern = Plant("Fern", 15, 120)

    garden = [Rose, Oak, Cactus, Sunflower, Fern]
    count = 0

    print("=== Plant Factory Output ===")

    for Plant in garden:
        print(f"Created: {Plant.name} ({Plant.height}cm, {Plant.day} days)")
        count += 1

    print(f"\nTotal plants created: {count}")
