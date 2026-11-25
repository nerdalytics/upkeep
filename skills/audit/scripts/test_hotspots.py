#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("hotspots.py")
GIT = ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false"]


def rank(directory):
    out = subprocess.run(
        [sys.executable, str(SCRIPT), str(directory), "--json", "--min-commits", "2", "--min-lines", "3"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [c["file"] for c in json.loads(out.stdout)]


with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["git", "init", "-q", tmp], check=True)
    Path(tmp, "src").mkdir()
    for round_number in range(3):
        for name in ("src/app.py", "top.py", "deps.lock", "deps-lock.json"):
            Path(tmp, name).write_text("\n".join(f"line {round_number} {i}" for i in range(10)) + "\n")
        subprocess.run(GIT + ["-C", tmp, "add", "-A"], check=True)
        subprocess.run(GIT + ["-C", tmp, "commit", "-q", "-m", f"round {round_number}"], check=True)

    # Lockfiles are left out, and paths are relative to the given directory.
    assert rank(tmp) == ["src/app.py", "top.py"], rank(tmp)
    # A directory inside the repository ranks only its own files.
    assert rank(Path(tmp, "src")) == ["app.py"], rank(Path(tmp, "src"))
print("ok")
