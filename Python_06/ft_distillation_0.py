#!/usr/bin/env python3
from alchemy import potions


healing = potions.healing_potion()
strength = potions.strength_potion()

print("=== Distillation 0 ===")
print("Direct access to alchemy/potions.py")
print(f"Testing strength_potion: {strength}")
print(f"Testing healing_potion: {healing}")
