#!/usr/bin/env python3
"""Safe simulator: creates an "infected" copy of a given file by appending a benign marker.
This script is intentionally non-destructive: it never overwrites or deletes existing files.

Usage:
    python3 simulated_virus.py [target_file]

Default target_file: sample.txt
"""
from pathlib import Path
import argparse

SIGNATURE = "SIMULATOR_SIGNATURE_v1"


def infect_file(path: Path, signature: str = SIGNATURE) -> Path:
    """Create a non-destructive "infected" copy of path.

    Returns the Path to the created infected copy.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Target not found: {path}")
    infected_path = path.with_name(path.name + ".infected")
    content = path.read_text()
    marker = f"\n#INFECTED_BY_{signature}\n"
    infected_path.write_text(content + marker)
    return infected_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="sample.txt", help="file to create an infected copy of")
    args = parser.parse_args()
    infected = infect_file(Path(args.target))
    print(f"Created infected copy: {infected}")


if __name__ == "__main__":
    main()
