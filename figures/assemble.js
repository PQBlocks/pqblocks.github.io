/**
 * Assemble: a core block with four studs and twenty-six loose tiles scattered
 * round it, in five groups of 4, 7, 4, 2 and 9. As the pointer comes near the
 * core the tiles straighten and slide into five branches, inner tiles first,
 * and dashed links draw out from the core. Pointing toward a branch lights it.
 * The slider is the reach: how far away the assembly starts.
 *
 * The pattern: a continuous field. One spring per tile, a falloff by distance
 * that spreads from the core outward, a hit test on the ground plane (which
 * never moves), and a scattered rest that is a composition.
 */
const {
  Cam, clamp, facing, fit, lerp, mk, open, pointer, prism, proj, put, rad, register, rrect,
  disposer, solid, spring, stepS, unproj,
} = HL;

// packages per area: the site sets window.PQB_AREA_COUNTS from its catalog; the bench uses today's counts.
// A branch draws at most nine tiles so the frame holds; the read-out keeps the real count.
const COUNTS = (typeof window !== "undefined" && window.PQB_AREA_COUNTS) || [4, 7, 4, 2, 9];
const GROUPS = COUNTS.map((n) => Math.min(n, 9)), HUB = 17, HUB_H = 13, STUD_R = 3.6, STUD_H = 3.2;
const T = 6.4, T_H = 4.2, ROW = 21, FAN = 16.5, R0 = 43, CORE = 34;

/** A ring of samples rotated by th about the origin and moved to (cx, cy): rings() only makes square ones. */
const turn = (ring, cx, cy, th) => {
  const c = Math.cos(th), s = Math.sin(th);
  return ring.map((q) => ({ u: cx + q.u * c - q.v * s, v: cy + q.u * s + q.v * c, nu: q.nu * c - q.nv * s, nv: q.nu * s + q.nv * c }));
};
const TILE = rrect(-T, -T, T, T, 2.4, 4), TILE_IN = rrect(-T + 1.3, -T + 1.3, T - 1.3, T - 1.3, 1.1, 4);
const STUD = rrect(-STUD_R, -STUD_R, STUD_R, STUD_R, STUD_R, 4), STUD_IN = rrect(-STUD_R + 0.8, -STUD_R + 0.8, STUD_R - 0.8, STUD_R - 0.8, STUD_R - 0.8, 4);

