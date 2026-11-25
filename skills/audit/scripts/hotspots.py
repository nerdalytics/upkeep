#!/usr/bin/env python3
import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_EXCLUDES = ("node_modules/", "vendor/", "dist/", "build/", ".git/")
# Lockfiles change with every dependency update and are long, so they would lead the ranking.
DEFAULT_EXCLUDE_NAMES = ("*.lock", "*-lock.*")


def die(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def commit_counts(repo, since):
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "log", f"--since={since}", "--name-only", "--pretty=format:", "--relative", "--", "."],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        die("error: git is not installed or is not on PATH.")
    except subprocess.CalledProcessError as exc:
        die(f"error: git log failed in '{repo}'. Check that it is a git repository with commits. git said: {exc.stderr.strip()}")
    counts = {}
    seen_in_commit = set()
    for line in proc.stdout.splitlines():
        path = line.strip()
        if not path:
            seen_in_commit = set()
            continue
        if path in seen_in_commit:
            continue
        seen_in_commit.add(path)
        counts[path] = counts.get(path, 0) + 1
    return counts


def count_lines(path):
    try:
        with open(path, "rb") as fh:
            if b"\0" in fh.read(8192):
                return None
            fh.seek(0)
            return sum(1 for _ in fh)
    except OSError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Rank hotspot candidates. The score is the number of commits that touched a file multiplied by its current line count. It is a proxy and does not measure complexity."
    )
    parser.add_argument("repo", nargs="?", default=".", help="Repository root, or a directory inside the repository to rank only its files. The default is the current directory.")
    parser.add_argument("--since", default="6 months ago", help="How far back to read git history. The default is '6 months ago'.")
    parser.add_argument("--top", type=int, default=20, help="Number of candidates to report. The default is 20.")
    parser.add_argument("--min-commits", type=int, default=5, help="Smallest number of commits in the window for a file to count. The default is 5.")
    parser.add_argument("--min-lines", type=int, default=200, help="Smallest current line count for a file to count. The default is 200.")
    parser.add_argument("--exclude", default=",".join(DEFAULT_EXCLUDES), help="Comma-separated path prefixes to skip.")
    parser.add_argument("--exclude-names", default=",".join(DEFAULT_EXCLUDE_NAMES), help="Comma-separated file name patterns to skip. The default skips lockfiles.")
    parser.add_argument("--json", action="store_true", help="Print JSON and not a table.")
    args = parser.parse_args()

    repo = Path(args.repo)
    excludes = tuple(p.strip() for p in args.exclude.split(",") if p.strip())
    exclude_names = [p.strip() for p in args.exclude_names.split(",") if p.strip()]
    counts = commit_counts(repo, args.since)

    candidates = []
    for rel, commits in counts.items():
        if commits < args.min_commits or rel.startswith(excludes):
            continue
        if any(fnmatch.fnmatch(Path(rel).name, pattern) for pattern in exclude_names):
            continue
        lines = count_lines(repo / rel)
        if lines is None or lines < args.min_lines:
            continue
        candidates.append({"file": rel, "commits": commits, "lines": lines, "score": commits * lines})
    candidates.sort(key=lambda c: (-c["score"], c["file"]))
    candidates = candidates[: args.top]

    if args.json:
        print(json.dumps(candidates, indent=2))
        return
    if not candidates:
        print(f"No file has at least {args.min_commits} commits since '{args.since}' and at least {args.min_lines} lines.")
        return
    print(f"{'commits':>7} {'lines':>7} {'score':>9}  file")
    for c in candidates:
        print(f"{c['commits']:>7} {c['lines']:>7} {c['score']:>9}  {c['file']}")


if __name__ == "__main__":
    main()