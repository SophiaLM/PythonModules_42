#!/usr/bin/env python3

class Plant:
    type_id = 0

    def __init__(self, name: str, height: int) -> None:
        self.name = name
        self.height = height

    def grow(self) -> None:
        self.height += 1
        print(f"{self.name} grew 1cm")

    def get_info(self) -> str:
        return f"{self.name}: {self.height}cm"


class FloweringPlant(Plant):
    type_id = 1

    def __init__(self, name: str, height: int, color: str) -> None:
        super().__init__(name, height)
        self.color = color

    def get_info(self) -> str:
        return f"{super().get_info()}, {self.color} flowers (blooming)"


class PrizeFlower(FloweringPlant):
    type_id = 2

    def __init__(self, name: str, height: int, color: str, pts: int) -> None:
        super().__init__(name, height, color)
        self.pts = pts

    def get_info(self) -> str:
        return f"{super().get_info()}, Prize points: {self.pts}"


class Garden:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.plants = []
        self.added = 0
        self.total_growth = 0

    def add_plant(self, plant: Plant) -> None:
        self.plants = self.plants + [plant]
        self.added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self) -> None:
        print(f"\n{self.owner} is helping all plants grow...")
        for p in self.plants:
            p.grow()
            self.total_growth += 1


class GardenManager:
    total_gardens = 0

    class GardenStats:
        def __init__(self, plants: list) -> None:
            self.plants = plants

        @staticmethod
        def count_types(plants: list) -> tuple:
            regular = 0
            flowering = 0
            prize = 0
            for p in plants:
                if p.type_id == 0:
                    regular += 1
                elif p.type_id == 1:
                    flowering += 1
                elif p.type_id == 2:
                    prize += 1
            return regular, flowering, prize

        @staticmethod
        def garden_score(plants: list) -> int:
            score = 0
            for p in plants:
                score += p.height
                if p.type_id == 2:
                    score += p.pts * 2
            return score

    def __init__(self) -> None:
        self.gardens = []

    def add_garden(self, garden: Garden) -> None:
        self.gardens = self.gardens + [garden]
        GardenManager.total_gardens += 1

    @classmethod
    def create_garden_network(cls) -> int:
        return cls.total_gardens

    @staticmethod
    def height_validation(plant: Plant) -> bool:
        return plant.height > 0


def main() -> None:
    print("=== Garden Management System Demo ===\n")

    manager = GardenManager()

    sophy_g = Garden("Sophy")
    david_g = Garden("David")

    manager.add_garden(sophy_g)
    manager.add_garden(david_g)

    oak = Plant("Oak Tree", 100)
    rose = FloweringPlant("Rose", 25, "red")
    sunflower = PrizeFlower("Sunflower", 50, "yellow", 10)

    sophy_g.add_plant(oak)
    sophy_g.add_plant(rose)
    sophy_g.add_plant(sunflower)
    sophy_g.grow_all()

    print(f"\n=== {sophy_g.owner}'s Garden Report ===")
    print("Plants in garden:")
    for p in sophy_g.plants:
        print(f"- {p.get_info()}")

    print(
        f"\nPlants added: {sophy_g.added}, "
        f"Total growth: {sophy_g.total_growth}cm"
    )

    stats_helper = GardenManager.GardenStats
    r, f, pf = stats_helper.count_types(sophy_g.plants)
    print(f"Plant types: {r} regular, {f} flowering, {pf} prize flowers")

    is_valid = GardenManager.height_validation(oak)
    print(f"\nHeight validation test: {is_valid}")

    sophy_score = stats_helper.garden_score(sophy_g.plants)
    david_score = stats_helper.garden_score(david_g.plants)
    print(f"Garden scores - {sophy_g.owner}: {sophy_score}, "
          f"{david_g.owner}: {david_score}")

    total_gardens = GardenManager.create_garden_network()
    print(f"Total gardens managed: {total_gardens}")


if __name__ == "__main__":
    main()
