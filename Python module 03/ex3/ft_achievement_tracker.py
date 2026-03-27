#!/usr/bin/env python3

def achievement_analitics(sophy: set, ali: set, juan: set) -> tuple:
    """
    Perform set operations to analyze player achievements.
    arg: sophy, ali, juan → sets of achievements
    """
    all_unique: set = sophy.union(ali).union(juan)
    common: set = sophy & ali & juan
    rare: set = set()

    for ach in all_unique:
        count: int = 0
        if ach in sophy:
            count += 1
        if ach in ali:
            count += 1
        if ach in juan:
            count += 1
        if count == 1:
            rare.add(ach)

    return (all_unique, common, rare)


def display_results(sophy: set, ali: set, juan: set) -> None:
    """
    Execute the analytics and print the formatted report.
    """
    print(f"Player sophy achievements: {sophy}")
    print(f"Player ali achievements: {ali}")
    print(f"Player juan achievements: {juan}\n")

    all_ach, common, rare = achievement_analitics(sophy, ali, juan)

    print("=== Achievement Analitics ===")
    print(f"All unique achievements: {all_ach}")
    print(f"Total unique achievements: {len(all_ach)}\n")

    print(f"Common to all players: {common}")
    print(f"Rare achievements (1 player): {rare}\n")

    print(f"Sophy vs Ali common: {sophy.intersection(ali)}")
    print(f"Sophy unique: {sophy.difference(ali)}")
    print(f"Ali unique: {ali.difference(sophy)}")


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")

    sophy_ach: set = {
        "first_kill",
        "level_10",
        "treasure_hunter",
        "speed_demon"
        }
    ali_ach: set = {
        "first_kill",
        "level_10",
        "boss_slayer",
        "collector"
        }
    juan_ach: set = {
        "level_10",
        "treasure_hunter",
        "boss_slayer",
        "speed_demon",
        "perfectionist",
    }

    display_results(sophy_ach, ali_ach, juan_ach)
