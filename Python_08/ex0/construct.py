# #!/usr/bin/env python3
# import sys
# import site
# import os


# if __name__ == "__main__":
#     inside_venv = sys.prefix != sys.base_prefix

#     if not inside_venv:
#         print("Outside the Matrix")
#         print("$> python construct.py")

#         print("MATRIX STATUS: You're still plugged in")
#         print()
#         print(f"Current Python: {sys.executable}")
#         print("Virtual Environment: None detected")
#         print()
#         print("WARNING: You're in the global environment!")
#         print("The machines can see everything you install.")
#         print()
#         print("To enter the construct, run:")
#         print("python -m venv matrix_env")
#         print("source matrix_env/bin/activate # On Unix")
#         print("matrix_env\\Scripts\\activate # On Windows")
#         print()
#         print("Then run this program again.")

#     else:
#         print("MATRIX STATUS: Welcome to the construct\n")

#         current = sys.executable
#         venv_name = os.path.basename(sys.prefix)
#         venv_path = sys.prefix
#         packages_path = site.getsitepackages()[0]

#         print(f"Current Python: {current}")
#         print(f"Virtual Enviroment: {venv_name}")
#         print(f"Enviroment Path: {venv_path}")
#         print()
#         print("SUCCESS: You're in an isolated environment!")
#         print("Safe to install packages without affecting")
#         print("the global system.")
#         print()
#         print("Package installation path:")
#         print(packages_path)


#!/usr/bin/env python3
"""
construct.py - Detecting and displaying Python virtual environment information.
"""

import os
import sys
import site


def get_venv_name() -> str:
    """Return the name of the active virtual environment, or empty string."""
    return os.path.basename(sys.prefix)


def get_site_packages() -> str:
    """Return the first site-packages path available."""
    packages = site.getsitepackages()
    return packages[0] if packages else "Unknown"


def display_outside_venv() -> None:
    """Display information and instructions when not in a virtual environment."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("    python -m venv matrix_env")
    print("    source matrix_env/bin/activate  # On Unix")
    print("    matrix_env\\Scripts\\activate      # On Windows")
    print()
    print("Then run this program again.")


def display_inside_venv() -> None:
    """Display environment details when running inside a virtual environment."""
    venv_name: str = get_venv_name()
    venv_path: str = sys.prefix
    packages_path: str = get_site_packages()

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(f"    {packages_path}")


def is_virtual_env() -> bool:
    """Detect whether the script is running inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def main() -> None:
    """Entry point: detect environment and display appropriate output."""
    if is_virtual_env():
        display_inside_venv()
    else:
        display_outside_venv()


if __name__ == "__main__":
    main()