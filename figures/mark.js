/**
 * Mark: the PQBlocks mark built as four blocks in a square on a round plate.
 * At rest it is the logo: one diagonal pair stands tall and the other sits low,
 * the near block lit. The block under the pointer rises to its full height and
 * the rest settle, staggered outward from it, so any block can lead. The
 * read-out names the block. The slider is the rise.
 *
 * The pattern: one of many. Tweens, a stagger by distance, a hit test on the
 * blocks' resting centres, and the logo as the rest pose.
 */
const { Cam, circ, facing, fit, mk, open, pointer, poly, prism, proj, put, ringAt, register, rings, disposer, solid, tween, tset, tval, tdone } = HL;

const S = 22, GAP = 5, HI = 26, LO = 8, R = 46, PLATE = 5;
const CELLS = [[0, 0], [1, 0], [0, 1], [1, 1]];       // back, right, left, front
const REST = [LO, HI, HI, LO];                        // the logo: the side-by-side diagonal raised

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let rise = value;
  const C = Cam(45, 0.5, 2.7);
  fit(C, [[-R, -R, 0], [R, R, 0], [R, -R, 0], [-R, R, 0], [0, 0, PLATE + HI + 18]], 200, 172);
  const P = proj(C), front = facing(C);

  const g = mk("g", {}, svg);
  put(solid(g), prism(P, front, circ(R, 40), circ(R - 2.4, 40), 0, PLATE));
  mk("path", { d: poly(ringAt(P, circ(R - 8, 40), PLATE)), class: "nf dash" }, g);
  let ticks = "";
  for (let k = 0; k < 24; k++) {
    const a = (k * Math.PI) / 12, r0 = R - 5, r1 = R - (k % 6 ? 3.5 : 1.5);
    ticks += open([P(Math.cos(a) * r0, Math.sin(a) * r0, PLATE), P(Math.cos(a) * r1, Math.sin(a) * r1, PLATE)]);
  }
  mk("path", { d: ticks, class: "nf lo" }, g);

  const o = -(S + GAP / 2);
  const blocks = CELLS.map(([i, j], k) => {
    const x0 = o + i * (S + GAP), y0 = o + j * (S + GAP), [ring, inner] = rings(x0, y0, x0 + S, y0 + S, 4.5, 1.6);
    return { k, ring, inner, cx: x0 + S / 2, cy: y0 + S / 2, h: tween(REST[k]), el: solid(g), drawn: NaN };
  });
  const draw = (b, now) => {
    const h = tval(b.h, now);
    if (h === b.drawn) return;
    b.drawn = h;
    put(b.el, prism(P, front, b.ring, b.inner, PLATE, PLATE + h));
  };
  const B = register(stage, (_dt, now) => {
    let m = false;
    blocks.forEach((b) => { draw(b, now); if (!tdone(b.h, now)) m = true; });
    return m;
  });
  bag.add(B.unregister);

  let lit = null;
  const light = (b) => { if (lit) lit.el.sil.classList.remove("hi"); lit = b; b.el.sil.classList.add("hi"); };
  light(blocks[1]);

  const restC = blocks.map((b) => P(b.cx, b.cy, PLATE + REST[b.k] / 2));
  const pick = ([sx, sy]) => {
    let best = -1, bd = 26;
    restC.forEach(([x, y], k) => { const d = Math.hypot(x - sx, y - sy); if (d < bd) { bd = d; best = k; } });
    return best;
  };

  let chosen = -2;
  function choose(k) {
    if (k === chosen) return;
    const now = performance.now(), from = k >= 0 ? k : Math.max(chosen, 0);
    chosen = k;
    blocks.forEach((b) => {
      const d = Math.abs(CELLS[b.k][0] - CELLS[from][0]) + Math.abs(CELLS[b.k][1] - CELLS[from][1]);
      tset(b.h, k < 0 ? REST[b.k] : b.k === k ? HI + rise : LO, now, d * 45);
    });
    light(k >= 0 ? blocks[k] : blocks[1]);
    read.textContent = k >= 0 ? "block " + (k + 1) : "rest";
    B.wake();
  }

  bag.add(pointer(stage, { move: (p) => choose(pick(p)), leave: () => choose(-1) }));
  bag.add(() => svg.replaceChildren());
  return { set: (v) => { rise = v; }, destroy: bag.dispose };
}

hairline({
  name: "mark",
  means: "The PQBlocks mark as four blocks: the one under the pointer rises, and the others settle around it.",
  rules: [1, 2, 4, 5],
  range: [4, 10, 18],
  tour: [[200, 120], [250, 170], [150, 170], null],
  mount,
});
