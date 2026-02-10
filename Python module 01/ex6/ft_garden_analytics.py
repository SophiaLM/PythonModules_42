#!/usr/bin/env python3

class Plant:
    type_id = 0

    def __init__(self, name, height):
        self.name = name
        self.height = height

    def grow(self):
        self.height += 1
        print(f"{self.name} grew 1cm")

    def get_info(self):
        return f"{self.name}: {self.height}cm"


class FlowerinPlant(Plant):
    type_if = 1

    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color

    def get_info(self):
        return f"{super().get_info()}, {self.color} flowers (blooming)"


class PriceFlower(FlowerinPlant):
    type_id = 2

    def __init__(self, name, height, color, pts):
        super().__init__(name, height, color)
        self.pts = pts

    def get_info(self):
        return f"{super().get_info()}, price point: {self.pts}"


class Garden:
    def __init__(self, owner):
        self.owner = owner
        self.Plant = []
        self.added = 0
        self.total_growth = 0

    def add_plant(self, plant):
        self.Plant = self.Plant + [plant]
        self.added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self):
        print(f"{self.owner} is helping all plants grow")
        for p in self.Plant:
            p.grow()
            self.total_growth += 1


class GardenManager:
    total_garden = 0

    @staticmethod
    def count_types(Plant):
        r = 0
        f = 0
        pf = 0
        for p in Plant:
            if p.type_id == 0:
                r += 1
            elif p.type_id == 1:
                f += 1
            else:
                pf += 1
        return r, f, pf

    def __init__(self):
        self.gardens = []
        GardenManager.total_garden += 1

    def add_garden(self, garden):
        self.gardens = self.gardens + [garden]

    @classmethod
    def created_garden_network(cls):
        return cls.total_garden

    @staticmethod
    def height_validation(plant):
        if plant.height > 0:
            return ("True")
        else:
            return ("False")


print("=== Garden Management System Demo ===")

manager = GardenManager()

sophy_g = Garden("Sophy")
david_g = Garden("David")

manager.add_garden(sophy_g)
manager.add_garden(david_g)

Oak = Plant("Oak Tree", 100)
Rose = FlowerinPlant("Rose", 25, "red")
Sunflower = PriceFlower("Sunflower", 50, "yellow", 10)

sophy_g.add_plant(Oak)
sophy_g.add_plant(Rose)
sophy_g.add_plant(Sunflower)
sophy_g.grow_all()

print(f"\n=== {sophy_g.owner}'s Garden Report ===")
print("Plants in garden:")
for p in sophy_g.Plant:
    print(f"- {p.get_info()}")

print(
    f"Plants added: {sophy_g.owner}, "
    f"Total growth: {sophy_g.total_growth}cm"
    )

stats_helper = GardenManager
r = stats_helper.count_types(sophy_g.Plant)
f = stats_helper.count_types(sophy_g.Plant)
pf = stats_helper.count_types(sophy_g.Plant)
print(
    f"Plant types: {r} regular, {f} flowering, "
    f"{pf} prize flowers"
    )

is_valid = GardenManager.height_validation(Oak)
print(f"Height validation test: {is_valid}")

total_gardens = GardenManager.created_garden_network()
print(f"Total gardens managed: {total_gardens}")
