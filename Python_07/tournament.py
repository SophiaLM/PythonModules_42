#!/usr/bin/env python3
from ex0 import FlameFactory, WaterFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    InvalidStrategyError,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy
)


def battle(opponents: list) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            print("\n* Battle *")
            factory1, strategy1 = opponents[i]
            factory2, strategy2 = opponents[j]

            c1 = factory1.create_base()
            c2 = factory2.create_base()

            print(c1.describe())
            print("vs.")
            print(c2.describe())
            print("now fight!")

            try:
                strategy1.act(c1)
                strategy2.act(c2)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    flame_f = FlameFactory()
    water_f = WaterFactory()
    heal_f = HealingCreatureFactory()
    trans_f = TransformCreatureFactory()

    n_strat = NormalStrategy()
    a_strat = AggressiveStrategy()
    d_strat = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame_f, n_strat), (heal_f, d_strat)])
    print()

    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame_f, a_strat), (heal_f, d_strat)])
    print()

    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([(water_f, n_strat), (heal_f, d_strat), (trans_f, a_strat)])
