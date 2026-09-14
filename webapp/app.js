// Castle Foundry :: Enfilade Terminal frontend.
//
// Drawing model taken from vii.js: draw the field cell-by-cell into a
// <canvas> via context.fillRect, one flat color per live cell, with a
// 1px gutter that reads as a continuous grid rather than boxes-per-block.
// No per-block outlines or inset shading. Cell size auto-fits so grids up
// to 100 x 50 render legibly at ~8-10px per cell.

import * as C from "./castles.js";

// -------- palette (single phosphor scheme, no more color cycling) --------
const FILL_ALIVE = "#7ab87a";   // living stone
const FILL_DEAD  = "#0b1a10";   // mortar (dead cell / bg)
const GRID_LINE  = "#173626";   // gutter

// -------- canvas sizing --------------------------------------------------
// Cell size floats between a min (tiny for 100x50 grids) and a max (chunky
// for a 3x3). The canvas backing store is sized to whatever fits at that
// cell size. CSS caps display width so nothing overflows.
const CELL_MIN = 4;
const CELL_MAX = 42;
const FIELD_MAX_W = 1200;    // px cap when computing which cellSize fits
const FIELD_MAX_H = 640;

// -------- helpers -------------------------------------------------------
const helpers = {
  registerEvent(el, type, fn, capture) {
    if (el.addEventListener) el.addEventListener(type, fn, !!capture);
  },
  clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); },
};

// -------- state ---------------------------------------------------------
const state = {
  designer: {
    profile: [1, 2, 3, 4, 5, 4, 3, 2, 1],
    gridOn: true,
    asciiOn: false,
    canvas: null,
    ctx: null,
    mouseDown: false,
    lastX: -1,
    lastY: -1,
    dragMode: 0,
    // cached geometry from the last draw (for mousePosition):
    cellSize: 0,
    cellSpace: 0,
    offX: 0,
    offY: 0,
    rows: 0,
    cols: 0,
  },
  inspector: {
    profile: [0, 1, 2, 1, 0],
    gridOn: true,
    asciiOn: false,
    canvas: null,
    ctx: null,
    cellSize: 0,
    cellSpace: 0,
    offX: 0,
    offY: 0,
    rows: 0,
    cols: 0,
  },
};

// ------------------------------------------------------------------------
// Field renderer (GoL-style: flat cells, 1px gutter, auto-fit cellSize)
// ------------------------------------------------------------------------

function drawField(view) {
  const { profile, ctx, canvas, gridOn } = view;
  const cols = profile.length;
  const maxProfile = cols ? Math.max(...profile) : 0;
  // rows shown = baseline (row 0 filled) + towers + one air row on top.
  // Also enforce a minimum viewable height so a flat castle isn't a sliver.
  const heightCap = view.heightCap || (maxProfile + 2);
  const rows = Math.max(maxProfile + 2, heightCap);

  const cellSpace = gridOn ? 1 : 0;

  // Largest cellSize that fits inside FIELD_MAX_{W,H}, then floored to
  // [CELL_MIN, CELL_MAX] so tiny castles still look chunky and huge ones
  // don't force a scroll.
  const csW = Math.floor((FIELD_MAX_W - cellSpace) / cols) - cellSpace;
  const csH = Math.floor((FIELD_MAX_H - cellSpace) / rows) - cellSpace;
  const cellSize = Math.max(CELL_MIN, Math.min(CELL_MAX, csW, csH));

  const fieldW = cellSpace + cols * (cellSize + cellSpace);
  const fieldH = cellSpace + rows * (cellSize + cellSpace);

  // Backing store fits the field exactly (no bleed).
  canvas.width = fieldW;
  canvas.height = fieldH;

  // Mortar first (everything dead).
  ctx.fillStyle = FILL_DEAD;
  ctx.fillRect(0, 0, fieldW, fieldH);

  // Gutter block: fill entire field with grid line color and punch through
  // per-cell with mortar/alive.
  if (gridOn) {
    ctx.fillStyle = GRID_LINE;
    ctx.fillRect(0, 0, fieldW, fieldH);
  }

  for (let c = 0; c < cols; c++) {
    const towerH = profile[c];
    for (let r = 0; r < rows; r++) {
      const alive = (r === 0) || (r <= towerH);
      const x = cellSpace + c * (cellSize + cellSpace);
      const y = cellSpace + (rows - 1 - r) * (cellSize + cellSpace);
      ctx.fillStyle = alive ? FILL_ALIVE : FILL_DEAD;
      ctx.fillRect(x, y, cellSize, cellSize);
    }
  }

  view.cellSize = cellSize;
  view.cellSpace = cellSpace;
  view.offX = 0;
  view.offY = 0;
  view.rows = rows;
  view.cols = cols;
}

