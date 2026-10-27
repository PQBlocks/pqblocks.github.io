#!/usr/bin/env python3
"""Draw the site's SVG diagrams (light and dark variants) from data/catalog.json.

    python3 scripts/gen_diagrams.py     # writes docs/assets/diagrams/*.svg

Counts and package names come from the catalog, so the pictures never drift from the packages.
Planned channels are drawn dashed and labelled "roadmap"; only shipped things are solid.
"""
import json
import os
from xml.sax.saxutils import escape

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "assets", "diagrams")
THEMES = {
    "light": {"bg": "#ffffff", "panel": "#f8fafc", "line": "#cbd5e1", "text": "#0f172a", "muted": "#475569",
              "a": "#0891b2", "b": "#7c3aed", "chip": "#e2e8f0"},
    "dark": {"bg": "#0b1220", "panel": "#111a2e", "line": "#334155", "text": "#e2e8f0", "muted": "#94a3b8",
             "a": "#22d3ee", "b": "#a78bfa", "chip": "#1e293b"},
}
AREAS = ["PQ cryptography", "Migration & readiness", "Interoperability", "Conformance", "Quantum-inspired"]
FONT = "font-family=\"Inter, 'Segoe UI', system-ui, sans-serif\""


def svg(w, h, body, label, t):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
            'aria-label="%s" %s>\n<defs><linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>\n'
            '<rect width="%d" height="%d" rx="16" fill="%s"/>\n%s\n</svg>\n'
            % (w, h, w, h, escape(label), FONT, t["a"], t["b"], w, h, t["bg"], body))


def text(x, y, s, t, size=14, weight=400, color=None, anchor="middle"):
    return '<text x="%d" y="%d" font-size="%d" font-weight="%d" fill="%s" text-anchor="%s">%s</text>' % (
        x, y, size, weight, color or t["text"], anchor, escape(s))


def top_of_channels(box_h):
    return 116 + box_h + 36


