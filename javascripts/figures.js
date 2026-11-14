// Interactive line figures, placed with <div class="pqb-figure" data-figure="NAME" data-label="..."></div>.
// NAME is one of the package's figures (hairline, MIT, vendored) or one of this site's own figures,
// drawn with the hairline-create skill on its kernel and registered in window.PQB_FIGURES.
// Material's instant navigation swaps pages without a reload, so figures are mounted on every page
// change (document$) and torn down before the next one. The scheme follows Material's toggle.
import * as hairline from "../assets/vendor/hairline/index.js";

let mounted = [];

const scheme = () => (document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "light");

/** A site figure, mounted the way the hairline bench mounts one. */
function mountCustom(el, fig) {
  const HL = window.HL;
  HL.inject(document);
  el.setAttribute("data-hairline", fig.name);
  el.setAttribute("data-hairline-theme", scheme());
  el.setAttribute("role", "img");
  el.setAttribute("aria-label", el.dataset.label || fig.means);
  const svg = HL.mk("svg", { viewBox: "0 0 400 320", "aria-hidden": "true" }, el);
  const read = { textContent: "rest" };
  const handle = fig.mount({ stage: el, svg, read }, fig.range[1]);
  return {
    update: ({ theme }) => el.setAttribute("data-hairline-theme", theme),
    destroy: () => { handle.destroy(); svg.remove(); },
  };
}

function mountAll() {
  mounted.forEach((f) => f.destroy());
  mounted = [];
  document.querySelectorAll(".pqb-figure[data-figure]").forEach((el) => {
    const name = el.dataset.figure, custom = (window.PQB_FIGURES || {})[name];
    if (custom && window.HL) mounted.push(mountCustom(el, custom));
    else if (typeof hairline[name] === "function")
      mounted.push(hairline[name](el, { theme: scheme(), intensity: 0.6, label: el.dataset.label || undefined }));
  });
}

new MutationObserver(() => mounted.forEach((f) => f.update({ theme: scheme() })))
  .observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

if (window.document$) window.document$.subscribe(mountAll);
else mountAll();
