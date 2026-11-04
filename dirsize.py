#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dirsize.py - Zero-dependency directory size analyzer (pure Python stdlib).

Walks a directory tree, sums file sizes, and shows the largest folders/files
in a readable tree. No pip, no third-party packages. Runs on Windows / macOS
/ Linux / Android (Termux).

Usage:
  python dirsize.py PATH                 # show top-level + largest entries
  python dirsize.py PATH --top 20        # show top 20 entries by size
  python dirsize.py PATH --depth 2       # control tree depth
  python dirsize.py PATH --json          # machine-readable output
  python dirsize.py PATH --min 1M        # only show entries >= 1 MB

Size units: K=1024, M=1024*1024, G=1024**3, T=1024**4 (case-insensitive,
e.g. 500K, 2M, 1G).

License: MIT
"""
import os
import sys
import json
import argparse

VERSION = "1.0.0"


def human(n):
    """Format byte count as human-readable string."""
    if n < 1024:
        return "%d B" % n
    units = ["KB", "MB", "GB", "TB", "PB"]
    f = float(n)
    for u in units:
        f /= 1024.0
        if f < 1024.0:
            return "%.1f %s" % (f, u)
    return "%.1f PB" % f


def parse_size(s):
    s = s.strip().upper()
    if not s:
        return 0
    mult = {"": 1, "B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
    num = ""
    for ch in s:
        if ch.isdigit() or ch == ".":
            num += ch
        else:
            break
    unit = s[len(num):].strip()
    if unit not in mult:
        raise ValueError("bad size unit: %r" % unit)
    return int(float(num) * mult[unit])


def walk(path):
    """Return (total_bytes, {dir: size}, [(file, size), ...]) for path."""
    total = 0
    dir_sizes = {}
    files = []
    path = os.path.abspath(path)
    for root, dirnames, filenames in os.walk(path):
        for fn in filenames:
            fp = os.path.join(root, fn)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                sz = 0
            total += sz
            files.append((fp, sz))
            # accumulate this file's size to every ancestor directory up to path
            d = root
            while True:
                dir_sizes[d] = dir_sizes.get(d, 0) + sz
                if os.path.abspath(d) == path:
                    break
                parent = os.path.dirname(d)
                if parent == d:
                    break
                d = parent
    return total, dir_sizes, files


def main():
    ap = argparse.ArgumentParser(
        description="Zero-dependency directory size analyzer.")
    ap.add_argument("path", nargs="?", default=".", help="directory to scan")
    ap.add_argument("--top", type=int, default=15, help="show top N entries")
    ap.add_argument("--depth", type=int, default=1, help="tree depth to show")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--min", default="", help="hide entries smaller than e.g. 1M")
    ap.add_argument("--version", action="version", version="dirsize %s" % VERSION)
    args = ap.parse_args()

    path = os.path.abspath(args.path)
    if not os.path.isdir(path):
        sys.stderr.write("error: not a directory: %s\n" % args.path)
        sys.exit(1)

    total, dir_sizes, files = walk(path)
    min_bytes = parse_size(args.min) if args.min else 0

    # Build a combined list of entries at each depth level
    entries = []
    for d, sz in dir_sizes.items():
        if d == path:
            continue
        entries.append((d, sz, True))
    for fp, sz in files:
        entries.append((fp, sz, False))

    # top-level (depth 1) relative entries
    def depth_of(p):
        rel = os.path.relpath(p, path)
        return 0 if rel == "." else rel.count(os.sep) + 1

    out = []
    for p, sz, is_dir in entries:
        if sz < min_bytes:
            continue
        if depth_of(p) > args.depth:
            continue
        out.append((p, sz, is_dir))
    out.sort(key=lambda x: x[1], reverse=True)

    if args.json:
        result = {
            "path": path,
            "total_bytes": total,
            "total_human": human(total),
            "entries": [
                {"path": p, "bytes": sz, "human": human(sz), "is_dir": is_dir}
                for p, sz, is_dir in out[: args.top]
            ],
        }
        sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("📁 %s" % path)
    print("   total: %s (%d bytes)\n" % (human(total), total))
    if not out:
        print("   (no entries meet the filter)")
        return
    shown = out[: args.top]
    maxlen = max(len(os.path.relpath(p, path)) for p, _, _ in shown)
    for p, sz, is_dir in shown:
        rel = os.path.relpath(p, path)
        icon = "📂" if is_dir else "📄"
        pct = (sz / total * 100) if total else 0
        print("  %-*s  %10s  %5.1f%%  %s" % (maxlen, rel, human(sz), pct, icon))
    if len(out) > args.top:
        print("  ... and %d more (use --top N)" % (len(out) - args.top))


if __name__ == "__main__":
    main()
