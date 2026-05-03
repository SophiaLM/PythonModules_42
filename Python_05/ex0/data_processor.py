#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.storage = []
        self.rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.storage:
            raise ValueError("No data output")
        data = self.storage.pop(0)
        current_rank = self.rank
        self.rank += 1

        return (current_rank, data)


class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self.validate(item) for item in data)
        try:
            float(data)
            return True
        except (ValueError, TypeError):
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:

        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self.storage.append(str(item))
        else:
            self.storage.append(str(data))


class TextProcessor(DataProcessor):
    def __init__(self):
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            self.storage.extend(data)
        else:
            self.storage.append(data)


class LogProcessor(DataProcessor):
    def __init__(self):
        super().__init__("Log Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not self.validate(item):
                    return False
            return True

        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False
            return True
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            items = data
        else:
            items = [data]

        for entry in items:
            parts = []
            for value in entry.values():
                parts.append(value)
            formatted_log = ": ".join(parts)
            self.storage.append(formatted_log)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    num = NumericProcessor()

    print(f"Trying to validate input '42': {num.validate("42")}")
    print(f"Trying to validate input 'Hello': {num.validate("Hello")}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    num_data = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    num.validate(num_data)
    num.ingest(num_data)

    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num.output()
        print(f"Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()

    print(f"Trying to validate input '42': {text_proc.validate(42)}")

    text_data = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_data}")
    text_proc.ingest(text_data)

    print("Extracting 1 value...")
    rank, val = text_proc.output()
    print(f"Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()

    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")
