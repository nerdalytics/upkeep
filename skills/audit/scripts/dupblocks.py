#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_EXTENSIONS = (".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rb", ".cs", ".php", ".kt", ".rs")
DEFAULT_EXCLUDES = ("node_modules", "vendor", "dist", "build", ".git", "target", "__pycache__")


def die(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def list_paths(root):
    # In a git repository, scan what git tracks or would track, so ignored folders such as virtual environments are left out.
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return sorted(root.rglob("*"))
    return sorted(root / p for p in out.split("\0") if p)


def iter_files(root, extensions, excludes):
    for path in list_paths(root):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        if any(part in excludes for part in path.relative_to(root).parts):
            continue
        yield path


def normalized_lines(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return [(i, line.strip()) for i, line in enumerate(text.splitlines(), 1) if line.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Find blocks of lines that occur in more than one place. The comparison ignores blank lines and the whitespace at both ends of a line. The report gives the line numbers of each copy in its file."
    )
    parser.add_argument("root", nargs="?", default=".", help="Directory to scan. In a git repository, files that git ignores are skipped. The default is the current directory.")
    parser.add_argument("--window", type=int, default=6, help="Smallest block size in non-blank lines. The default is 6.")
    parser.add_argument("--min-copies", type=int, default=2, help="Smallest number of copies to report. The default is 2.")
    parser.add_argument("--top", type=int, default=20, help="Number of groups to report. The default is 20.")
    parser.add_argument("--extensions", default=",".join(DEFAULT_EXTENSIONS), help="Comma-separated file extensions to scan.")
    parser.add_argument("--exclude", default=",".join(DEFAULT_EXCLUDES), help="Comma-separated directory names to skip.")
    parser.add_argument("--json", action="store_true", help="Print JSON and not text.")
    args = parser.parse_args()

    if args.window < 2:
        die("error: --window must be at least 2.")
    root = Path(args.root)
    if not root.is_dir():
        die(f"error: {root} is not a directory.")
    extensions = {e.strip().lower() for e in args.extensions.split(",") if e.strip()}
    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}

    files = []
    windows = {}
    skipped = 0
    for path in iter_files(root, extensions, excludes):
        lines = normalized_lines(path)
        if lines is None:
            skipped += 1
            continue
        if len(lines) < args.window:
            continue
        file_idx = len(files)
        files.append((str(path.relative_to(root)), lines))
        for start in range(len(lines) - args.window + 1):
            text = "\n".join(line for _, line in lines[start : start + args.window])
            key = hashlib.sha1(text.encode("utf-8")).hexdigest()
            windows.setdefault(key, []).append((file_idx, start))

    # Every distinct set of places where one window occurs often enough.
    place_sets = set()
    for locations in windows.values():
        places = []
        for file_idx, start in locations:
            if places and places[-1][0] == file_idx and start < places[-1][1] + args.window:
                continue  # overlaps the previous copy in the same file
            places.append((file_idx, start))
        if len(places) >= args.min_copies:
            place_sets.add(frozenset(places))

    # A block grows while the next window occurs in the same places, each shifted by one line.
    report = []
    for places in place_sets:
        if frozenset((f, s - 1) for f, s in places) in place_sets:
            continue  # the block starts earlier
        length = args.window
        while frozenset((f, s + length - args.window + 1) for f, s in places) in place_sets:
            length += 1
        report.append(
            [
                {"file": files[f][0], "start": files[f][1][s][0], "end": files[f][1][s + length - 1][0], "lines": length}
                for f, s in sorted(places)
            ]
        )
    report.sort(key=lambda g: (-sum(loc["lines"] for loc in g), g[0]["file"], g[0]["start"]))
    report = report[: args.top]

    if args.json:
        print(json.dumps([{"copies": len(g), "duplicated_lines": sum(loc["lines"] for loc in g), "locations": g} for g in report], indent=2))
        return
    if not report:
        print(f"Found no duplicated block of {args.window} or more lines. Files scanned: {len(files)}. Files that could not be read: {skipped}.")
        return
    for locations in report:
        print(f"{len(locations)} copies of a block of {locations[0]['lines']} lines:")
        for loc in locations:
            print(f"  {loc['file']}:{loc['start']}-{loc['end']}")


if __name__ == "__main__":
    main()