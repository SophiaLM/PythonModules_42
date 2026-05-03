#!/usr/bin/env python3
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_dark_ingredients(ingredients: str) -> str:
    allowed_string = dark_spell_allowed_ingredients()
    allowed_list = allowed_string.split(",")

    is_valid = False
    ingredients_lower = ingredients.lower()

    for item in allowed_list:
        if item.strip().lower() in ingredients_lower:
            is_valid = True
            break

    status = "VALID" if is_valid else "INVALID"
    return (f"{ingredients} - {status}")
