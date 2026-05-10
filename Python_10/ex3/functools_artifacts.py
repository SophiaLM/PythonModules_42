import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    def max_op(a: int, b: int) -> int:
        return a if a > b else b

    def min_op(a: int, b: int) -> int:
        return a if a < b else b

    operations: dict[str, Callable[[list[int]], int]] = {
        'add': functools.partial(functools.reduce, operator.add),
        'multiply': functools.partial(functools.reduce, operator.mul),
        'max': functools.partial(functools.reduce, max_op),
        'min': functools.partial(functools.reduce, min_op)
    }
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    return operations[operation](spells)


EnchantFunc = Callable[..., str]


def partial_enchanter(
    base_enchantment: EnchantFunc
) -> dict[str, Callable[[str], str]]:
    fire = functools.partial(base_enchantment, power=50, element='fire')
    ice = functools.partial(base_enchantment, power=50, element='ice')
    ltn = functools.partial(base_enchantment, power=50, element='lightning')
    return {'fire': fire, 'ice': ice, 'lightning': ltn}


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


@functools.singledispatch
def spell_dispatcher(arg: Any) -> str:
    return "Unknown spell type"


@spell_dispatcher.register
def _(arg: int) -> str:
    return f"Damage spell: {arg} damage"


@spell_dispatcher.register
def _(arg: str) -> str:
    return f"Enchantment: {arg}"


@spell_dispatcher.register(list)
def _(_arg: list) -> str:  # type: ignore[type-arg]
    return f"Multi-cast: {len(_arg)} spells"


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element} enchantment with {power} power on {target}"


if __name__ == "__main__":
    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting spell dispatcher...")
    print(spell_dispatcher(42))
    print(spell_dispatcher("fireball"))
    print(spell_dispatcher(["spell1", "spell2", "spell3"]))
    print(spell_dispatcher(3.14))
