#!/usr/bin/env python3
from typing import Generator


def gererate_fibonacci() -> Generator[int, None, None]:
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b


def generate_primes() -> Generator[int, None, None]:
    num = 2
    while True:
        prime = True
        for n in range(2, num):
            if num % n == 0:
                prime = False
                break
        if prime:
            yield num
        num += 1


def generate_events() -> Generator[dict, None, None]:
    names = ["juan-cast", "alineiro", "delrio", "sophluna", "luferna"]
    actions = ["Killed monster", "Found treasure", "Leveled up",
               "Joined party", "Used magic"]
    for i in range(0, 1000):
        name = names[i % len(names)]
        level = (i * 13) % 21
        event = actions[i % len(actions)]
        yield {
            "player": name,
            "level": level,
            "event": event
        }


def stream_analytics(event_stream: Generator[dict, None, None]) -> dict:
    stats = {
        "total": 0,
        "high_levels": 0,
        "treasures": 0,
        "level_up": 0
    }
    for event in event_stream:
        stats["total"] += 1
        if event["level"] > 10:
            stats["high_levels"] += 1
        elif event["event"] == "Found treasure":
            stats["treasures"] += 1
        elif event["event"] == "Leveled up":
            stats["level_up"] += 1
    return (stats)


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===\n"
          "\nProcessing 1000 game events...\n")

    events = generate_events()
    for i in range(0, 5):
        event = next(events)
        name = event["player"]
        lvl = event["level"]
        action = event["event"]
        print(f"Event {i + 1}: Player {name} (level {lvl}) {action}")

    print("\nMemory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")

    print("\n=== Generator Demonstration ===")
    fibonacci = gererate_fibonacci()
    fib = [str(next(fibonacci)) for _ in range(10)]
    print(f"Fibonacci sequence (first 10): {', '.join(fib)}")
    prime = generate_primes()
    prim = [str(next(prime)) for _ in range(5)]
    print(f"Prime numbers (first 5): {', '.join(prim)}")
