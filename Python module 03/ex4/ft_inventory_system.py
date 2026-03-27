#!/usr/bin/env python3
import sys


def get_inventory() -> dict:
    """
    Creates the inventory using a nested dictionary structure.
    Args: sys.argv[1:] → list of strings 'item:qty'
    Nested structure as requested by subject.
    """
    inventory = dict()
    for arg in sys.argv[1:]:
        try:
            name, qty = arg.split(":")
            item_data = {
                "name": name,
                "type": "General",
                "quantity": int(qty),
                "value": 10
            }
            inventory.update({name: item_data})
        except ValueError:
            continue
    return (inventory)


def find_extremes(inventory: dict) -> tuple:
    """
    Finds the most and least abundant items manually.
    """
    most_item = None
    least_item = None

    for name, data in inventory.items():
        qty = data.get("quantity")
        if most_item is None or qty > most_item.get("quantity"):
            most_item = data
        if least_item is None or qty < least_item.get("quantity"):
            least_item = data
    return (most_item, least_item)


def inventory_system(inventory: dict) -> None:
    """
    Generates and prints the inventory report.
    """
    total_qty = 0
    for data in inventory.values():
        total_qty += data.get("quantity")

    print("=== Inventory System Analysis ===\n")
    print(f"Total items in inventory: {total_qty}")
    print(f"Unique item types: {len(inventory.keys())}\n")

    print("=== Current Inventory ===")
    for name, data in inventory.items():
        qty = data.get("quantity")
        percentage = (qty / total_qty) * 100
        print(f"{name}: {qty} units ({percentage:.1f}%)")

    most, least = find_extremes(inventory)
    print("\n=== Inventory Statistics ===")
    print(f"Most abundant: {most.get('name')} ({most.get('quantity')} units)")
    print(f"Least abundant: {least.get('name')} "
          f"({least.get('quantity')} units)")

    categories = {"Moderate": {}, "Scarce": {}}
    restock = []

    for name, data in inventory.items():
        qty = data.get("quantity")
        if qty >= 4:
            categories["Moderate"].update({name: qty})
        else:
            categories["Scarce"].update({name: qty})
        if qty == 1:
            restock.append(name)

    print("\n=== Item Categories ===")
    print(f"Moderate: {categories.get('Moderate')}")
    print(f"Scarce: {categories.get('Scarce')}")

    print("\n=== Management Suggestions ===")
    print(f"Restock needed: {', '.join(restock)}")

    print("\n=== Dictionary Properties Demo ===")
    print(f"Dictionary keys: {', '.join(inventory.keys())}")

    val_list = []
    for data in inventory.values():
        val_list.append(str(data.get("quantity")))

    print(f"Dictionary values: {', '.join(val_list)}")
    print(f"Sample lookup - 'sword' in inventory: {'sword' in inventory}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        inventory_master = get_inventory()
        inventory_system(inventory_master)
    else:
        print("Error: you need to add more arguments!")
