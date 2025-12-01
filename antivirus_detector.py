#!/usr/bin/env python3
"""Detector with a tiny signature database, recursive scanning, and optional quarantine.

Usage examples:
  # Scan current directory non-recursively using bundled signatures
  python3 antivirus_detector.py .

  # Recursive scan and quarantine infected files into ./quarantine
  python3 antivirus_detector.py /path/to/scan --recursive --quarantine-dir quarantine

  # Manage signatures
  python3 antivirus_detector.py --list-signatures
  python3 antivirus_detector.py --add-signature NEW_SIG

This tool is intentionally safe: quarantine moves files into a local folder inside the
project and does not delete anything permanently.
"""
from pathlib import Path
import argparse
import json
import shutil
import sys


DEFAULT_SIGNATURES = "signatures.json"


def load_signatures(path: Path = Path(DEFAULT_SIGNATURES)) -> list:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        if isinstance(data, list):
            return [str(s) for s in data]
    except Exception:
        pass
    return []


def save_signatures(sigs: list, path: Path = Path(DEFAULT_SIGNATURES)) -> None:
    path.write_text(json.dumps(sigs, indent=2))


def signature_marker(signature: str) -> str:
    return f"#INFECTED_BY_{signature}"


def is_infected(path: Path, signatures: list) -> bool:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return False
    for sig in signatures:
        if signature_marker(sig) in text:
            return True
    return False


def scan_path(path: Path, signatures: list, recursive: bool = False):
    found = []
    if path.is_file():
        if is_infected(path, signatures):
            found.append(path)
        return found

    if recursive:
        for p in path.rglob("*"):
            if p.is_file():
                if is_infected(p, signatures):
                    found.append(p)
    else:
        for p in path.iterdir():
            if p.is_file():
                if is_infected(p, signatures):
                    found.append(p)
    return found


def quarantine_files(files: list, quarantine_dir: Path):
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    moved = []
    for f in files:
        try:
            dest = quarantine_dir / f.name
            shutil.move(str(f), str(dest))
            moved.append(dest)
        except Exception:
            pass
    return moved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".", help="file or directory to scan")
    parser.add_argument("--recursive", "-r", action="store_true", help="scan directories recursively")
    parser.add_argument("--signatures", "-s", default=DEFAULT_SIGNATURES, help="path to signatures JSON file")
    parser.add_argument("--quarantine-dir", help="move infected files to this directory (optional)")
    parser.add_argument("--list-signatures", action="store_true", help="list loaded signatures and exit")
    parser.add_argument("--add-signature", help="add a signature to the signatures file and exit")
    parser.add_argument("--remove-signature", help="remove a signature from the signatures file and exit")
    args = parser.parse_args()

    sig_path = Path(args.signatures)
    signatures = load_signatures(sig_path)

    # Management operations
    if args.list_signatures:
        if signatures:
            print("Signatures:")
            for s in signatures:
                print(" -", s)
        else:
            print("No signatures loaded.")
        return

    if args.add_signature:
        new = args.add_signature.strip()
        if new and new not in signatures:
            signatures.append(new)
            save_signatures(signatures, sig_path)
            print(f"Added signature: {new}")
        else:
            print("Signature already present or invalid.")
        return

    if args.remove_signature:
        torem = args.remove_signature.strip()
        if torem in signatures:
            signatures = [s for s in signatures if s != torem]
            save_signatures(signatures, sig_path)
            print(f"Removed signature: {torem}")
        else:
            print("Signature not found.")
        return

    p = Path(args.path)
    if not p.exists():
        print(f"Path not found: {p}")
        sys.exit(2)

    if not signatures:
        print(f"No signatures loaded from {sig_path}. Use --add-signature to add one.")

    found = scan_path(p, signatures, recursive=args.recursive)
    if not found:
        print("No infected files found.")
        return

    for f in found:
        print(f"Infected: {f}")

    if args.quarantine_dir:
        qdir = Path(args.quarantine_dir)
        moved = quarantine_files(found, qdir)
        if moved:
            for m in moved:
                print(f"Quarantined: {m}")


if __name__ == "__main__":
    main()
