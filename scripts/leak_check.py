#!/usr/bin/env python3
"""Public-text gate: internal build names, ids and paths must never reach a public page.

    python3 scripts/leak_check.py <file-or-dir>...    prints each hit, exit 1 if any

Also imported by build_catalog.py, which holds back any package whose public text trips it.
The patterns are deliberately narrow (no plain "factory", which is a normal programming word).
"""
import os
import re
import sys

PATTERNS = [
    ("internal build system", re.compile(r"algo[-_ ]?factory|factory[-_ ]workspace|factory\.sh|hermes", re.I)),
    ("internal role or tool", re.compile(r"\baf[-_](?:[a-z]+)(?:\.py)?\b")),
    ("internal gate id", re.compile(r"\bgate\s+G(?:[0-7]|-V|-X)\b|\bG(?:[0-7]|-V|-X)\s+gate\b|\bG-[VX]\b", re.I)),
    ("internal work-item id", re.compile(r"\br1-s\d+\b|\blane[-_ ]id\b|\bin-flight lane", re.I)),
    ("internal rule id", re.compile(r"\(R\d{1,2}\)|\brule R\d{1,2}\b")),
    ("retired product name", re.compile(r"pqshift|qshift|qproof|pqblack", re.I)),
    ("local path", re.compile(r"/home/[a-z_][a-z0-9_-]*/|~/\.hermes|/Documents/Hermes")),
    ("assistant or vendor name", re.compile(r"\banthropic\b|\bclaude-(?:opus|sonnet|haiku)|\bgpt-[0-9]", re.I)),
]
_CERT = re.compile(r"\bcertified\b", re.I)
_CERT_OK = re.compile(r"\b(?:not|never|no|isn't|aren't|nor)\b[^.]{0,60}\bcertified\b|\"certified\"|"
                      r"certified,\s*(?:validated|FIPS)|\bcertified\s+or\b", re.I)


def leaks(text):
    """[(label, matched text)] for every internal term in text."""
    out = [(label, m.group(0)) for label, rx in PATTERNS for m in rx.finditer(text)]
    for line in text.splitlines():
        if _CERT.search(line) and not _CERT_OK.search(line):
            out.append(("overclaim", "certified"))
    return out


def _files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", ".cache", "__pycache__", "node_modules")]
                for f in files:
                    if f.endswith((".md", ".txt", ".json", ".html", ".py", ".yml", ".mdc", ".svg", ".toml")):
                        yield os.path.join(root, f)
        else:
            yield p


def main(argv):
    hits = 0
    for path in _files(argv):
        if os.path.basename(path) == "leak_check.py":
            continue
        for n, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
            for label, text in leaks(line):
                hits += 1
                print("%s:%d: %s: %s" % (path, n, label, text))
    print("leak check: %d hit(s)" % hits)
    return 1 if hits else 0


def _selftest():
    assert leaks("built by the algo factory") and leaks("see factory.sh") and leaks("role af-packager")
    assert leaks("passed gate G7") and leaks("import pqshift_core") and leaks("/home/alice/x")
    assert leaks("This package is certified.")
    assert not leaks("It is not FIPS 140-3 certified.") and not leaks("Never call them certified, validated")
    assert not leaks("use a key factory method") and not leaks("G7 countries") and not leaks("agility score R2")
    return 0


if __name__ == "__main__":
    sys.exit(_selftest() if sys.argv[1:] == ["selftest"] else main(sys.argv[1:] or ["docs", "data"]))
