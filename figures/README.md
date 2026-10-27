# Custom figures

Isometric line figures drawn for this site with the `hairline-create` skill of
[lucasmarkes/hairline](https://github.com/lucasmarkes/hairline) (MIT), on its kernel
(`docs/assets/vendor/hairline/kernel.js`, unchanged).

| Figure | Where | What it shows |
|---|---|---|
| `assemble.js` | home page | A core block and one loose block per package; near the pointer they slide into five branches, one per area, and links draw out. Pointing toward a branch lights that area. |
| `swap.js` | transition map | Seven blocks in a tray: the one under the pointer lifts out of its slot and its neighbours part. One block replaced without touching the rest. |

To change a figure, edit it here, check it with the skill (`node look.mjs swap.js --answer 136,15,40 --edge 194,30,44`),
then run `python3 scripts/gen_figures.py`, which wraps each figure in its own scope for the site.
