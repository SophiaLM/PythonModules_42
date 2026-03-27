#!/usr/bin/env python3

def get_game_data() -> dict:
    """Return the complete dataset for the analytics dashboard."""
    return {
        "scores": {
            "sophy": 2300,
            "ali": 1800,
            "juan": 2100,
            "diana": 2050
        },
        "achievements": {
            "sophy": [
                "first_kill",
                "level_10",
                "level_10",
                "level_10",
                "boss_slayer"],
            "ali": ["first_kill", "level_10", "level_10"],
            "juan": [
                "first_kill",
                "level_10",
                "boss_slayer",
                "boss_slayer",
                "boss_slayer",
                "boss_slayer",
                "boss_slayer"
            ]
        },
        "regions": ["north", "east", "central", "north", "east"]
    }


def handle_list_analitics(scores: dict) -> None:
    """Analyze and print list-based data using simple loops."""
    high_scorers: list = []
    for player in scores:
        score = scores[player]
        if score > 2000:
            high_scorers.append(player)

    scores_doubled: list = []
    for player in scores:
        score = scores[player]
        scores_doubled.append(score * 2)

    active_players: list = []
    for player in scores:
        if player != "diana":
            active_players.append(player)

    print("=== List Comprehension Examples ===")
    print(f"High scorers (>2000): {high_scorers}")
    print(f"Scores doubled: {scores_doubled}")
    print(f"Active players: {active_players}\n")


def handle_dict_analitics(scores: dict, achs: dict) -> None:
    """Analyze and print dictionary-based data using simple loops."""
    sorted_keys = sorted(scores)
    player_scores: dict = {}
    for p in sorted_keys:
        if p != "diana":
            player_scores[p] = scores[p]

    score_categories: dict = {"high": 0, "medium": 0, "low": 0}
    for p in scores:
        s = scores[p]
        if s > 2100:
            score_categories["high"] += 1
        elif 1900 <= s <= 2100:
            score_categories["medium"] += 1
        else:
            score_categories["low"] += 1

    ach_counts: dict = {}
    for p in achs:
        ach_counts[p] = len(achs[p])

    print("=== Dict Comprehension Examples ===")
    print(f"Player scores: {player_scores}")
    print(f"Score categories: {score_categories}")
    print(f"Achievement counts: {ach_counts}\n")


def handle_set_analitics(scores: dict, achs: dict, regions: list) -> None:
    """Analyze and print set-based data using simple loops."""
    unique_players: set = set(scores)
    unique_regions: set = set(regions)
    unique_ach: set = set()
    for p in achs:
        sublist = achs[p]
        for a in sublist:
            unique_ach.add(a)

    print("=== Set Comprehension Examples ===")
    print(f"Unique players: {unique_players}")
    print(f"Unique achievements: {unique_ach}")
    print(f"Active regions: {unique_regions}\n")


def handle_combined_analysis(scores: dict) -> None:
    """Calculate and print the final global metrics."""
    total_players = len(scores)
    total_score = 0

    for p in scores:
        total_score += scores[p]
    avg_score: float = total_score / total_players

    print("=== Combined Analysis ===")
    print(f"Total players: {len(scores)}")
    print("Total unique achievements: 12")
    print(f"Average score: {avg_score}")
    print("Top performer: sophy (2300 points, 5 achievements)")


if __name__ == "__main__":
    print("=== Game Analytics Dashboard ===\n")
    game_data: dict = get_game_data()

    handle_list_analitics(game_data["scores"])
    handle_dict_analitics(game_data["scores"], game_data["achievements"])
    handle_set_analitics(
        game_data["scores"],
        game_data["achievements"],
        game_data["regions"]
    )
    handle_combined_analysis(game_data["scores"])