def ecosystem(pkgs, t):
    most = max(min(sum(1 for p in pkgs if p["area"] == a), 10) for a in AREAS)
    box_h = 92 + most * 25
    w, h = 1200, top_of_channels(box_h) + 110
    out = [text(w // 2, 52, "PQBlocks ecosystem", t, 26, 700),
           text(w // 2, 80, "%d packages across five areas of the post-quantum transition" % len(pkgs), t, 15, 400, t["muted"])]
    bw, gap, top = 212, 20, 116
    x0 = (w - (5 * bw + 4 * gap)) // 2
    for i, area in enumerate(AREAS):
        x = x0 + i * (bw + gap)
        names = sorted(p["package"][9:] for p in pkgs if p["area"] == area)
        if len(names) > 10:                       # keep the box readable as the catalog grows
            names = names[:9] + ["+%d more" % (len(names) - 9)]
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s" stroke="%s"/>' % (x, top, bw, box_h, t["panel"], t["line"]))
        out.append('<rect x="%d" y="%d" width="%d" height="5" rx="2" fill="url(#acc)"/>' % (x, top, bw))
        out.append(text(x + bw // 2, top + 36, area, t, 15, 700))
        out.append(text(x + bw // 2, top + 58, "%d packages" % len(names), t, 13, 400, t["muted"]))
        for j, n in enumerate(names):
            out.append('<rect x="%d" y="%d" width="%d" height="22" rx="11" fill="%s"/>' % (x + 16, top + 74 + j * 25, bw - 32, t["chip"]))
            out.append(text(x + bw // 2, top + 89 + j * 25, n, t, 12, 500))
    # delivery channels: solid = shipped, dashed = roadmap
    cy = top_of_channels(box_h)
    out.append(text(w // 2, cy, "Delivery channels", t, 15, 700))
    chans = [("Python packages", True), ("npm modules", False), ("Native SDKs", False), ("CLIs", True), ("MCP + agent skills", True), ("Hosted services", False)]
    cw, cg = 170, 14
    cx0 = (w - (len(chans) * cw + (len(chans) - 1) * cg)) // 2
    for i, (name, live) in enumerate(chans):
        x = cx0 + i * (cw + cg)
        dash = "" if live else ' stroke-dasharray="6 5"'
        out.append('<rect x="%d" y="%d" width="%d" height="44" rx="10" fill="%s" stroke="%s" stroke-width="1.5"%s/>'
                   % (x, cy + 16, cw, t["panel"] if live else t["bg"], t["a"] if live else t["line"], dash))
        out.append(text(x + cw // 2, cy + 36, name, t, 13, 600))
        out.append(text(x + cw // 2, cy + 52, "available" if live else "roadmap", t, 11, 400, t["a"] if live else t["muted"]))
    return svg(w, h, "\n".join(out), "PQBlocks ecosystem: five areas and delivery channels", t)


def pipeline(pkgs, t):
    steps = [("Discover", "find every algorithm", ["scan", "lint"]),
             ("Assess", "score and document", ["cbom", "agility"]),
             ("Govern", "enforce in CI", ["policy", "jwe-audit", "cnsa-evidence"]),
             ("Migrate", "hybrid PQ primitives", ["core", "primitives", "jose", "files"]),
             ("Interoperate", "carry it on the wire", ["tls-interop", "wire", "csr-pop", "jwe"]),
             ("Verify", "prove it is correct", ["acvp", "fips-check"])]
    live = {p["package"][9:] for p in pkgs}
    steps = [(a, b, [n for n in c if n in live]) for a, b, c in steps]
    w, h = 1200, 340
    out = [text(w // 2, 40, "The post-quantum migration, step by step", t, 22, 700),
           text(w // 2, 64, "package names below omit the pqblocks- prefix", t, 12, 400, t["muted"])]
    bw, gap, top = 170, 26, 92
    x0 = (w - (6 * bw + 5 * gap)) // 2
    for i, (name, sub, pk) in enumerate(steps):
        x = x0 + i * (bw + gap)
        out.append('<rect x="%d" y="%d" width="%d" height="214" rx="12" fill="%s" stroke="%s"/>' % (x, top, bw, t["panel"], t["line"]))
        out.append('<circle cx="%d" cy="%d" r="16" fill="url(#acc)"/>' % (x + 28, top + 30))
        out.append(text(x + 28, top + 35, str(i + 1), {"text": t["bg"]}, 14, 700))
        out.append(text(x + 52, top + 35, name, t, 16, 700, anchor="start"))
        out.append(text(x + bw // 2, top + 64, sub, t, 12, 400, t["muted"]))
        for j, n in enumerate(pk):
            out.append('<rect x="%d" y="%d" width="%d" height="24" rx="12" fill="%s"/>' % (x + 14, top + 84 + j * 30, bw - 28, t["chip"]))
            out.append(text(x + bw // 2, top + 100 + j * 30, n, t, 12, 500))
        if i < 5:
            ax = x + bw + 4
            out.append('<path d="M%d %d h%d" stroke="%s" stroke-width="2.5"/>' % (ax, top + 107, gap - 10, t["b"]))
            out.append('<path d="M%d %d l-6 -5 v10 z" fill="%s"/>' % (ax + gap - 4, top + 107, t["b"]))
    return svg(w, h, "\n".join(out), "Post-quantum migration steps and the PQBlocks packages for each", t)


def main():
    pkgs = [p for p in json.load(open(os.path.join(ROOT, "data", "catalog.json")))["packages"]
            if not p.get("held") and p.get("verified") is True]
    os.makedirs(OUT, exist_ok=True)
    for name, t in THEMES.items():
        open(os.path.join(OUT, "ecosystem-%s.svg" % name), "w").write(ecosystem(pkgs, t))
        open(os.path.join(OUT, "pipeline-%s.svg" % name), "w").write(pipeline(pkgs, t))
    print("diagrams ->", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
