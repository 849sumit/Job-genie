"""Entry points and core helpers for Job Genie Backend."""

from __future__ import annotations

def greet(name: str = "World") -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to Job Genie Backend."


def main() -> None:
    """Run the package as a simple CLI."""
    print(greet())


if __name__ == "__main__":
    main()
