#!/usr/bin/env python3
"""Run every recipe under docs/recipes/code/ against the package sources and fail on any error.

    python3 scripts/check_recipes.py <packages-dir>

Each recipe is executed exactly as the site shows it (the pages include these files verbatim),
with PYTHONPATH pointing at <packages-dir>/*/src. Exit status 0 only if every recipe ran.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..", "docs", "recipes", "code")


def setup_node_modules(cwd, pkg_root):
    nm = os.path.join(cwd, "node_modules")
    os.makedirs(nm, exist_ok=True)
    for pkg_dir in glob.glob(os.path.join(os.path.abspath(pkg_root), "*")):
        pj_path = os.path.join(pkg_dir, "package.json")
        if os.path.isfile(pj_path):
            try:
                with open(pj_path, "r", encoding="utf-8") as f:
                    pj = json.load(f)
                    name = pj.get("name")
                    if name:
                        if name.startswith("@"):
                            scope, subname = name.split("/", 1)
                            os.makedirs(os.path.join(nm, scope), exist_ok=True)
                            target = os.path.join(nm, scope, subname)
                        else:
                            target = os.path.join(nm, name)
                        if not os.path.exists(target):
                            os.symlink(pkg_dir, target)
                        src_nm = os.path.join(pkg_dir, "node_modules")
                        if os.path.isdir(src_nm):
                            for dep in os.listdir(src_nm):
                                dep_dst = os.path.join(nm, dep)
                                if not os.path.exists(dep_dst):
                                    try:
                                        os.symlink(os.path.join(src_nm, dep), dep_dst)
                                    except Exception:
                                        pass
            except Exception:
                pass


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pkg_root = os.path.abspath(argv[0])
    srcs = sorted(glob.glob(os.path.join(pkg_root, "*", "src")))
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(srcs))
    failed = []

    # 1. Run Python recipes
    for path in sorted(glob.glob(os.path.join(CODE, "*.py"))):
        with tempfile.TemporaryDirectory() as cwd:
            r = subprocess.run([sys.executable, path], cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
        tail = (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:] or [""]
        print("%-4s %-26s %s" % ("ok" if r.returncode == 0 else "FAIL", os.path.basename(path), tail[0][:110]))
        if r.returncode:
            failed.append(path)
            print(r.stderr[-1500:])

    # 2. Run Node.js / JavaScript recipes
    for path in sorted(glob.glob(os.path.join(CODE, "*.mjs")) + glob.glob(os.path.join(CODE, "*.js"))):
        with tempfile.TemporaryDirectory() as cwd:
            setup_node_modules(cwd, pkg_root)
            script_in_cwd = os.path.join(cwd, os.path.basename(path))
            shutil.copy(path, script_in_cwd)
            r = subprocess.run(["node", script_in_cwd], cwd=cwd, env=os.environ, capture_output=True, text=True, timeout=120)
        tail = (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:] or [""]
        print("%-4s %-26s %s" % ("ok" if r.returncode == 0 else "FAIL", os.path.basename(path), tail[0][:110]))
        if r.returncode:
            failed.append(path)
            print(r.stderr[-1500:])

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
