"""Step 0: rebuild the UN troop-contribution data with project #11, pinned to its v1.0.0 release.

This repository does not contain any UN figures: the UN's terms of use do not allow its
data to be redistributed. Instead, this script

  1. clones peacekeeping-tracker at tag v1.0.0 into external/peacekeeping-tracker
     (Azom 2026, https://doi.org/10.5281/zenodo.23752307),
  2. runs its code/01_download.py (downloads the UN files from the UN),
  3. runs its code/02_build_panel.py (builds data/build/contributions_monthly.csv),
  4. runs its code/03_check.py, which confirms the rebuild matches the v1.0.0 release,
  5. stops with an error if any of these fail or the check does not pass.

Needs git and an internet connection.

Usage:  python code/00_get_un_data.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / "external" / "peacekeeping-tracker"
REPO = "https://github.com/Affnann/peacekeeping-tracker"
TAG = "v1.0.0"
# Commit that tag v1.0.0 points to; guards against the tag being moved.
TAG_COMMIT = "f391c51"


def run(cmd, cwd=None):
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    if not EXT.exists():
        EXT.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--quiet", "--depth", "1", "--branch", TAG, REPO, str(EXT)])
    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=EXT,
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != TAG_COMMIT:
        sys.exit(f"external/peacekeeping-tracker is at {head}, expected {TAG_COMMIT} (tag {TAG}). "
                 "Delete the external/ folder and run this script again.")
    py = sys.executable
    run([py, "code/01_download.py"], cwd=EXT)
    run([py, "code/02_build_panel.py"], cwd=EXT)
    run([py, "code/03_check.py"], cwd=EXT)
    report = (EXT / "data" / "check_report.md").read_text(encoding="utf-8")
    if "All checks passed." not in report:
        sys.exit("peacekeeping-tracker's checks did not all pass; see external/peacekeeping-tracker/data/check_report.md")
    print("UN data rebuilt and checked against peacekeeping-tracker v1.0.0.")


if __name__ == "__main__":
    main()
