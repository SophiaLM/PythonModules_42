#!/usr/bin/env python3

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def get_info(self):
        return (f"{self.name}: {self.height}cm, {self.age} days")


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def get_info(self):
        return (f"{super().get_info()}, {self.color} color")


class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def get_info(self):
        return (f"{super().get_info()}, trunk {self.trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(self, name, height, age, hearvest_season):
        super().__init__(name, height, age)
        self.hearvest_season = hearvest_season

    def get_info(self):
        return f"{super().get_info()}, harvest in {self.hearvest_season}"


def ft_plant_types():
    print("=== Garden Plant Types ===\n")

    Rose = Flower("Rose", 25, 30, "red")
    Oak = Tree("Oak", 500, 1825, 50)
    Tomato = Vegetable("Tomato", 80, 90, "summer")

    print(Rose.get_info())
    print("Rose is blooming beautifully!\n")

    print(Oak.get_info())
    print("Oak provides 78 square meters of shade\n")

    print(Tomato.get_info())
    print("Tomato is rich in vitamin C")
