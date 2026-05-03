#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, name: str):
        self.name = name
        self.storage: list[str] = []
        self.rank = 0
        self.total_processed = 0

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
            for item in data:
                if not self.validate(item):
                    return False
            return True
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
                self.total_processed += 1
        else:
            self.storage.append(str(data))
            self.total_processed += 1


class TextProcessor(DataProcessor):
    def __init__(self):
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
            return True
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self.storage.append(item)
                self.total_processed += 1
        else:
            self.storage.append(data)
            self.total_processed += 1


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

        items = data if isinstance(data, list) else [data]
        for entry in items:
            parts = []
            for value in entry.values():
                parts.append(value)
            formatted_log = ": ".join(parts)
            self.storage.append(formatted_log)
            self.total_processed += 1


class DataStream:
    def __init__(self):
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                err_msg = "DataStream error - Can't process element in stream"
                print(f"{err_msg}: {element}")

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data\n")
            return
        for proc in self.processors:
            print(f"{proc.name}: total {proc.total_processed} items processed,"
                  f" remaining {len(proc.storage)} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...\n")
    ds = DataStream()
    ds.print_processors_stats()

    print("Registering Numeric Processor\n")
    num_p = NumericProcessor()
    ds.register_processor(num_p)

    groups = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING', 'log_message': 'Telnet access!'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]

    print("Send first groups of goups on stream:", groups)
    ds.process_stream(groups)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    text_p = TextProcessor()
    log_p = LogProcessor()
    ds.register_processor(text_p)
    ds.register_processor(log_p)

    print("Send the same batch again")
    ds.process_stream(groups)
    ds.print_processors_stats()

    msg = "Consume elements from the data processors: Numeric 3, Text 2, Log 1"
    print(msg)
    for _ in range(3):
        num_p.output()
    for _ in range(2):
        text_p.output()
    for _ in range(1):
        log_p.output()

    ds.print_processors_stats()
