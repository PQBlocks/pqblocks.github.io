// Custom figures call hairline({ name, means, range, mount, ... }) when they load; keep them by name.
window.PQB_FIGURES = window.PQB_FIGURES || {};
window.hairline = function (figure) { window.PQB_FIGURES[figure.name] = figure; };
