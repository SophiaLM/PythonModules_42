#!/usr/bin/env python3
from alchemy.transmutation import recipes

print("=== Transmutation 1 ===")
print("Import transmutation module directly")
lead_gold = recipes.lead_to_gold()
print(f"Testing lead_to_gold: {lead_gold}")
