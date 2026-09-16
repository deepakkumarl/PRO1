import os
import sys
from pathlib import Path

# Trigger evaluation script
if __name__ == "__main__":
    eval_path = Path(__file__).resolve().parent.parent / "evaluation" / "run_eval.py"
    os.system(f"{sys.executable} {eval_path}")
