#!/usr/bin/env python3
"""Run every recipe under docs/recipes/code/ against the package sources and fail on any error.

    python3 scripts/check_recipes.py <packages-dir>

Each recipe is executed exactly as the site shows it (the pages include these files verbatim),
with PYTHONPATH pointing at <packages-dir>/*/src. Exit status 0 only if every recipe ran.
"""
import glob
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..", "docs", "recipes", "code")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    srcs = sorted(glob.glob(os.path.join(os.path.abspath(argv[0]), "*", "src")))
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(srcs))
    failed = []
    for path in sorted(glob.glob(os.path.join(CODE, "*.py"))):
        with tempfile.TemporaryDirectory() as cwd:
            r = subprocess.run([sys.executable, path], cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
        tail = (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:] or [""]
        print("%-4s %-22s %s" % ("ok" if r.returncode == 0 else "FAIL", os.path.basename(path), tail[0][:110]))
        if r.returncode:
            failed.append(path)
            print(r.stderr[-1500:])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
