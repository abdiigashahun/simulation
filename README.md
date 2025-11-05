# Safe Malware Study: Simulator + Detector (Python)

Important: I will not create real malware or code that spreads, infects other systems, or damages data. That would be unsafe and against policy and law.

This repository provides a safe, non-destructive educational simulation of how a virus might "mark" a file and how a simple antivirus scanner could detect that mark.

Files added:

- `simulated_virus.py` — a safe simulator that creates an "infected" copy of a target file by appending a benign marker. It never overwrites the original and does not spread.
- `antivirus_detector.py` — a simple detector that looks for the simulator's benign marker in files.
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

If you'd like, I can extend the detector to use file hashing, maintain a local signature database, or add unit tests. Tell me which safe direction you'd like to explore next.
