# #!/usr/bin/env python3
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt


# def check_dependencies() -> None:
#     print("LOADING STATUS: Loading programs...\n")
#     print("Checking dependencies:")

#     dependencies = [
#         ("pandas", "2.1.0", "Data manipulation ready"),
#         ("numpy", "1.25.0", "Numerical computation ready"),
#         ("requests", "2.31.0", "Network access ready"),
#         ("matplotlib", "3.7.2", "Visualization ready"),
#     ]

#     all_ok = True
#     for dep, ver, msg in dependencies:
#         try:
#             __import__(dep)
#             print(f"[OK] {dep} ({ver}) - {msg}")
#         except ModuleNotFoundError:
#             print(f"[Error] {dep} ({ver}) is missing!")
#             all_ok = False

#     if not all_ok:
#         print("\nMissing dependencies found!")
#         print("To install with pip: pip install -r requirements.txt")
#         print("To install with Poetry: poetry install")


# def matrix_data() -> None:
#     print("Analyzing Matrix data...")
#     numpydata = np.random.randn(1000)
#     print(f"Processing {len(numpydata)} data points...")

#     pandadata = pd.DataFrame(numpydata, columns=['Signal'])
#     print("Generating visualization...")
#     plt.figure(figsize=(10, 5))
#     plt.plot(pandadata['Signal'], color='green', linewidth=0.5)
#     plt.title("Matrix Data Analysis")
#     plt.savefig("matrix_analysis.png")

#     print("Analysis complete!")
#     print("Results saved to: matrix_analysis.png")



# if __name__ == "__main__":
#     check_dependencies()
#     matrix_data()


#!/usr/bin/env python3
"""
loading.py - Matrix data analysis using pandas, numpy, and matplotlib.
Demonstrates package management with pip and Poetry.
"""

import sys
import importlib
import importlib.metadata
from types import ModuleType
from typing import Optional


REQUIRED_PACKAGES: list[tuple[str, str]] = [
    ("pandas", "Data manipulation ready"),
    ("numpy", "Numerical computation ready"),
    ("matplotlib", "Visualization ready"),
]


def get_package_version(name: str) -> str:
    """Return the installed version of a package, or 'unknown'."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def try_import(name: str) -> Optional[ModuleType]:
    """Attempt to import a module; return None if not available."""
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        return None


def check_dependencies() -> bool:
    """
    Check that all required packages are importable.
    Print status for each and return True only if all are present.
    """
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    all_ok: bool = True
    for package, description in REQUIRED_PACKAGES:
        mod = try_import(package)
        if mod is not None:
            version = get_package_version(package)
            print(f"  [OK] {package} ({version}) - {description}")
        else:
            print(f"  [MISSING] {package} - NOT installed")
            all_ok = False

    if not all_ok:
        print()
        print("ERROR: Missing dependencies. Install them with:")
        print("  pip:    pip install -r requirements.txt")
        print("  Poetry: poetry install")

    return all_ok


def show_package_manager_info() -> None:
    """Print a comparison between pip and Poetry dependency management."""
    print()
    print("=" * 50)
    print("DEPENDENCY MANAGER COMPARISON")
    print("=" * 50)
    print()
    print("pip (requirements.txt):")
    print("  - Simple, built into Python")
    print("  - Installs packages globally or in active venv")
    print("  - No lock file by default (use pip freeze)")
    print("  - Command: pip install -r requirements.txt")
    print()
    print("Poetry (pyproject.toml):")
    print("  - Manages venv, deps, and packaging in one tool")
    print("  - Generates poetry.lock for reproducible installs")
    print("  - Separates dev and prod dependencies cleanly")
    print("  - Command: poetry install")
    print("=" * 50)


def run_analysis() -> None:
    """
    Generate simulated Matrix data with numpy, analyse with pandas,
    and save a matplotlib visualisation.
    """
    # Late imports — only called after dependency check passes
    import numpy as np          # type: ignore[import-untyped]
    import pandas as pd         # type: ignore[import-untyped]
    import matplotlib           # type: ignore[import-untyped]
    matplotlib.use("Agg")       # non-interactive backend (no display needed)
    import matplotlib.pyplot as plt  # type: ignore[import-untyped]

    print()
    print("Analyzing Matrix data...")

    # numpy is the sole source of the dataset (no hardcoded lists / range())
    rng = np.random.default_rng(seed=42)
    raw: np.ndarray = rng.standard_normal(1000)
    print(f"Processing {len(raw)} data points...")

    df: pd.DataFrame = pd.DataFrame(
        {
            "index": np.arange(len(raw)),
            "signal": raw,
            "rolling_mean": pd.Series(raw).rolling(window=50).mean().to_numpy(),
        }
    )

    # Basic statistics
    stats: pd.Series = df["signal"].describe()  # type: ignore[assignment]
    print(f"  Mean:   {stats['mean']:.4f}")
    print(f"  Std:    {stats['std']:.4f}")
    print(f"  Min:    {stats['min']:.4f}")
    print(f"  Max:    {stats['max']:.4f}")

    print("Generating visualization...")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Matrix Signal Analysis", fontsize=14)

    # Signal over time
    axes[0].plot(df["index"], df["signal"],
                 color="green", linewidth=0.5, alpha=0.7, label="Signal")
    axes[0].plot(df["index"], df["rolling_mean"],
                 color="red", linewidth=1.5, label="Rolling mean (50)")
    axes[0].set_title("Signal over time")
    axes[0].set_xlabel("Index")
    axes[0].set_ylabel("Value")
    axes[0].legend()

    # Histogram
    axes[1].hist(df["signal"], bins=40, color="green", edgecolor="black", alpha=0.7)
    axes[1].set_title("Signal distribution")
    axes[1].set_xlabel("Value")
    axes[1].set_ylabel("Frequency")

    plt.tight_layout()
    output_file = "matrix_analysis.png"
    plt.savefig(output_file, dpi=150)
    plt.close(fig)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    """Entry point."""
    ok = check_dependencies()
    if not ok:
        sys.exit(1)

    show_package_manager_info()
    run_analysis()


if __name__ == "__main__":
    main()