/**
 * Translate a mouse event to (col, row) in castle coordinates.
 * Accounts for the CSS scaling of the canvas (backing store is fixed
 * at CANVAS_W x CANVAS_H, but the canvas element is width:100%).
 */
function mousePosition(view, event) {
  const rect = view.canvas.getBoundingClientRect();
  const scaleX = view.canvas.width / rect.width;
  const scaleY = view.canvas.height / rect.height;
  const px = (event.clientX - rect.left) * scaleX - view.cellSpace;
  const py = (event.clientY - rect.top)  * scaleY - view.cellSpace;
  const stride = view.cellSize + view.cellSpace;
  const col = Math.floor(px / stride);
  const rowFromTop = Math.floor(py / stride);
  const row = view.rows - 1 - rowFromTop;
  if (col < 0 || col >= view.cols) return null;
  if (row < 0) return null;
  return [col, row];
}

// ------------------------------------------------------------------------
// Fact sheet rendering (grid of key-value chips, not a table anymore)
// ------------------------------------------------------------------------

function boolCell(v) {
  return v ? '<span class="yes">yes</span>' : '<span class="no">no</span>';
}

function renderFacts(sheet, factsEl, asciiEl, statusEl) {
  if (sheet.error) {
    factsEl.innerHTML =
      `<div class="fact-line"><span class="k">status</span> <span class="v flag-invalid">${sheet.error}</span></div>`;
    if (asciiEl) asciiEl.textContent = "";
    if (statusEl) { statusEl.textContent = "[ error: " + sheet.error + " ]"; statusEl.className = "status err"; }
    return;
  }
  const idx = sheet.canonical_index === null || sheet.canonical_index === undefined
    ? "&mdash;"
    : sheet.canonical_index;

  const statusV = sheet.valid
    ? `<span class="v yes">valid</span>`
    : `<span class="v flag-invalid">invalid :: odd blocks</span>`;

  const shortFacts = [
    [ "status",       statusV ],
    [ "size",         `<span class="v">${sheet.width} &times; ${sheet.height}</span>` ],
    [ "blocks",       `<span class="v">${sheet.blocks}</span>` ],
    [ "degree",       `<span class="v">${sheet.degree}</span>` ],
    [ "valleys",      `<span class="v">${sheet.valleys}</span>` ],
    [ "symmetric",    `<span class="v">${boolCell(sheet.features && sheet.features.symmetric)}</span>` ],
    [ "convex",       `<span class="v">${boolCell(sheet.features && sheet.features.convex)}</span>` ],
    [ "concave",      `<span class="v">${boolCell(sheet.features && sheet.features.concave)}</span>` ],
    [ "nickname",     `<span class="v">${sheet.nickname}</span>` ],
    [ "# in (w,h)",   `<span class="v">${sheet.count}</span>` ],
    [ "canonical idx",`<span class="v">${idx}</span>` ],
  ];

  const shortHtml = shortFacts
    .map(([k, v]) => `<span class="fact-line"><span class="k">${k}</span> ${v}</span>`)
    .join('<span class="sep-dot">::</span>');

  factsEl.innerHTML = `
    <div class="fact-inline">${shortHtml}</div>
    <div class="fact-urd">
      <span class="k">urd</span>
      <code class="urd-code">${sheet.urd}</code>
    </div>
  `;

  if (asciiEl) asciiEl.textContent = sheet.ascii || "";
  if (statusEl) {
    statusEl.className = "status";
    statusEl.textContent = `[ ok :: ${sheet.width} x ${sheet.height} :: ${sheet.blocks} blocks :: ${sheet.nickname} ]`;
  }
}

// ------------------------------------------------------------------------
// Tabs
// ------------------------------------------------------------------------

function initTabs() {
  const buttons = document.querySelectorAll(".tabs button.tab");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      document.querySelectorAll(".tab-panel").forEach((t) => t.classList.remove("active"));
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
    });
  });
}

// ------------------------------------------------------------------------
// Slider + numeric input pairs (both drive the same value)
// ------------------------------------------------------------------------

