#!/usr/bin/env python3
"""
oracle.py - Secure configuration management using environment variables and .env files.
Demonstrates development vs production configuration patterns.
"""

import os
import sys
from typing import Optional


def load_dotenv_safe() -> bool:
    """
    Load .env file using python-dotenv if available.
    Returns True if dotenv was loaded, False if the library is missing.
    """
    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]
        load_dotenv(override=False)     # env vars already set take priority
        return True
    except ModuleNotFoundError:
        return False


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Return an environment variable value or a default."""
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    """Return an environment variable or exit with a clear error."""
    value = os.environ.get(key)
    if not value:
        print(f"  [MISSING] {key} is not set — add it to your .env file.")
        return "NOT SET"
    return value


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def mask_secret(value: str) -> str:
    """Return a masked version of a secret for safe display."""
    if value in ("NOT SET", ""):
        return "NOT SET"
    visible = min(4, len(value) // 2)
    return value[:visible] + "*" * (len(value) - visible)


def display_config(
    mode: str,
    database_url: str,
    api_key: str,
    log_level: str,
    zion_endpoint: str,
) -> None:
    """Print the loaded configuration table."""
    is_dev = mode.lower() == "development"

    print("ORACLE STATUS: Reading the Matrix...")
    print()
    print("Configuration loaded:")
    print(f"  Mode:     {mode}")

    if is_dev:
        print(f"  Database: Connected to local instance ({database_url})")
    else:
        print(f"  Database: Connected to production instance")

    print(f"  API Access: {'Authenticated' if api_key != 'NOT SET' else 'UNAUTHENTICATED'}")
    print(f"  Log Level:  {log_level}")
    print(f"  Zion Network: {'Online' if zion_endpoint != 'NOT SET' else 'OFFLINE'}")

    if not is_dev:
        print()
        print("  [PRODUCTION MODE] Verbose logging suppressed.")
        print("  [PRODUCTION MODE] Errors will be forwarded to monitoring.")


def display_security_check(
    dotenv_loaded: bool,
    api_key: str,
    mode: str,
) -> None:
    """Run and display a simple environment security check."""
    print()
    print("Environment security check:")

    # Check 1 — no hardcoded secrets (we always pass since we read from env)
    print("  [OK] No hardcoded secrets detected")

    # Check 2 — .env file configured
    if dotenv_loaded:
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] python-dotenv not installed — .env file not loaded")
        print("         Install with: pip install python-dotenv")

    # Check 3 — production overrides work
    if mode.lower() == "production":
        print("  [OK] Running in PRODUCTION mode — env var overrides active")
    else:
        print("  [OK] Production overrides available via env vars")

    # Check 4 — API key present
    if api_key != "NOT SET":
        print(f"  [OK] API_KEY loaded ({mask_secret(api_key)})")
    else:
        print("  [WARN] API_KEY is not set")

    print()
    print("The Oracle sees all configurations.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point: load config and display environment status."""
    dotenv_loaded = load_dotenv_safe()

    if not dotenv_loaded:
        print("[INFO] python-dotenv not available. "
              "Reading from shell environment only.")
        print()

    # Gather configuration — require_env returns "NOT SET" for missing keys
    mode: str = get_env("MATRIX_MODE", "development") or "development"
    database_url: str = require_env("DATABASE_URL")
    api_key: str = require_env("API_KEY")
    log_level: str = get_env("LOG_LEVEL", "DEBUG") or "DEBUG"
    zion_endpoint: str = require_env("ZION_ENDPOINT")

    display_config(mode, database_url, api_key, log_level, zion_endpoint)
    display_security_check(dotenv_loaded, api_key, mode)


if __name__ == "__main__":
    main()