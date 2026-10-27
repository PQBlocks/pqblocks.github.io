# Custom figures

Isometric line figures drawn for this site with the `hairline-create` skill of
[lucasmarkes/hairline](https://github.com/lucasmarkes/hairline) (MIT), on its kernel
(`docs/assets/vendor/hairline/kernel.js`, unchanged).

| Figure | Where | What it shows |
|---|---|---|
| `construct.js` | home page | Modules scattered on a round platform. The module under the pointer lifts; at the core they fly in to form the frame and the processor chip of a quantum computer, then its cryostat stages and coaxial lines grow round them. |
| `lattice.js` | home page, Why lattices | Pillars on a skewed 2-D lattice (the structure behind ML-KEM and ML-DSA): the closest lattice point to the pointer rises, found by rounding in the basis and checking neighbours, and a dashed path of whole basis steps draws to it. |
| `assemble.js` | package catalog | A core block and one loose block per package; near the pointer they slide into five branches, one per area, and links draw out. Pointing toward a branch lights that area. |
| `swap.js` | transition map | Seven blocks in a tray: the one under the pointer lifts out of its slot and its neighbours part. One block replaced without touching the rest. |

To change a figure, edit it here, check it with the skill (`node look.mjs swap.js --answer 136,15,40 --edge 194,30,44`),
then run `python3 scripts/gen_figures.py`, which wraps each figure in its own scope for the site.
