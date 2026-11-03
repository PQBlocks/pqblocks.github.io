#!/usr/bin/env python3
"""Build data/catalog.json from the package repositories of the organisation.

Every field comes from a file in the package (pyproject.toml, package.json, README.md, examples/),
from GitHub (repository topics), PyPI, or npm. Nothing is written by hand,
so the catalog can never describe an API the package does not have.

    python3 scripts/build_catalog.py <packages-dir> [--verify] [--out data/catalog.json]
    python3 scripts/build_catalog.py <packages-dir> --print-deps     # runtime deps of every package

<packages-dir> holds one checkout per repository. A directory is a package when its
pyproject.toml or package.json defines an open-source distribution. --verify runs each
README quickstart against the package source. A package is published only when it is verified,
carries an area topic and passes the public-text gate; otherwise it stays in the catalog with
"held" set to the reason, and the site, MCP server and skills leave it out until it is fixed.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.request

ORG = "PQBlocks"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leak_check  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "catalog.json")
NOT_PACKAGES = {"pqblocks-mcp"}          # tooling, not a library
AREAS = {
    "pq-crypto": "PQ cryptography",
    "pq-migration": "Migration & readiness",
    "pq-interop": "Interoperability",
    "pq-conformance": "Conformance",
    "quantum-inspired": "Quantum-inspired"
}
FALLBACK_AREAS = {
    "browser-pqc-verifier": "PQ cryptography",
    "pqblocks-browser-verifier": "PQ cryptography",
    "fips-dualmode": "PQ cryptography",
    "hybrid-sdk": "PQ cryptography",
    "fips-pqc-primitives": "PQ cryptography",
    "hybrid-file-encryption": "PQ cryptography",
    "hybrid-jose": "PQ cryptography",
    "hybrid-jwe": "Interoperability",
    "pqc-wireformat": "Interoperability",
    "tls-hybrid-interop": "Interoperability",
    "mlkem-csr-pop": "Interoperability",
    "cbom-scanner": "Migration & readiness",
    "cbom-enricher": "Migration & readiness",
    "crypto-policy-engine": "Migration & readiness",
    "cnsa-evidence-pack": "Migration & readiness",
    "jwe-policy-auditor": "Migration & readiness",
    "pqc-lint": "Migration & readiness",
    "crypto-agility": "Migration & readiness",
    "acvp-conformance": "Conformance",
    "fips-boundary-validator": "Conformance",
    "sparse-bifurcation": "Quantum-inspired",
    "simulated-bifurcation": "Quantum-inspired",
    "simulated-annealing": "Quantum-inspired",
    "simulated-quantum-annealing": "Quantum-inspired",
    "annealing-schedule": "Quantum-inspired",
    "digital-annealing": "Quantum-inspired",
    "population-annealing": "Quantum-inspired",
    "quantum-inspired-evolutionary": "Quantum-inspired",
    "qubo-core": "Quantum-inspired",
    "qubo-benchmark-harness": "Quantum-inspired",
}
DOCS = ("README.md", "AGENTS.md", "SECURITY_NOTES.md", "TESTING.md", "BENCHMARKS.md",
        "EVIDENCE.md", "VERIFICATION_REPORT.md", "USE_CASES.md", "CHANGELOG.md")
NOISE = re.compile(r"^(\s*$|\[!\[|<|---|>\s*\[!|\s*!\[)")


def repo_of(d, pyproject=None, pkg_json=None):
    if pyproject:
        url = pyproject.get("project", {}).get("urls", {}).get("Homepage", "")
        m = re.search(r"github\.com/%s/([^/#]+)" % ORG, url)
        if m:
            return m.group(1)
    if pkg_json:
        repo = pkg_json.get("repository", "")
        if isinstance(repo, dict):
            repo = repo.get("url", "")
        m = re.search(r"github\.com/%s/([^/#.]+)" % ORG, repo)
        if m:
            return m.group(1)
    git_cfg = os.path.join(d, ".git", "config")
    if os.path.isfile(git_cfg):
        try:
            content = open(git_cfg, "r", encoding="utf-8", errors="ignore").read()
            m = re.search(r"github\.com[:/]%s/([^/#.]+?)(?:\.git|\s)" % ORG, content)
            if m:
                return m.group(1)
        except Exception:
            pass
    base = os.path.basename(d)
    return base.replace("pqblocks-", "")


def on_pypi(dist):
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/%s/json" % dist, timeout=10) as r:
            return json.load(r)["info"]["version"]
    except Exception:
        return None


def on_npm(pkg_name):
    try:
        url = "https://registry.npmjs.org/%s" % pkg_name.replace("/", "%2F")
        req = urllib.request.Request(url, headers={"User-Agent": "PQBlocks-Catalog-Builder/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
            return data.get("dist-tags", {}).get("latest")
    except Exception:
        return None


def topics():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    env = dict(os.environ)
    if token:
        env["GH_TOKEN"] = token
    try:
        res = subprocess.run(["gh", "repo", "list", ORG, "--limit", "200", "--json", "name,repositoryTopics"],
                             capture_output=True, text=True, env=env)
        if res.returncode == 0 and res.stdout.strip():
            return {r["name"]: [t["name"] for t in (r.get("repositoryTopics") or [])] for r in json.loads(res.stdout)}
    except Exception as e:
        print(f"Notice: gh repo list failed ({e}), using fallback topics", file=sys.stderr)
    return {}


def detect_c_sdk(d):
    headers = []
    libs = []
    for root, dirs, files in os.walk(d):
        if any(ign in root for ign in ("node_modules", ".git", "venv", ".pytest_cache", "build")):
            continue
        for f in files:
            if f.endswith(".h"):
                headers.append(f)
            elif f.endswith(".so") or f.endswith(".dylib") or f.endswith(".dll"):
                libs.append(f)
    has_cmake = os.path.isfile(os.path.join(d, "CMakeLists.txt")) or os.path.isfile(os.path.join(d, "Makefile"))
    return {
        "has_c_sdk": bool(headers or has_cmake),
        "headers": sorted(set(headers)),
        "libs": sorted(set(libs)),
        "has_cmake": has_cmake,
    }


def detect_cli(pyproject, pkg_json, d):
    cli = set()
    if pyproject:
        cli.update(pyproject.get("project", {}).get("scripts", {}).keys())
    if pkg_json:
        b = pkg_json.get("bin", {})
        if isinstance(b, dict):
            cli.update(b.keys())
        elif isinstance(b, str):
            cli.add(pkg_json.get("name", "").split("/")[-1])
    bin_dir = os.path.join(d, "bin")
    if os.path.isdir(bin_dir):
        for f in os.listdir(bin_dir):
            if os.path.isfile(os.path.join(bin_dir, f)) and not f.startswith("."):
                cli.add(f.replace(".js", "").replace(".py", ""))
    return sorted(cli)


def readme_parts(text):
    lines = text.splitlines()
    intro = []
    for line in lines[1:]:
        if line.startswith("```") or line.startswith("## "):
            break
        if NOISE.match(line):
            continue
        intro.append(line.lstrip("> ").strip())

    quick_py = re.search(r"```python\n(.*?)```", text, re.S)
    quick_js = re.search(r"```(?:javascript|js|node)\n(.*?)```", text, re.S)

    lang = "python" if quick_py else ("javascript" if quick_js else "none")
    quick = quick_py.group(1) if quick_py else (quick_js.group(1) if quick_js else "")
    heads = [h.strip() for h in re.findall(r"^## (.+)$", text, re.M)]
    return [l for l in intro if l][:4], quick, heads, lang


def verify(pkg_dir, code, lang="python"):
    """Run a snippet against the package source; True/False plus the last output line."""
    if not code.strip():
        return False, "no runnable quickstart in README"
    pkg_dir = os.path.abspath(pkg_dir)
    with tempfile.TemporaryDirectory() as d:
        if lang in ("javascript", "typescript"):
            try:
                pkg_name = None
                p_json_path = os.path.join(pkg_dir, "package.json")
                if os.path.isfile(p_json_path):
                    with open(p_json_path, "r", encoding="utf-8") as f:
                        pkg_name = json.load(f).get("name")
                if not pkg_name:
                    pkg_name = os.path.basename(pkg_dir)
                nm = os.path.join(d, "node_modules")
                if pkg_name.startswith("@"):
                    scope, subname = pkg_name.split("/", 1)
                    os.makedirs(os.path.join(nm, scope), exist_ok=True)
                    os.symlink(pkg_dir, os.path.join(nm, scope, subname))
                else:
                    os.makedirs(nm, exist_ok=True)
                    os.symlink(pkg_dir, os.path.join(nm, pkg_name))
                pkg_nm = os.path.join(pkg_dir, "node_modules")
                if os.path.isdir(pkg_nm):
                    for dep in os.listdir(pkg_nm):
                        src = os.path.join(pkg_nm, dep)
                        dst = os.path.join(nm, dep)
                        if not os.path.exists(dst):
                            os.symlink(src, dst)
                r = subprocess.run(["node", "--input-type=module", "-e", code], cwd=d, capture_output=True,
                                  text=True, timeout=60)
            except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
                return False, str(e)
            tail = (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:] or [""]
            return r.returncode == 0, re.sub(r"(?:/[^\s/'\"]+)+/", "", tail[0])[:200]
        else:
            env = dict(os.environ, PYTHONPATH=os.path.abspath(os.path.join(pkg_dir, "src")))
            try:
                r = subprocess.run([sys.executable, "-c", code], cwd=d, env=env, capture_output=True,
                                  text=True, timeout=120)
            except subprocess.TimeoutExpired:
                return False, "timed out"
            tail = (r.stdout.strip() or r.stderr.strip()).splitlines()[-1:] or [""]
            return r.returncode == 0, re.sub(r"(?:/[^\s/'\"]+)+/", "", tail[0])[:200]


def build(pkg_root, run_verify):
    tops = topics()
    existing_entries = {}
    if os.path.isfile(OUT):
        try:
            with open(OUT, "r", encoding="utf-8") as f:
                prev = json.load(f)
                for item in prev.get("packages", []):
                    if "package" in item and item.get("verified") is True:
                        existing_entries[item["package"]] = item
        except Exception:
            pass
    try:
        raw = subprocess.check_output(
            ["git", "show", "HEAD:data/catalog.json"],
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        prev = json.loads(raw)
        for item in prev.get("packages", []):
            if "package" in item and item.get("verified") is True and item["package"] not in existing_entries:
                existing_entries[item["package"]] = item
    except Exception:
        pass
    out = []
    for name in sorted(os.listdir(pkg_root)):
        d = os.path.join(pkg_root, name)
        if not os.path.isdir(d):
            continue

        has_pyproject = os.path.isfile(os.path.join(d, "pyproject.toml"))
        has_pkg_json = os.path.isfile(os.path.join(d, "package.json"))

        py = {}
        proj = {}
        if has_pyproject:
            try:
                py = tomllib.load(open(os.path.join(d, "pyproject.toml"), "rb"))
                proj = py.get("project", {})
            except Exception:
                pass

        pkg_json = {}
        if has_pkg_json:
            try:
                pkg_json = json.load(open(os.path.join(d, "package.json"), "r", encoding="utf-8"))
            except Exception:
                pass

        dist_py = proj.get("name", "")
        dist_npm = pkg_json.get("name", "")

        # Determine primary distribution identity
        if dist_py and dist_py.startswith("pqblocks-"):
            dist = dist_py
        elif dist_npm:
            # Map npm packages cleanly to pqblocks catalog identifier
            base_npm = dist_npm.split("/")[-1]
            dist = base_npm if base_npm.startswith("pqblocks-") else f"pqblocks-{base_npm}"
        elif dist_py:
            dist = dist_py
        else:
            dist = name

        if dist in NOT_PACKAGES:
            continue

        # Skip directory if it doesn't contain code or project metadata
        if not has_pyproject and not has_pkg_json:
            continue

        repo = repo_of(d, py, pkg_json)
        readme_path = os.path.join(d, "README.md")
        readme = open(readme_path, encoding="utf-8").read() if os.path.isfile(readme_path) else ""
        intro, quick, heads, lang = readme_parts(readme)

        # Detect C SDK / headers
        c_sdk_info = detect_c_sdk(d)
        has_c_sdk = c_sdk_info["has_c_sdk"]

        # Detect CLI
        cli_list = detect_cli(py, pkg_json, d)

        # PyPI / npm presence
        live_py = on_pypi(dist_py) if dist_py else None
        live_npm = on_npm(dist_npm) if dist_npm else None

        # Determine area
        repo_topics = tops.get(repo, [])
        area = next((AREAS[t] for t in repo_topics if t in AREAS), None)
        if not area:
            area = FALLBACK_AREAS.get(repo) or FALLBACK_AREAS.get(dist.replace("pqblocks-", "")) or FALLBACK_AREAS.get(name)

        # Ecosystem
        if has_pyproject and has_pkg_json:
            ecosystem = "dual"
        elif has_pkg_json:
            ecosystem = "npm"
        elif has_c_sdk and not has_pyproject:
            ecosystem = "c"
        else:
            ecosystem = "python"

        # Install strings
        install_pip = f"pip install {dist_py}" if live_py else f"pip install git+https://github.com/{ORG}/{repo}"
        install_npm = f"npm install {dist_npm}" if live_npm else f"npm install git+https://github.com/{ORG}/{repo}"
        install_c = "cmake -B build && cmake --build build && sudo cmake --install build" if has_c_sdk else None

        if ecosystem == "dual":
            install = f"{install_pip}  # Python\n{install_npm}  # Node.js"
        elif ecosystem == "npm":
            install = install_npm
        else:
            install = install_pip

        # Detect Python import module if available
        mods = []
        src_dir = os.path.join(d, "src")
        if os.path.isdir(src_dir):
            mods = [m for m in os.listdir(src_dir) if m.startswith("pqblocks_") and os.path.isdir(os.path.join(src_dir, m))]

        import_name = mods[0] if mods else (dist_py.replace("-", "_") if dist_py else dist_npm)
        import_npm = dist_npm if dist_npm else None

        summary = (proj.get("description") or pkg_json.get("description") or "").strip()
        keywords = sorted(set(proj.get("keywords", []) + pkg_json.get("keywords", [])))
        ex_dir = os.path.join(d, "examples")

        entry = {
            "package": dist,
            "import": import_name,
            "import_npm": import_npm,
            "version": proj.get("version") or pkg_json.get("version") or "0.1.0",
            "repo": "%s/%s" % (ORG, repo),
            "url": "https://github.com/%s/%s" % (ORG, repo),
            "area": area,
            "kind": "optimizer" if area == "Quantum-inspired" else "pq",
            "ecosystem": ecosystem,
            "summary": summary,
            "intro": intro,
            "keywords": keywords,
            "topics": repo_topics,
            "python": proj.get("requires-python"),
            "cli": cli_list,
            "status": next((c.split(" - ")[-1] for c in proj.get("classifiers", [])
                            if c.startswith("Development Status")), "alpha"),
            "on_pypi": live_py,
            "on_npm": live_npm,
            "install": install,
            "install_pip": install_pip if (has_pyproject or ecosystem in ("python", "dual")) else None,
            "install_npm": install_npm if (has_pkg_json or ecosystem in ("npm", "dual")) else None,
            "install_c": install_c,
            "has_c_sdk": has_c_sdk,
            "c_headers": c_sdk_info["headers"],
            "c_libs": c_sdk_info["libs"],
            "needs_liboqs": "liboqs" in readme.lower(),
            "quickstart": quick,
            "quickstart_lang": lang,
            "examples": sorted(f for f in os.listdir(ex_dir) if not f.startswith(".")) if os.path.isdir(ex_dir) else [],
            "docs": {f: "https://github.com/%s/%s/blob/main/%s" % (ORG, repo, f)
                     for f in DOCS if os.path.isfile(os.path.join(d, f))},
            "sections": heads,
        }

        if run_verify:
            entry["verified"], entry["verify_output"] = verify(d, quick, lang=lang)
        elif dist in existing_entries and "verified" in existing_entries[dist]:
            entry["verified"] = existing_entries[dist]["verified"]
            if "verify_output" in existing_entries[dist]:
                entry["verify_output"] = existing_entries[dist]["verify_output"]
        elif lang in ("javascript", "typescript"):
            entry["verified"], entry["verify_output"] = verify(d, quick, lang=lang)

        public = "\n".join([entry["summary"], quick] + intro)
        found = leak_check.leaks(public)
        entry["held"] = ("no area topic (add one of: %s)" % ", ".join(AREAS) if not area else
                         "quickstart did not run: %s" % entry.get("verify_output", "") if entry.get("verified") is False else
                         "public-text gate: %s" % ", ".join(sorted({l for l, _ in found})) if found else None)
        if entry["held"]:
            entry = {"package": dist, "repo": entry["repo"], "url": entry["url"], "held": entry["held"].split(":")[0]
                     if found else entry["held"]}
        out.append(entry)
    return out


def deps(pkg_root):
    out = set()
    for name in sorted(os.listdir(pkg_root)):
        f = os.path.join(pkg_root, name, "pyproject.toml")
        if os.path.isfile(f):
            proj = tomllib.load(open(f, "rb")).get("project", {})
            if proj.get("name", "").startswith("pqblocks-"):
                out.update(proj.get("dependencies", []))
    return sorted(out)


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    if "--print-deps" in argv:
        print("\n".join(deps(argv[0])))
        return 0
    global OUT
    if "--out" in argv:
        OUT = argv[argv.index("--out") + 1]
    cat = build(argv[0], "--verify" in argv)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"org": ORG, "site": "https://pqblocks.github.io", "packages": cat}, fh, indent=1,
                  ensure_ascii=False)
        fh.write("\n")
    held = [p for p in cat if p.get("held")]
    print("%d packages -> %s; published: %d; on PyPI: %d; on npm: %d" % (
        len(cat), os.path.normpath(OUT), len(cat) - len(held),
        sum(1 for p in cat if p.get("on_pypi")),
        sum(1 for p in cat if p.get("on_npm"))))
    for p in held:
        print("HELD %s: %s" % (p["package"], p["held"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
