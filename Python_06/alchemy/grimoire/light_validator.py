def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    allowed_list = light_spell_allowed_ingredients()
    ingredients_lower = ingredients.lower()
    is_valid = False

    for allowed in allowed_list:
        allowed_lower = str(allowed).lower()
        if allowed_lower in ingredients_lower:
            is_valid = True
            break

    if is_valid:
        return f"{ingredients} -> VALID"
    else:
        return f"{ingredients} -> INVALID"
