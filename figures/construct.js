/**
 * Construct: twenty-six blocks lie scattered on the orbits of a round platform.
 * The block under the pointer lifts and takes the bright stroke. Bring the
 * pointer to the core pad at the centre and every block arcs in, lowest tiers
 * first, and they stack into one structure: two square tiers, a cross, and a
 * spire of three narrowing turned blocks. The slider is the arc: how high the
 * blocks fly on their way in.
 *
 * The pattern: one of many (a block answers) and a field (the build answers
 * the distance to the core). A spring for the build, each block offset by its
 * tier so the structure rises bottom-up, hit tests on rest poses and on the
 * ground plane, guides painted behind the plates, and a scattered rest.
 */
const {
  Cam, circ, clamp, facing, fit, flatDot, lerp, mk, open, place, pointer, poly, prism, proj, put, rad,
  register, ringAt, rrect, disposer, solid, spring, stepS, tween, tset, tval, tdone, unproj,
} = HL;

const R_PLATE = 104, PLATE_H = 6, R_PAD = 40, PAD_H = 2.6, BASE = PLATE_H + PAD_H, CORE = 34;
const CELL = 21, ORBITS = [62, 86];
// the structure, bottom up: [x, y, tier, size, height, turn in degrees]. The second tier is the first
// turned 45 degrees (a star over a square), then a cross, then a spire of three narrowing turned blocks.
const TIERS = [];
const D = Math.SQRT1_2;
for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) TIERS.push([i * CELL, j * CELL, 0, 19, 12, 0]);
for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) TIERS.push([(i - j) * CELL * D, (i + j) * CELL * D, 1, 16, 12, 45]);
[[0, 0], [CELL, 0], [-CELL, 0], [0, CELL], [0, -CELL]].forEach(([x, y]) => TIERS.push([x, y, 2, 15, 12, 0]));
TIERS.push([0, 0, 3, 15, 14, 45], [0, 0, 4, 10, 18, 45], [0, 0, 5, 6, 26, 45]);
const TOPS = [0, 12, 24, 36, 50, 68];                            // each tier's floor above the pad

