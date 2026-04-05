#!/usr/bin/env python3
from typing import Generator
import random


def get_events() -> Generator[dict, None, None]:
    names = [
                "juan-cast", "alineiro", "delrio", "sophluna", "luferna"
            ]
    actions = [
                "Killed monster", "Found treasure", "Leveled up",
                "Joined party", "Used magic", "Completed quest",
                "Opened chest", "Defeated boss", "Took damage",
            ]
    for i in range(0, 1000):
        name = random.choice(names)
        event = random.choice(actions)
        yield {
            "player": name,
            "event": event
        }


def consume_event(event_list: list):
    while event_list:
        event = random.choice(event_list)
        event_list.remove(event)
        yield event


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===\n"
          "=== Processing 1000 game events ===\n")

    events = get_events()
    for i in range(0, 1000):
        event = next(events)
        name = event["player"]
        action = event["event"]
        print(f"Event {i + 1}: Player {name} {action}")

    event_list = []
    gen_event_list = get_events()
    for _ in range(0, 10):
        event = next(gen_event_list)
        event_list.append(event)

    print(f"\nbuilt list of: {event_list}")
    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Reamins in list: {event_list}")
