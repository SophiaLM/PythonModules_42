#!/usr/bin/env python3

def preservation_system(file_content: list) -> None:
    i = 0
    with open("new_discovery.txt", "w", encoding="utf-8") as file:
        print(f"Initializing new storage unit: {file.name}\n"
              "Storage unit created successfully...\n")
        for content in file_content:
            i += 1
            file.write(content + "\n")
            print(f"[Entry 00{i}] {content}")
        print("\nData inscription complete. Storage unit sealed.")
        print(f"Archive '{file.name}' ready for long-term preservation.")


if __name__ == "__main__":
    file_content = [
        "New quantum algorithm discovered",
        "Efficiency increased by 347%",
        "Archived by Data Archivist trainee",
    ]
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    preservation_system(file_content)
