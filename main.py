"""
Main pipeline script to generate all figures for the project.

This script sequentially executes each figure script in src/ and
saves all outputs to the figures/ directory.
"""

import os
import subprocess
import sys

SCR_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

# List all the figure scripts to run, in desired order
FIG_SCRIPTS = [
    "fig_1B.py",
    "fig_3E.py",
    "fig_4E.py",
    "fig_5E.py",
    "fig_6BD.py",
    "fig_8.py",
    "fig_9B.py",
    "fig_S3.py",
    "fig_S4.py",
    "fig_S6B.py",
    "fig_S7BE.py",
]

def run_script(script):
    script_path = os.path.join(SCR_DIR, script)
    print(f"\n--- Running {script} ---")

    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(__file__))
    if result.returncode != 0:
        print(f"Error: {script} exited with code {result.returncode}")
    else:
        print(f"Done: {script}")

def main():
    print("=== Generating Figuers ===")
    for script in FIG_SCRIPTS:
        run_script(script)
    print("\nAll figures generated! See the 'figures/' directory.")

if __name__ == "__main__":
    main()
