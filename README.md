1# Safe Malware Study: Simulator + Detector (Python)

Important: I will not create real malware or code that spreads, infects other systems, or damages data. That would be unsafe and against policy and law.

This repository provides a safe, non-destructive educational simulation of how a virus might "mark" a file and how a simple antivirus scanner could detect that mark.

Files added:

- `simulated_virus.py` — a safe simulator that creates an "infected" copy of a target file by appending a benign marker. It never overwrites the original and does not spread.
- `antivirus_detector.py` — a detector that uses a tiny JSON-based signature database, supports recursive scanning, and can optionally quarantine infected files.
- `signatures.json` — a small JSON array containing signature IDs used by the detector.
- `sample.txt` — a harmless sample file used for the demo.
- `tests.py` — a small test harness that runs the simulator and detector and prints results.

Usage (run in this folder):

```bash
python3 tests.py
```

This will create `sample.txt.infected` and demonstrate that the detector flags the infected copy while leaving the original clean.

Safety notes:

- NEVER run malware on real data or outside of a sandbox. Use virtual machines or disposable containers for experiments.
- The provided code is intentionally harmless. It writes a separate file and detects a plaintext marker.

Additional features (safe and educational):

- Signature database: `signatures.json` contains an array of signature IDs used by the detector. You can add/remove signatures with the detector's CLI flags.
- Recursive scan: pass `--recursive` (or `-r`) to scan directories recursively.
- Quarantine: pass `--quarantine-dir <dir>` to move detected files into a quarantine folder (no permanent deletion).

Examples:

```bash
# list signatures
python3 antivirus_detector.py --list-signatures

# add a signature
python3 antivirus_detector.py --add-signature SIMULATOR_SIGNATURE_v2

# scan current directory recursively and quarantine infected files
python3 antivirus_detector.py . --recursive --quarantine-dir quarantine
```

If you'd like any of these safe extensions implemented (hashing, improved quarantine, unit tests, or a small UI), tell me which and I'll add it.
