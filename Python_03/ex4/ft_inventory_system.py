#!/usr/bin/env python3
import sys


def get_diccionary() -> dict[str, int]:
    inventory = dict()
    for arg in sys.argv[1:]:
        try:
            if ":" not in arg:
                raise ValueError(f"Error: invalid parameter: {arg}")
            item_name, qty = arg.split(":")
            if item_name in inventory:
                raise ValueError(f"Redundant item '{item_name}' - discarding")
            item_data = {
                "name": item_name,
                "quantity": int(qty),
            }
            inventory.update({item_name: item_data})
        except ValueError as e:
            print(f"{e}")
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
    total = 0
    for data in inventory.values():
        total_qty += data.get("quantity")
        total += 1

    parts = []
    for item in inventory.values():
        name = item["name"]
        quantity = item["quantity"]
        parts.append(f"'{name}:{quantity}'")
    formatted = ", ".join(parts)

    print(f"Got inventory: {formatted}")
    print(f"Total quantity of the {total} items: {total_qty}")

    print("\n=== Current Inventory ===")
    for name, data in inventory.items():
        qty = data.get("quantity")
        percentage = (qty / total_qty) * 100
        print(f"{name}: {qty} units ({percentage:.1f}%)")

    most, least = find_extremes(inventory)
    print("\n=== Inventory Statistics ===")
    print(f"Most abundant: {most.get('name')} with "
          f"({most.get('quantity')} units)")
    print(f"Least abundant: {least.get('name')} "
          f"with ({least.get('quantity')} units)")

    new_dic = {
        "magic_item": {"name": "magic_item", "quantity": 2},
        "magic_sword": {"name": "magic_sword", "quantity": 5}
    }
    new_dic.update(inventory)
    simple_inventory = {}
    for name, data in new_dic.items():
        quantity = data["quantity"]
        simple_inventory[name] = quantity
    print(f"Update inventory: {simple_inventory}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("=== Inventory System Analysis ===")
        inventory_master = get_diccionary()
        inventory_system(inventory_master)
    else:
        print("Error: you need to add more arguments!")
