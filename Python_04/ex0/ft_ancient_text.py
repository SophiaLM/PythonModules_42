#!/usr/bin/env python3

def recovery_system(file_name: str) -> None:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"RECOVERED DATA:\n{content}")
            print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print(f"Caught FileNotFoundError: No such file '{file_name}'")


if __name__ == "__main__":
    file_name = "ancient_fragment.txt"

    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    print(f"Accessing Storage Vault: {file_name}\n"
          "Connection established...\n")
    recovery_system(file_name)
