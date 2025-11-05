#!/usr/bin/env python3
"""Simple detector for the simulator signature.

Usage:
    python3 antivirus_detector.py [path]
If path is a directory, scans files in the directory (non-recursive) and reports infected files.
If path is a file, prints "Infected" or "Clean".
"""
from pathlib import Path
import argparse

SIGNATURE = "SIMULATOR_SIGNATURE_v1"


def is_infected(path: Path, signature: str = SIGNATURE) -> bool:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return False
    return f"#INFECTED_BY_{signature}" in text


def scan_dir(dir_path: Path, signature: str = SIGNATURE):
    found = []
    for p in dir_path.iterdir():
        if p.is_file():
            if is_infected(p, signature):
                found.append(p)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    p = Path(args.path)
    if p.is_dir():
        found = scan_dir(p)
        if found:
            for f in found:
                print(f"Infected: {f}")
        else:
            print("No infected files found.")
    else:
        print("Infected" if is_infected(p) else "Clean")


if __name__ == "__main__":
    main()
