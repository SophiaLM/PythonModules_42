#!/usr/bin/env python3


import random


def handle_list_transformation(players: list) -> list:
    print("=== List Comprehension Examples ===")

    all_cap = [name.capitalize() for name in players]
    only_init_cap = [name for name in players if name.istitle()]

    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {all_cap}")
    print(f"New list of capitalized names only: {only_init_cap}\n")

    return all_cap


def handle_dict_analysis(capitalized_names: list) -> dict:
    print("=== Dict Comprehension Examples ===")

    score_dict = {name: random.randint(50, 1000) for name in capitalized_names}

    avg = sum(score_dict.values()) / len(score_dict)
    high_scores = {
        name: score for name, score in score_dict.items() if score > avg
    }

    print(f"Score dict: {score_dict}")
    print(f"Score average is {avg:.2f}")
    print(f"High scores: {high_scores}\n")

    return score_dict


def handle_set_analysis(user_regions: list) -> None:
    print("=== Set Comprehension Examples ===")

    unique_regions = {region for region in user_regions}

    print(f"Active regions (unique): {unique_regions}")


def data_alchemist():
    print("=== Game Data Alchemist ===\n")

    initial_players = [
        'Alice', 'BOB', 'CharLie', 'dylan', 'Emma',
        'Gregory', 'john', 'kEvin', 'Liam'
    ]
    raw_regions = ["north", "east", "central", "north", "east"]

    processed_names = handle_list_transformation(initial_players)
    handle_dict_analysis(processed_names)
    handle_set_analysis(raw_regions)


if __name__ == "__main__":
    data_alchemist()
