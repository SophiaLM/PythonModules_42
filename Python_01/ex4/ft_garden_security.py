#!/usr/bin/env python3

class SecurePlant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.__name = name
        self.__height = height
        self.__age = age

    def set_height(self, height):
        if height < 0:
            print(f"\nInvalid operation attempted: "
                  f"height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def get_days(self):
        return self.__age


def ft_garden_security():
    print("=== Garden Security System ===")

    Rose = SecurePlant("Rose", 25, 30)

    print(f"Plant created: {Rose.get_name()}")
    print(f"Height update: {Rose.get_height()}cm [OK]")
    print(f"Age updated: {Rose.get_days()} days [OK]")
    Rose.set_height(-5)

    print(
        f"\nCurrent plant: {Rose.get_name()} "
        f"({Rose.get_height()}cm, {Rose.get_days()} days) "
        )
