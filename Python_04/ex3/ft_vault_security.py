#!/usr/bin/env python3

def vault_security_system(file_name: str, secure_type: str) -> None:
    try:
        if secure_type == "EXTRACTION":
            with open(file_name, "r", encoding="utf-8") as file:
                file_content = file.read()
                print(f"SECURE {secure_type}:\n{file_content}\n")
        elif secure_type == "PRESERVATION":
            with open(file_name, "w", encoding="utf-8") as file:
                message = "[CLASSIFIED] New security protocols archived"
                file.write(message)
                print(f"SECURE {secure_type}:\n{message}\n")
    except FileNotFoundError:
        print(f"SECURE {secure_type}:")
        print(f"[ERROR] Access Denied: Vault unit '{file_name}' is missing.")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")

    print("Initiating secure vault access...\n"
          "Vault connection established with failsafe protocols\n")

    vault_security_system("classified_data.txt", "EXTRACTION")
    vault_security_system("security_protocols.txt", "PRESERVATION")

    print("Vault automatically sealed upon completion\n"
          "All vault operations completed with maximum security.")
