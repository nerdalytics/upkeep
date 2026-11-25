#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("ratchet_baseline.py")


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, cwd=cwd)


with tempfile.TemporaryDirectory() as tmp:
    one, three, baseline = Path(tmp, "one.json"), Path(tmp, "three.json"), Path(tmp, "baseline.json")
    violation = {"rule": "C901", "file": "src/billing.py"}
    one.write_text(json.dumps([violation]))
    three.write_text(json.dumps([violation] * 3))

    assert run("snapshot", one, "-o", baseline).returncode == 0
    grown = run("check", three, "--baseline", baseline)
    assert grown.returncode == 1 and "not in the baseline: 2." in grown.stdout, grown.stdout

    assert run("snapshot", three, "-o", baseline).returncode == 0
    assert run("check", three, "--baseline", baseline).returncode == 0
    shrunk = run("check", one, "--baseline", baseline)
    assert shrunk.returncode == 0 and "no longer occur: 2." in shrunk.stdout, shrunk.stdout

    baseline.write_text(json.dumps({"violations": [violation]}))  # baseline without counts
    assert run("check", one, "--baseline", baseline).returncode == 0

    # An absolute path becomes relative to the working directory.
    absolute = Path(tmp, "absolute.json")
    absolute.write_text(json.dumps([{"rule": "R1", "file": str(Path(tmp, "src", "a.py"))}]))
    assert run("snapshot", absolute, "-o", baseline, cwd=tmp).returncode == 0
    assert [v["file"] for v in json.loads(baseline.read_text())["violations"]] == ["src/a.py"]
    absolute.write_text(json.dumps({"rule": "R1"}))
    assert run("check", absolute, "--baseline", baseline, cwd=tmp).returncode == 2
print("ok")
