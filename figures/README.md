# Custom figures

Isometric line figures drawn for this site with the `hairline-create` skill of
[lucasmarkes/hairline](https://github.com/lucasmarkes/hairline) (MIT), on its kernel
(`docs/assets/vendor/hairline/kernel.js`, unchanged).

| Figure | Where | What it shows |
|---|---|---|
| `swap.js` | home page | Seven blocks in a tray: the one under the pointer lifts out of its slot and its neighbours part. One block replaced without touching the rest. |

To change a figure, edit it here, check it with the skill (`node look.mjs swap.js --answer 136,15,40 --edge 194,30,44`),
then run `python3 scripts/gen_figures.py`, which wraps each figure in its own scope for the site.
