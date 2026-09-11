// Castle Foundry frontend.  Loads Pyodide, installs the castles wheel, runs the
// bridge, and wires up the Designer / Inspector / Zoo views.

// Where the built wheel lives, relative to this page.  Build it with
//     python -m pip wheel . --no-deps -w dist/
const CASTLES_WHEEL = "../dist/castles-0.0.0-py3-none-any.whl";

let pyodide = null;
const py = {}; // bridge functions, populated once Pyodide is ready

const status = document.getElementById("status");

async function boot() {
  try {
    status.textContent = "Loading Pyodide…";
    pyodide = await loadPyodide();

    status.textContent = "Installing the castles wheel…";
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install(new URL(CASTLES_WHEEL, location.href).href);

    status.textContent = "Loading the bridge…";
    const bridgeSource = await (await fetch("bridge.py")).text();
    await pyodide.runPython(bridgeSource);
    py.inspect = pyodide.globals.get("inspect");
    py.random = pyodide.globals.get("random_castle");
    py.preset = pyodide.globals.get("preset");
    py.profile = pyodide.globals.get("profile");
    py.zoo = pyodide.globals.get("zoo");

    status.textContent = "Ready.";
    initUI();
  } catch (err) {
    status.textContent = "Failed to load: " + err;
    console.error(err);
  }
}

// --- helpers -------------------------------------------------------------

function parseSheet(jsonStr) {
  return JSON.parse(jsonStr);
}

function renderSVG(svg, el) {
  el.innerHTML = svg || "";
}

function renderFacts(sheet, el) {
  const rows = [];
  if (sheet.error) {
    rows.push(`<tr><td colspan="2" class="flag-invalid">${sheet.error}</td></tr>`);
  } else {
    const flag = sheet.valid ? "" : `<tr><td>status</td><td class="flag-invalid">odd block count (not a valid castle)</td></tr>`;
    const index = sheet.canonical_index === null ? "—" : sheet.canonical_index;
    rows.push(
      flag,
      `<tr><td>URD</td><td><code>${sheet.urd}</code></td></tr>`,
      `<tr><td>size</td><td>${sheet.width} × ${sheet.height}</td></tr>`,
      `<tr><td>blocks</td><td>${sheet.blocks}</td></tr>`,
      `<tr><td>nickname</td><td>${sheet.nickname}</td></tr>`,
      `<tr><td>degree</td><td>${sheet.degree}</td></tr>`,
      `<tr><td>valleys</td><td>${sheet.valleys}</td></tr>`,
      `<tr><td>#castles(w,h)</td><td>${sheet.count}</td></tr>`,
      `<tr><td>index</td><td>${index}</td></tr>`,
    );
  }
  el.innerHTML = `<table>${rows.join("")}</table>`;
}

function show(sheet, svgEl, factsEl) {
  renderSVG(sheet.svg, svgEl);
  renderFacts(sheet, factsEl);
}

// --- tabs -----------------------------------------------------------------

function initTabs() {
  const buttons = document.querySelectorAll("#tabs button");
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
    });
  });
}

// --- designer --------------------------------------------------------------

const designer = {
  profile: [1, 2, 3, 2, 1], // tower heights, one per column (the Pyramid)
};

function designerDims() {
  return {
    w: Math.max(1, Math.min(12, parseInt(document.getElementById("w").value, 10) || 1)),
    h: Math.max(1, Math.min(12, parseInt(document.getElementById("h").value, 10) || 1)),
  };
}

function renderGrid() {
  const { w, h } = designerDims();
  if (designer.profile.length < w) {
    for (let i = designer.profile.length; i < w; i++) designer.profile.push(0);
  }
  designer.profile.length = w;

  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  for (let level = h - 1; level >= 1; level--) {
    const row = document.createElement("div");
    row.className = "row";
    for (let c = 0; c < w; c++) {
      const cell = document.createElement("button");
      cell.className = "cell" + (designer.profile[c] >= level ? " filled" : "");
      cell.addEventListener("click", () => {
        designer.profile[c] = designer.profile[c] === level ? level - 1 : level;
        refreshDesigner();
      });
      row.appendChild(cell);
    }
    grid.appendChild(row);
  }
  // base row
  const base = document.createElement("div");
  base.className = "row";
  for (let c = 0; c < w; c++) {
    const cell = document.createElement("button");
    cell.className = "cell base filled";
    cell.addEventListener("click", () => {
      designer.profile[c] = 0;
      refreshDesigner();
    });
    base.appendChild(cell);
  }
  grid.appendChild(base);
}

function refreshDesigner() {
  renderGrid();
  const sheet = parseSheet(py.profile(JSON.stringify(designer.profile)));
  show(sheet, document.getElementById("designer-svg"), document.getElementById("designer-facts"));
}

function designerGenerate(kind) {
  const { w, h } = designerDims();
  let sheet;
  if (kind === "random" || kind === "symmetric") {
    const features = checkedFeatures();
    if (kind === "symmetric") features.symmetric = true;
    sheet = parseSheet(py.random(w, h, JSON.stringify(features)));
  } else {
    sheet = parseSheet(py.preset(w, h, kind));
  }
  if (!sheet.error && sheet.profile) {
    syncProfileFromSheet(sheet);
  }
  show(sheet, document.getElementById("designer-svg"), document.getElementById("designer-facts"));
}

function syncProfileFromSheet(sheet) {
  // Rebuild the designer's grid heights from a generated castle's profile.
  designer.profile = sheet.profile.slice();
  renderGrid();
}

function checkedFeatures() {
  const out = {};
  document.querySelectorAll("[data-feature]").forEach((cb) => {
    if (cb.checked) out[cb.dataset.feature] = true;
  });
  return out;
}

// --- inspector --------------------------------------------------------------

function initInspector() {
  const run = () => {
    const sheet = parseSheet(py.inspect(document.getElementById("urd").value.trim()));
    show(sheet, document.getElementById("inspector-svg"), document.getElementById("inspector-facts"));
  };
  document.getElementById("inspect-btn").addEventListener("click", run);
  document.getElementById("urd").addEventListener("keydown", (e) => {
    if (e.key === "Enter") run();
  });
}

// --- zoo -------------------------------------------------------------------

function initZoo() {
  const specs = parseSheet(py.zoo());
  const container = document.getElementById("zoo-grid");
  container.innerHTML = "";
  specs.forEach((spec) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `<h3>${spec.name}</h3><p>${spec.description}</p><div class="svg-wrap">${spec.svg}</div>`;
    card.addEventListener("click", () => {
      document.querySelector('[data-tab="inspector"]').click();
      document.getElementById("urd").value = spec.urd;
      const sheet = parseSheet(py.inspect(spec.urd));
      show(sheet, document.getElementById("inspector-svg"), document.getElementById("inspector-facts"));
    });
    container.appendChild(card);
  });
}

// --- wire-up ---------------------------------------------------------------

function initUI() {
  initTabs();
  renderGrid();
  refreshDesigner();

  document.querySelectorAll("[data-gen]").forEach((btn) => {
    btn.addEventListener("click", () => designerGenerate(btn.dataset.gen));
  });

  initInspector();
  initZoo();
}

boot();
