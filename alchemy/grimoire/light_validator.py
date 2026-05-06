def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    allowed_list = light_spell_allowed_ingredients()
    ingredients_lower = ingredients.lower().replace(',', '').split()
    print(f"{allowed_list}")
    print(f"{ingredients_lower}")

    if (
        all(x in ingredients_lower for x in allowed_list)
        or all(x in allowed_list for x in ingredients_lower)
    ):
        return f"{ingredients} -> VALID"
    else:
        return f"{ingredients} -> INVALID"
