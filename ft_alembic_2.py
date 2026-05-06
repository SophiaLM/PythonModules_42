#!/usr/bin/env python3
import alchemy.elements

print("=== Alembic 2 ===")
print("Accessing alchemy/elements.py using 'import ...' structure")
eart = alchemy.elements.create_earth()
print(f"Testing create_earth: {eart}")
