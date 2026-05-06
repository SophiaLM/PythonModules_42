#!/usr/bin/env python3
import alchemy

print("=== Alembic 4 ===")
print("Accessing the alchemy module using 'import alchemy'")
print(f"Testing created_air: {alchemy.create_air()}")

print("Now show that not all functions can be reached\n"
      "This will raise an exception!")
print(f"{alchemy.create_earth()}")
