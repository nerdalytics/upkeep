#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("dupblocks.py")
X = [f"x_{i} = compute({i})" for i in range(10)]
Y = [f"y_{i} = other({i})" for i in range(10)]


def scan(files):
    with tempfile.TemporaryDirectory() as tmp:
        for name, lines in files.items():
            Path(tmp, name).write_text("\n".join(lines) + "\n")
        out = subprocess.run([sys.executable, str(SCRIPT), tmp, "--json"], capture_output=True, text=True, check=True)
    return [[(loc["file"], loc["start"], loc["end"]) for loc in group["locations"]] for group in json.loads(out.stdout)]


# a.py holds X then Y back to back; each is copied in a different file.
groups = scan({"a.py": ["def a():"] + X + Y, "b.py": ["def b():"] + X, "c.py": ["def c():", ""] + Y})
assert [("a.py", 2, 11), ("b.py", 2, 11)] in groups, groups
assert [("a.py", 12, 21), ("c.py", 3, 12)] in groups, groups
assert len(groups) == 2, groups

assert scan({"a.py": X, "b.py": Y}) == []

# In a git repository, a copy inside an ignored folder is not scanned.
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["git", "init", "-q", tmp], check=True)
    Path(tmp, "env").mkdir()
    for name, text in {"a.py": X, "env/b.py": X, ".gitignore": ["env/"]}.items():
        Path(tmp, name).write_text("\n".join(text) + "\n")
    out = subprocess.run([sys.executable, str(SCRIPT), tmp, "--json"], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout) == [], out.stdout
print("ok")
