"""Quick test harness that demonstrates the safe simulator and detector.
It:
 - ensures sample.txt exists
 - creates an infected copy (sample.txt.infected)
 - runs the detector on both original and infected copy
"""
from pathlib import Path
from simulated_virus import infect_file, SIGNATURE
from antivirus_detector import is_infected, scan_dir


def run():
    sample = Path("sample.txt")
    if not sample.exists():
        sample.write_text("This is an auto-created sample file.\n")
    print("Sample file:", sample)
    infected = infect_file(sample)
    print("Infected copy created:", infected)

    print("Detector on original:", "Infected" if is_infected(sample) else "Clean")
    print("Detector on infected copy:", "Infected" if is_infected(infected) else "Clean")

    print("Directory scan result:", scan_dir(Path('.')))


if __name__ == "__main__":
    run()
