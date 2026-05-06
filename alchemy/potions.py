#!/usr/bin/env python3
import elements
from . import elements as els


def strength_potion() -> str:
    fire = elements.create_fire()
    water = elements.create_water()
    return f"Strength potion brewed with '{fire}' and '{water}'"


def healing_potion() -> str:
    air = els.create_air()
    earth = els.create_earth()
    return f"Strength potion brewed with '{earth}' and '{air}'"
