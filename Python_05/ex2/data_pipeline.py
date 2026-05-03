#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVPlugin:
    def process_output(self, raw_data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        messages = [content for rank, content in raw_data]
        print(",".join(messages))


class JSONPlugin:
    def process_output(self, raw_data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        json_entries = []
        for rank, content in raw_data:
            entry = f'"item_{rank}": "{content}"'
            json_entries.append(entry)

        final_json = "{" + ", ".join(json_entries) + "}"
        print(final_json)


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
                print(f"DataStream error - Can't process: {element}")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            collected = []
            for _ in range(nb):
                if proc.storage:
                    collected.append(proc.output())
            if collected:
                plugin.process_output(collected)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            print(f"{proc.name}: total {proc.total_processed} items processed,"
                  f" remaining {len(proc.storage)} on processor")


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("Registering Processors")
    num_p, text_p, log_p = NumericProcessor(), TextProcessor(), LogProcessor()
    ds.register_processor(num_p)
    ds.register_processor(text_p)
    ds.register_processor(log_p)

    groups1 = [
        'Hello world', [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
        42, ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {groups1}")
    ds.process_stream(groups1)
    ds.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, CSVPlugin())
    ds.print_processors_stats()

    groups2 = [
        21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [{'log_level': 'ERROR', 'log_message': '500 server crash'},
         {'log_level': 'NOTICE',
          'log_message': 'Certificate expires in 10 days'}],
        [32, 42, 64, 84, 128, 168], 'World hello'
    ]

    print(f"Send another batch of data: {groups2}")
    ds.process_stream(groups2)
    ds.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, JSONPlugin())
    ds.print_processors_stats()
