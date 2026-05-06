#!/usr/bin/env python3
from ..elements import create_air
from elements import create_fire
from ..potions import strength_potion

air = create_air()
fire = create_fire()
strength = strength_potion()


def lead_to_gold() -> str:
    return (
        f"Recipe transmuting Lead to Gold: "
        f"brew '{air}' and '{strength}' mixed with '{fire}'"
        )