const turn = (ring, cx, cy, th) => {
  const c = Math.cos(th), s = Math.sin(th);
  return ring.map((q) => ({ u: cx + q.u * c - q.v * s, v: cy + q.u * s + q.v * c, nu: q.nu * c - q.nv * s, nv: q.nu * s + q.nv * c }));
};

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let arc = value;

  // the scatter: every block on one of two orbits, at its own angle and turn
  let seed = 11;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) * 2 - 1;
  const blocks = TIERS.map(([tx, ty, tier, size, h, tdeg], i) => {
    const a = rad(i * (360 / TIERS.length) + rnd() * 5), r = ORBITS[i % 2] + rnd() * 5;
    const half = size / 2, ring = rrect(-half, -half, half, half, Math.min(3, half * 0.45), 4);
    const inner = rrect(-half + 1.2, -half + 1.2, half - 1.2, half - 1.2, Math.min(1.8, half * 0.3), 4);
    return { i, tier, h, ring, inner, tx, ty, tz: BASE + TOPS[tier], tth: rad(tdeg),
      rx: Math.cos(a) * r, ry: Math.sin(a) * r, rth: rad(rnd() * 40), lift: tween(0), drawn: "" };
  });

  const C = Cam(45, 0.5, 1.5);
  fit(C, [[-R_PLATE, -R_PLATE, 0], [R_PLATE, R_PLATE, 0], [R_PLATE, -R_PLATE, 0], [-R_PLATE, R_PLATE, 0],
    [0, 0, BASE + TOPS[5] + 26 + 4]], 200, 180);
  const P = proj(C), front = facing(C);

  const g = mk("g", {}, svg);
  // the platform: a disc, a rim line set into its top, and the core pad
  put(solid(g), prism(P, front, circ(R_PLATE, 40), circ(R_PLATE - 2.6, 40), 0, PLATE_H));
  mk("path", { d: poly(ringAt(P, circ(R_PLATE - 9, 40), PLATE_H)), class: "nf lo" }, g);
  // guides on the deck: the two orbits and eight spokes, all behind the plates
  ORBITS.forEach((r) => mk("path", { d: poly(ringAt(P, circ(r, 40), PLATE_H)), class: "nf dash" }, g));
  let spokes = "";
  for (let k = 0; k < 8; k++) {
    const a = rad(22.5 + k * 45);
    spokes += open([P(Math.cos(a) * (R_PAD + 4), Math.sin(a) * (R_PAD + 4), PLATE_H), P(Math.cos(a) * (R_PLATE - 12), Math.sin(a) * (R_PLATE - 12), PLATE_H)]);
  }
  mk("path", { d: spokes, class: "nf dash" }, g);
  // rim beacons: twelve dim dots
  for (let k = 0; k < 12; k++) {
    const a = rad(k * 30), d = flatDot(g, C, 0.9, "dot off");
    place(d, P(Math.cos(a) * (R_PLATE - 5), Math.sin(a) * (R_PLATE - 5), PLATE_H));
  }
  const pad = solid(g);
  put(pad, prism(P, front, circ(R_PAD, 28), circ(R_PAD - 2.2, 28), PLATE_H, BASE));
  mk("path", { d: poly(ringAt(P, circ(R_PAD - 8, 28), BASE)), class: "nf lo" }, g);

  const layer = mk("g", {}, g);
  blocks.forEach((b) => { b.el = solid(mk("g", {}, layer)); });
  const build = spring(0, { eps: 0.002 });

  /** Where block b stands: its scatter, its place in the structure, or on the arc between. */
  function pose(b, now) {
    const s = clamp(build.x * 1.6 - b.tier * 0.12, 0, 1);
    const x = lerp(b.rx, b.tx, s), y = lerp(b.ry, b.ty, s), th = lerp(b.rth, b.tth, s);
    const z = lerp(PLATE_H, b.tz, s) + Math.sin(Math.PI * s) * arc + tval(b.lift, now) * (1 - s);
    return { x, y, z, th };
  }

  let order = "";
  function draw(now) {
    const poses = blocks.map((b) => pose(b, now));
    blocks.forEach((b, k) => {
      const q = poses[k], key = [q.x, q.y, q.z, q.th].map((v) => v.toFixed(2)).join();
      if (key === b.drawn) return;
      b.drawn = key;
      put(b.el, prism(P, front, turn(b.ring, q.x, q.y, q.th), turn(b.inner, q.x, q.y, q.th), q.z, q.z + b.h));
    });
    // back to front, and bottom to top within the structure
    const depth = (q) => q.x + q.y + q.z * 1.6;
    const idx = blocks.map((_, k) => k).sort((a, c) => depth(poses[a]) - depth(poses[c]));
    const key = idx.join();
    if (key !== order) { order = key; idx.forEach((k) => layer.appendChild(blocks[k].el.g)); }
  }

  const B = register(stage, (dt, now) => {
    let m = stepS(build, dt);
    blocks.forEach((b) => { if (!tdone(b.lift, now)) m = true; });
    draw(now);
    return m;
  });
  bag.add(B.unregister);

  // hit tests: the core on the ground plane; a block by its RESTING centre on screen
  const restC = blocks.map((b) => P(b.rx, b.ry, PLATE_H + b.h / 2));
  function pickBlock([sx, sy]) {
    let best = -1, bd = 16;
    restC.forEach(([x, y], k) => { const d = Math.hypot(x - sx, y - sy); if (d < bd) { bd = d; best = k; } });
    return best;
  }

  let lit = null;
  function light(el) {
    if (el === lit) return;
    if (lit) lit.classList.remove("hi");
    lit = el;
    if (lit) lit.classList.add("hi");
  }
  light(pad.sil);

  let picked = -1;
  function answer(p) {
    const over = p ? unproj(C, p[0], p[1], PLATE_H) : null;
    const d = over ? Math.hypot(over[0], over[1]) : Infinity;
    build.t = d <= CORE ? 1 : 0;
    const k = p && d > CORE ? pickBlock(p) : -1;
    if (k !== picked) {
      const now = performance.now();
      if (picked >= 0) tset(blocks[picked].lift, 0, now, 0);
      if (k >= 0) tset(blocks[k].lift, 9, now, 0);
      picked = k;
    }
    if (build.t > 0) { light(blocks[blocks.length - 1].el.sil); read.textContent = "build"; }
    else if (k >= 0) { light(blocks[k].el.sil); read.textContent = "block " + String(k + 1).padStart(2, "0"); }
    else { light(pad.sil); read.textContent = "rest"; }
    B.wake();
  }

  bag.add(pointer(stage, { move: (p) => answer(p), leave: () => answer(null) }));
  bag.add(() => svg.replaceChildren());
  return { set: (v) => { arc = v; B.wake(); }, destroy: bag.dispose };
}

hairline({
  name: "construct",
  means: "Blocks scattered on a platform: the one under the pointer lifts; at the core they all fly in and build one structure.",
  rules: [1, 3, 5, 6],
  range: [8, 22, 40],
  tour: [[291, 232], [200, 184], [120, 200], null],
  mount,
});
