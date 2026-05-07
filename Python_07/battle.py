#!/usr/bin/env python3
from ex0 import FlameFactory, WaterFactory


def test_factory(factory):
    print("Testing factory")

    base_creature = factory.create_base()
    evolved_creature = factory.create_evolved()

    print(base_creature.describe())
    print(base_creature.attack())

    print(evolved_creature.describe())
    print(evolved_creature.attack())


def battle(factory1, factory2):
    print("Testing battle")

    creature1 = factory1.create_base()
    creature2 = factory2.create_base()

    print(creature1.describe())
    print("vs.")
    print(creature2.describe())

    print("fight!")

    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    water_factory = WaterFactory()

    test_factory(flame_factory)
    print()
    test_factory(water_factory)
    print()
    battle(flame_factory, water_factory)
