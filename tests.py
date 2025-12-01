"""Quick test harness that demonstrates the safe simulator and detector.
It:
 - ensures sample.txt exists
 - creates an infected copy (sample.txt.infected)
 - runs the detector on both original and infected copy
"""
from pathlib import Path
import subprocess
from simulated_virus import infect_file


def run():
    sample = Path("sample.txt")
    if not sample.exists():
        sample.write_text("This is an auto-created sample file.\n")
    print("Sample file:", sample)
    infected = infect_file(sample)
    print("Infected copy created:", infected)

    # Use the improved detector CLI
    print('\n-- Detector on original --')
    subprocess.run(["python3", "antivirus_detector.py", str(sample)])

    print('\n-- Detector on infected copy --')
    subprocess.run(["python3", "antivirus_detector.py", str(infected)])

    print('\n-- Directory scan (non-recursive) --')
    subprocess.run(["python3", "antivirus_detector.py", "."])

    print('\n-- Directory scan (recursive) --')
    subprocess.run(["python3", "antivirus_detector.py", ".", "--recursive"])


if __name__ == "__main__":
    run()