function initDim(sliderId, numId, max, onChange) {
  const slider = document.getElementById(sliderId);
  const num = document.getElementById(numId);
  const setBoth = (v) => {
    v = helpers.clamp(parseInt(v, 10) || 1, 1, max);
    slider.value = v;
    num.value = v;
    return v;
  };
  // While dragging: mirror slider position into the number box but do NOT
  // trigger a re-render. Only commit on 'change' (mouseup / touchend / kb).
  slider.addEventListener("input", () => { num.value = slider.value; });
  slider.addEventListener("change", () => onChange(setBoth(slider.value)));
  // Number box: commit on blur or Enter; ignore keystrokes in between so
  // typing "12" doesn't fire twice for '1' then '12'.
  num.addEventListener("blur", () => onChange(setBoth(num.value)));
  num.addEventListener("keydown", (e) => {
    if (e.key === "Enter") { onChange(setBoth(num.value)); num.blur(); }
  });
  return () => helpers.clamp(parseInt(num.value, 10) || 1, 1, max);
}

// ------------------------------------------------------------------------
// Designer
// ------------------------------------------------------------------------

let designerDims = { w: () => 9, h: () => 5 };

function refreshDesigner() {
  const view = state.designer;
  const w = designerDims.w();
  const h = designerDims.h();

  // Resize profile to match w (pad with 0, or truncate).
  while (view.profile.length < w) view.profile.push(0);
  view.profile.length = w;
  // Clamp tower heights DOWN to h-1 only. This lets the user shrink the
  // castle without losing information: previously-tall towers survive as
  // stored heights, but the visible ceiling is h, so the render caps them.
  // (Actually we do want to enforce h-1 hard so counts / fact sheet reflect
  //  the visible castle; use displayProfile below for rendering only.)
  const display = view.profile.map((v) => helpers.clamp(v, 0, h - 1));
  view.profile = display;
  // Force the visible canvas rows to at least h+1 so the user can always
  // see (and click into) the "airspace" above the tallest tower.
  view.heightCap = h + 1;

  drawField(view);
  const sheet = C.factSheet(view.profile);
  renderFacts(
    sheet,
    document.getElementById("designer-facts"),
    view.asciiOn ? document.getElementById("designer-ascii") : null,
    document.getElementById("designer-status"),
  );
  document.getElementById("designer-ascii-panel").classList.toggle("hidden", !view.asciiOn);
}

function designerGenerate(kind) {
  const view = state.designer;
  const w = designerDims.w();
  const h = designerDims.h();
  const statusEl = document.getElementById("designer-status");
  try {
    let profile;
    if (kind === "clear") {
      profile = new Array(w).fill(0);
    } else if (kind === "symmetric") {
      profile = C.randomFiltered(w, h, { ...checkedFeatures(), symmetric: true });
    } else if (kind === "random") {
      profile = C.randomFiltered(w, h, checkedFeatures());
    } else if (kind === "tallest") {
      profile = C.tallest(w, h);
    } else if (kind === "widest") {
      profile = C.widest(w, h);
    } else {
      return;
    }
    view.profile = profile.slice();
    refreshDesigner();
  } catch (err) {
    statusEl.className = "status err";
    statusEl.textContent = "[ error :: " + err.message + " ]";
  }
}

function checkedFeatures() {
  const out = {};
  document.querySelectorAll("[data-feature]").forEach((cb) => {
    if (cb.checked) out[cb.dataset.feature] = true;
  });
  return out;
}

function initDesignerCanvas() {
  const view = state.designer;
  view.canvas = document.getElementById("designer-canvas");
  view.ctx = view.canvas.getContext("2d");

  helpers.registerEvent(view.canvas, "mousedown", (e) => {
    const pos = mousePosition(view, e);
    if (!pos) return;
    const [col, row] = pos;
    const cur = view.profile[col];
    if (row <= cur) {
      // click inside/on top of a tower -> lower it to (row - 1)
      view.profile[col] = row === 0 && cur === 0 ? 0 : row - 1;
      view.dragMode = -1;
    } else {
      // click above -> raise it to (row), clamped to max allowed
      const h = designerDims.h();
      view.profile[col] = Math.min(row, h - 1);
      view.dragMode = +1;
    }
    view.mouseDown = true;
    view.lastX = col; view.lastY = row;
    refreshDesigner();
  }, false);

  helpers.registerEvent(view.canvas, "mousemove", (e) => {
    if (!view.mouseDown) return;
    const pos = mousePosition(view, e);
    if (!pos) return;
    const [col, row] = pos;
    if (col === view.lastX && row === view.lastY) return;
    view.lastX = col; view.lastY = row;
    const h = designerDims.h();
    if (view.dragMode > 0) {
      view.profile[col] = Math.max(view.profile[col], Math.min(row, h - 1));
    } else {
      view.profile[col] = Math.min(view.profile[col], Math.max(0, row - 1));
    }
    refreshDesigner();
  }, false);

  helpers.registerEvent(document, "mouseup", () => { view.mouseDown = false; }, false);
}

