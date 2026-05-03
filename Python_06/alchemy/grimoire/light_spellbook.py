#!/usr/bin/env python3
from alchemy.elements import create_air, create_earth
import elements as els

air = create_air()
earth = create_earth()
fire = els.create_fire()
water = els.create_water()

air_name = air.split()[0]
earth_name = earth.split()[0]
fire_name = fire.split()[0]
water_name = water.split()[0]


def light_spell_allowed_ingredients():
    return [earth_name, air_name, fire_name, water_name]


def light_spell_record(spell_name: str, ingredients: str):
    from .light_validator import validate_ingredients
    result = validate_ingredients(ingredients)
    return (f"Spell recorded: {spell_name} ({result})")
