# dirsize

> Zero-dependency directory size analyzer. Pure Python standard library. No `pip install`. Works on Windows / macOS / Linux / Android (Termux).

Find out what's eating your disk — instantly. No install, no internet, just one file.

[![Sponsor](https://img.shields.io/badge/sponsor-afdian-ff69b4)](https://afdian.com/a/Zhiyilang)

## Why

- **Zero dependencies** — only the Python standard library. Drop the single file anywhere and run.
- **Portable** — one `dirsize.py` file, runs on Python 3.6+.
- **Fast & safe** — skips unreadable files instead of crashing; never modifies anything.

## Features

| Feature | Supported |
| --- | --- |
| Total size of a folder | ✅ |
| Top-N largest folders & files | ✅ |
| Percentage of total per entry | ✅ |
| Depth control (`--depth`) | ✅ |
| Min-size filter (`--min 1M`) | ✅ |
| JSON output (`--json`) | ✅ |
| Human-readable units (B/KB/MB/GB/TB) | ✅ |

## Install

Just download `dirsize.py`. That's it.

```bash
python dirsize.py /path/to/folder
```

## Usage

```bash
# Top 15 largest entries under a folder
python dirsize.py ./projects

# Show top 20, 2 levels deep
python dirsize.py ./projects --top 20 --depth 2

# Only entries >= 100 MB
python dirsize.py ./videos --min 100M

# Machine-readable
python dirsize.py ./data --json
```

### Example output

```
📁 /home/me/projects
   total: 1.2 GB (1288490188 bytes)

  node_modules   892.3 MB   69.3%  📂
  build          210.4 MB   16.3%  📂
  README.md        4.2 KB    0.0%  📄
  main.py          1.8 KB    0.0%  📄
```

## License

MIT — free to use, modify and ship.

---

### 👋 Like this tool?

If `dirsize` helped you clean up disk space, consider supporting my open-source
work via [爱发电 (afdian)](https://afdian.com/a/Zhiyilang). Every bit funds more
zero-dependency tools. Thank you! ⭐

<!-- cross-links -->

## 🔗 More zero-dependency tools

All of these are single-file, pure Python-stdlib CLIs — offline, no `pip install`, cross-platform:

- **billfusion** — Bill / CSV merging · <https://github.com/Zhiyilang/billfusion>
- **lanshare** — LAN file transfer · <https://github.com/Zhiyilang/lanshare>
- **dupescan** — Duplicate file finder · <https://github.com/Zhiyilang/dupescan>
- **csvdiff** — CSV / JSON diff · <https://github.com/Zhiyilang/csvdiff>
- **md2html** — Markdown to HTML · <https://github.com/Zhiyilang/md2html>

Full portfolio & docs: <https://zhiyilang.github.io/>
