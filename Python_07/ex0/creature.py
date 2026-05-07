#!/usr/bin/env python3
from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, type_name: str):
        self.name = name
        self.type = type_name

    @abstractmethod
    def attack(self):
        pass

    def describe(self):
        return f"{self.name} is a {self.type} type creature!"


class Flameling(Creature):
    def attack(self):
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"


class CreatureFactory(ABC):

    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):

    def create_base(self) -> Creature:
        return Flameling("Flameling", "Fyre")

    def create_evolved(self) -> Creature:
        return Pyrodon("Pyrodon", "Fire/Flying")


class WaterFactory(CreatureFactory):

    def create_base(self) -> Creature:
        return Aquabub("Aquabub", "Water")

    def create_evolved(self) -> Creature:
        return Torragon("Torragon", "Water")
