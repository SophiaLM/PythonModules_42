#!/usr/bin/env python3

def crisis_response(file_name: str) -> None:
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            file_content = file.read()
            print(f"ROUTINE ACCESS: Attempting access to '{file_name}'...")
            print(f"SUCCESS: Archive recovered - {file_content}")
            status_msg = "Normal operations resumed"
    except FileNotFoundError:
        print(f"CRISIS ALERT: Attempting access to '{file_name}'...")
        print("RESPONSE: Archive not found in storage matrix")
        status_msg = " Crisis handled, security maintained"
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        status_msg = "Crisis handled, system stable"
    except Exception as error:
        print(f"RESPONSE: Unexpected system anomaly - {error}")
        status_msg = "Crisis handled, emergency protocols active"
    finally:
        print(f"STATUS: {status_msg}")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")

    crisis_response("lost_archive.txt")
    print("")
    crisis_response("classified_data.txt")
    print("")
    crisis_response("standar_archive.txt")
