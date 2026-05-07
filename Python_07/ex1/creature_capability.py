#!/usr/bin/env python3
from ex0.creature import Creature, CreatureFactory
from ex1.Capability_class import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):

    def heal(self, target=None) -> str:
        if target is None:
            return f"{self.name} heals itself for a small amount"

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"


class Bloomelle(Creature, HealCapability):

    def heal(self, target=None) -> str:
        if target is None:
            return f"{self.name} heals itself and others for a large amount"

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"


class Shiftling(Creature, TransformCapability):
    def __init__(self, name: str, type_name: str):
        super().__init__(name, type_name)
        TransformCapability.__init__(self)

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."


class Morphagon(Creature, TransformCapability):
    def __init__(self, name: str, type_name: str):
        super().__init__(name, type_name)
        TransformCapability.__init__(self)

    def transform(self) -> str:
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        return f"{self.name} stabilizes its form."

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."


class HealingCreatureFactory(CreatureFactory):

    def create_base(self):
        return Sproutling("Sproutling", "Grass")

    def create_evolved(self):
        return Bloomelle("Bloomelle", "Grass/Fairy")


class TransformCreatureFactory(CreatureFactory):

    def create_base(self):
        return Shiftling("Shiftling", "Normal")

    def create_evolved(self):
        return Morphagon("Morphagon", "Normal/Dragon")
