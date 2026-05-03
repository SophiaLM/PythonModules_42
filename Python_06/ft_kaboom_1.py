#!/usr/bin/env python3
from alchemy.grimoire.dark_spellbook import dark_spell_record

print("=== Kaboom 1 ===")
print("Access to alchemy/grimoire/dark_spellbook.py directly")
print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")

result = dark_spell_record("Forbidden", "blood, bones")
print(result)
