from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count = [0]

    def counter() -> int:
        count[0] += 1
        return count[0]
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total = [initial_power]

    def accumulator(amount: int) -> int:
        total[0] += amount
        return total[0]
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchantment


StoreFunc = Callable[[str, str], None]
RecallFunc = Callable[[str], str]


def memory_vault() -> dict[str, Callable[..., Any]]:
    storage: dict[str, str] = {}

    def store(key: str, value: str) -> None:
        storage[key] = value

    def recall(key: str) -> str:
        return storage.get(key, "Memory not found")
    return {'store': store, 'recall': recall}


if __name__ == "__main__":
    print("Testing mage counter...")
    counter_a = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    counter_b = mage_counter()
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")
    print(f"Base 100, add 30: {acc(30)}")

    print("\nTesting enchantment factory...")
    fire_enchant = enchantment_factory("Flaming")
    print(fire_enchant("Sword"))
    ice_enchant = enchantment_factory("Frozen")
    print(ice_enchant("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault['store']('secret', '42')
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