// ------------------------------------------------------------------------
// Inspector
// ------------------------------------------------------------------------

function initInspector() {
  const view = state.inspector;
  view.canvas = document.getElementById("inspector-canvas");
  view.ctx = view.canvas.getContext("2d");
  renderInspector();

  const run = () => {
    const raw = document.getElementById("urd").value.trim();
    const statusEl = document.getElementById("inspector-status");
    if (!raw) {
      statusEl.textContent = "[ awaiting input ]";
      statusEl.className = "status";
      return;
    }
    try {
      view.profile = C.parseUrd(raw);
      renderInspector();
    } catch (err) {
      statusEl.className = "status err";
      statusEl.textContent = "[ parse error :: " + err.message + " ]";
    }
  };
  document.getElementById("inspect-btn").addEventListener("click", run);
  document.getElementById("urd").addEventListener("keydown", (e) => {
    if (e.key === "Enter") run();
  });
}

function renderInspector() {
  const view = state.inspector;
  drawField(view);
  const sheet = C.factSheet(view.profile);
  renderFacts(
    sheet,
    document.getElementById("inspector-facts"),
    view.asciiOn ? document.getElementById("inspector-ascii") : null,
    document.getElementById("inspector-status"),
  );
  document.getElementById("inspector-ascii-panel").classList.toggle("hidden", !view.asciiOn);
}

// ------------------------------------------------------------------------
// Zoo
// ------------------------------------------------------------------------

function initZoo() {
  const container = document.getElementById("zoo-grid");
  container.innerHTML = "";
  C.ZOO.forEach((spec, idx) => {
    const sheet = C.factSheet(spec.profile);
    const card = document.createElement("div");
    card.className = "zoo-card";
    card.innerHTML = `
      <h3>${spec.name}</h3>
      <p>${spec.description}</p>
      <div class="zoo-canvas-wrap"><canvas id="zoo-canvas-${idx}"></canvas></div>
      <div class="zoo-urd">// ${sheet.urd}</div>
    `;
    card.addEventListener("click", () => {
      document.querySelector('[data-tab="inspector"]').click();
      document.getElementById("urd").value = sheet.urd;
      state.inspector.profile = spec.profile.slice();
      renderInspector();
    });
    container.appendChild(card);

    const miniCanvas = card.querySelector("canvas");
    const miniView = {
      profile: spec.profile,
      ctx: miniCanvas.getContext("2d"),
      canvas: miniCanvas,
      gridOn: true,
    };
    drawField(miniView);
  });
}

// ------------------------------------------------------------------------
// Keyboard shortcuts (G grid, A ascii; no C/colors anymore)
// ------------------------------------------------------------------------

function initKeyboard() {
  helpers.registerEvent(document.body, "keyup", (event) => {
    const tag = (event.target && event.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    if (event.keyCode === 71) {          // G
      state.designer.gridOn = !state.designer.gridOn;
      state.inspector.gridOn = state.designer.gridOn;
      refreshDesigner(); renderInspector();
    } else if (event.keyCode === 65) {   // A
      state.designer.asciiOn = !state.designer.asciiOn;
      state.inspector.asciiOn = state.designer.asciiOn;
      refreshDesigner(); renderInspector();
    }
  }, false);
}

// ------------------------------------------------------------------------
// Buttons
// ------------------------------------------------------------------------

function initButtons() {
  document.querySelectorAll("[data-gen]").forEach((btn) => {
    btn.addEventListener("click", () => designerGenerate(btn.dataset.gen));
  });
  document.getElementById("buttonGrid").addEventListener("click", () => {
    state.designer.gridOn = !state.designer.gridOn;
    state.inspector.gridOn = state.designer.gridOn;
    refreshDesigner(); renderInspector();
  });
  document.getElementById("buttonAscii").addEventListener("click", () => {
    state.designer.asciiOn = !state.designer.asciiOn;
    state.inspector.asciiOn = state.designer.asciiOn;
    refreshDesigner(); renderInspector();
  });
}

// ------------------------------------------------------------------------
// Init
// ------------------------------------------------------------------------

initTabs();
designerDims.w = initDim("w-slider", "w-num", 200, () => refreshDesigner());
designerDims.h = initDim("h-slider", "h-num", 100, () => refreshDesigner());
initDesignerCanvas();
initButtons();
refreshDesigner();
initInspector();
initZoo();
initKeyboard();
