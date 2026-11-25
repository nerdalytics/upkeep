#!/usr/bin/env python3
import argparse
import json
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path


def die(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def repo_relative(path):
    # Linters report absolute paths. The baseline needs relative ones to match on another machine.
    # The operating system reports the working directory without symlinks, but a linter's path may contain one.
    return os.path.relpath(os.path.realpath(path)) if os.path.isabs(path) else path


def load_violations(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"error: {path} does not exist.")
    except json.JSONDecodeError as exc:
        die(f"error: {path} is not valid JSON. {exc}")
    if not isinstance(data, list):
        die(f"error: {path} must contain a JSON array.")
    fingerprints = Counter()
    for i, item in enumerate(data):
        if not isinstance(item, dict) or not isinstance(item.get("rule"), str) or not isinstance(item.get("file"), str):
            die(f"error: entry {i} in {path} needs the string fields 'rule' and 'file'.")
        symbol = item.get("symbol", "")
        if not isinstance(symbol, str):
            die(f"error: 'symbol' in entry {i} of {path} is not a string.")
        fingerprints[(item["rule"], repo_relative(item["file"]), symbol)] += 1
    return fingerprints


def fingerprint_list(fingerprints):
    return [
        {"rule": rule, "file": file, "symbol": symbol, "count": count}
        for (rule, file, symbol), count in sorted(fingerprints.items())
    ]


def cmd_snapshot(args):
    current = load_violations(args.violations)
    baseline = {
        "version": 1,
        "created": date.today().isoformat(),
        "violations": fingerprint_list(current),
    }
    Path(args.output).write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote the baseline to {args.output}. Violations in it: {sum(current.values())}.")


def cmd_check(args):
    current = load_violations(args.violations)
    try:
        baseline_data = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        stored = baseline_data["violations"]
    except FileNotFoundError:
        die(f"error: the baseline {args.baseline} does not exist.")
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        die(f"error: {args.baseline} is not a valid baseline. {exc}")
    baseline = Counter()
    for i, item in enumerate(stored):
        if not isinstance(item, dict) or not isinstance(item.get("rule"), str) or not isinstance(item.get("file"), str):
            die(f"error: baseline entry {i} needs the string fields 'rule' and 'file'.")
        count = item.get("count", 1)  # baselines written before counts existed have none
        if type(count) is not int or count < 1:
            die(f"error: 'count' in baseline entry {i} is not a positive whole number.")
        baseline[(item["rule"], item["file"], item.get("symbol", ""))] += count
    added = current - baseline
    resolved = baseline - current
    if added:
        print(f"Failed. New violations that are not in the baseline: {sum(added.values())}.")
        for fingerprint in sorted(added):
            rule, file, symbol = fingerprint
            location = f"{file} ({symbol})" if symbol else file
            print(f"  {rule} in {location}: {current[fingerprint]} now, {baseline[fingerprint]} in the baseline")
    if resolved:
        print(f"Violations in the baseline that no longer occur: {sum(resolved.values())}. Take a new snapshot so that they cannot return.")
    if added:
        sys.exit(1)
    print(f"Passed. No new violations. {sum(current.values())} now, {sum(baseline.values())} in the baseline.")


def main():
    parser = argparse.ArgumentParser(
        description="Freeze the current violations of any check as a baseline, then fail only when a violation appears that is not in it."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="Write the current violations to the baseline file.")
    snap.add_argument("violations", help="JSON file with an array of {rule, file, symbol} objects. symbol is optional.")
    snap.add_argument("-o", "--output", default="maintainability-baseline.json", help="Baseline file to write. The default is maintainability-baseline.json.")
    snap.set_defaults(func=cmd_snapshot)
    chk = sub.add_parser("check", help="Exit with 1 when a violation is not in the baseline.")
    chk.add_argument("violations", help="JSON file with an array of {rule, file, symbol} objects. symbol is optional.")
    chk.add_argument("--baseline", default="maintainability-baseline.json", help="Baseline file to read. The default is maintainability-baseline.json.")
    chk.set_defaults(func=cmd_check)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()