/** Every tile's place in the tree and its place at rest: a fixed scatter, so the rest pose is the same each time. */
function layout() {
  const tiles = [];
  let seed = 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;
  GROUPS.forEach((n, b) => {
    const a = rad(-90 + b * 72), ax = Math.cos(a), ay = Math.sin(a), px = -ay, py = ax;
    for (let k = 0; k < n; k++) {
      const row = Math.floor(k / 3), inRow = Math.min(3, n - row * 3), col = (k % 3) - (inRow - 1) / 2;
      const r = R0 + row * ROW, tx = ax * r + px * col * FAN, ty = ay * r + py * col * FAN;
      const spread = 1.42 + rnd() * 0.08;
      tiles.push({ b, k, tx, ty, tth: a, rx: tx * spread + rnd() * 5, ry: ty * spread + rnd() * 5,
        rth: a + rad(rnd() * 34), depth: row / 2 });
    }
  });
  return tiles;
}

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let reach = value, over = null, branch = -1;
  const tiles = layout();

  const C = Cam(45, 0.5, 1.36);
  const ext = tiles.flatMap((t) => [[t.rx, t.ry, 0], [t.tx, t.ty, 0]]);
  fit(C, ext.concat([[0, 0, HUB_H + STUD_H + 4]]), 200, 170);
  const P = proj(C), front = facing(C);

  const g = mk("g", {}, svg);
  // links, painted first so every plate covers them; each grows out from the core with its tile
  const links = tiles.map(() => mk("path", { class: "nf dash" }, g));
  const hub = { g: mk("g", {}, g), y: 0, x: 0 };
  const hubBody = solid(hub.g), studs = [0, 1, 2, 3].map(() => solid(hub.g));
  const top = HUB_H + 2.4;
  put(solid(hub.g), prism(P, front, turn(rrect(-HUB, -HUB, HUB, HUB, 6, 6), 0, 0, 0), turn(rrect(-HUB + 2, -HUB + 2, HUB - 2, HUB - 2, 4, 6), 0, 0, 0), 0, 2.4));
  put(hubBody, prism(P, front, turn(rrect(-HUB + 3, -HUB + 3, HUB - 3, HUB - 3, 5, 6), 0, 0, 0), turn(rrect(-HUB + 4.6, -HUB + 4.6, HUB - 4.6, HUB - 4.6, 3.6, 6), 0, 0, 0), 2.4, top));
  [[-6.5, -6.5], [6.5, -6.5], [-6.5, 6.5], [6.5, 6.5]].forEach(([sx, sy], i) =>
    put(studs[i], prism(P, front, turn(STUD, sx, sy, 0), turn(STUD_IN, sx, sy, 0), top, top + STUD_H)));
  tiles.forEach((t) => { t.el = solid(mk("g", {}, g)); t.sp = spring(0, { eps: 0.002 }); t.drawn = NaN; });

  const order = (items) => items.slice().sort((a, b) => a.x + a.y - (b.x + b.y));
  let lastOrder = "";
  function paint() {
    // back to front by x + y; move groups only when the order changes
    const items = tiles.map((t) => ({ el: t.el.g, x: lerp(t.rx, t.tx, t.sp.x), y: lerp(t.ry, t.ty, t.sp.x) })).concat([{ el: hub.g, x: 0, y: 0 }]);
    const sorted = order(items), key = sorted.map((i) => i.el === hub.g ? "h" : tiles.findIndex((t) => t.el.g === i.el)).join(",");
    if (key === lastOrder) return;
    lastOrder = key;
    sorted.forEach((i) => g.appendChild(i.el));
  }
  function drawTile(t, i) {
    const s = t.sp.x;
    if (Math.abs(s - t.drawn) < 0.0005) return;
    t.drawn = s;
    const x = lerp(t.rx, t.tx, s), y = lerp(t.ry, t.ty, s), th = lerp(t.rth, t.tth, s);
    put(t.el, prism(P, front, turn(TILE, x, y, th), turn(TILE_IN, x, y, th), 0, T_H));
    // the link draws from the core (or the tile before it in its branch) toward the tile as it settles
    const from = t.k < 3 ? [Math.cos(t.tth) * CORE * 0.62, Math.sin(t.tth) * CORE * 0.62] : [tiles[i - 3].tx, tiles[i - 3].ty];
    const k = clamp((s - 0.35) / 0.65, 0, 1);
    links[i].setAttribute("d", k <= 0 ? "" : open([P(from[0], from[1], 1), P(lerp(from[0], t.tx, k), lerp(from[1], t.ty, k), 1)]));
  }

  const B = register(stage, (dt) => {
    let m = false;
    tiles.forEach((t, i) => { if (stepS(t.sp, dt)) m = true; drawTile(t, i); });
    paint();
    return m;
  });
  bag.add(B.unregister);

  function light(b) {
    hubBody.sil.classList.toggle("hi", b < 0);
    studs.forEach((s) => s.sil.classList.toggle("hi", b < 0));
    tiles.forEach((t) => t.el.sil.classList.toggle("hi", t.b === b));
  }
  light(-1);

  function retarget() {
    // assembly: 1 near the core, falling to 0 at the reach; outer rows lag, so it spreads from the core
    const d = over ? Math.hypot(over[0], over[1]) : Infinity;
    const A = clamp(1 - (d - CORE) / reach, 0, 1);
    tiles.forEach((t) => { t.sp.t = clamp((A * 1.5 - t.depth * 0.5), 0, 1); });
    // the branch the pointer faces, read from the ground plane, once the tree has mostly formed
    let b = -1;
    if (over && A > 0.55) {
      const ang = (Math.atan2(over[1], over[0]) * 180) / Math.PI + 90;
      b = ((Math.round(ang / 72) % 5) + 5) % 5;
    }
    if (b !== branch) { branch = b; light(b); }
    read.textContent = b >= 0 ? "area " + (b + 1) + " · " + String(COUNTS[b]).padStart(2, "0") : A > 0 ? "tree " + Math.round(A * 100) + "%" : "rest";
    B.wake();
  }

  bag.add(pointer(stage, {
    move: (p) => { over = unproj(C, p[0], p[1], 0); retarget(); },
    leave: () => { over = null; retarget(); },
  }));
  bag.add(() => svg.replaceChildren());
  return { set: (v) => { reach = v; retarget(); }, destroy: bag.dispose };
}

hairline({
  name: "assemble",
  means: "Loose blocks round a core, one per package, slide into five branches as the pointer comes near, and links draw out.",
  rules: [1, 3, 5, 6],
  range: [40, 80, 130],
  tour: [[195, 172], [165, 200], [155, 168], null],
  mount,
});
