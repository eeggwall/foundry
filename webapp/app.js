// Castle Foundry frontend — pure JS, no Pyodide.  Imports the ported library
// from castles.js and wires up the Designer / Inspector / Zoo views.

import * as C from "./castles.js";

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

// --- helpers -------------------------------------------------------------

function renderSVG(svg, el) {
  el.innerHTML = svg || "";
}

function renderFacts(sheet, el) {
  const rows = [];
  if (sheet.error) {
    rows.push(`<tr><td colspan="2" class="flag-invalid">${sheet.error}</td></tr>`);
  } else {
    const flag = sheet.valid
      ? ""
      : `<tr><td>status</td><td class="flag-invalid">odd block count (not a valid castle)</td></tr>`;
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

function showSheet(sheet, svgEl, factsEl) {
  renderSVG(sheet.svg, svgEl);
  renderFacts(sheet, factsEl);
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
  const sheet = C.factSheet(designer.profile);
  showSheet(sheet, document.getElementById("designer-svg"), document.getElementById("designer-facts"));
}

function designerGenerate(kind) {
  const { w, h } = designerDims();
  let sheet;
  try {
    let profile;
    if (kind === "random" || kind === "symmetric") {
      const features = checkedFeatures();
      if (kind === "symmetric") features.symmetric = true;
      profile = C.randomFiltered(w, h, features);
    } else if (kind === "tallest") {
      profile = C.tallest(w, h);
    } else {
      profile = C.widest(w, h);
    }
    sheet = C.factSheet(profile);
    designer.profile = profile.slice();
    renderGrid();
  } catch (err) {
    sheet = { error: err.message };
  }
  showSheet(sheet, document.getElementById("designer-svg"), document.getElementById("designer-facts"));
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
    const input = document.getElementById("urd").value.trim();
    let sheet;
    try {
      sheet = C.factSheet(C.parseUrd(input));
    } catch (err) {
      sheet = { error: err.message };
    }
    showSheet(sheet, document.getElementById("inspector-svg"), document.getElementById("inspector-facts"));
  };
  document.getElementById("inspect-btn").addEventListener("click", run);
  document.getElementById("urd").addEventListener("keydown", (e) => {
    if (e.key === "Enter") run();
  });
}

// --- zoo -------------------------------------------------------------------

function initZoo() {
  const container = document.getElementById("zoo-grid");
  container.innerHTML = "";
  C.ZOO.forEach((spec) => {
    const sheet = C.factSheet(spec.profile);
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML =
      `<h3>${spec.name}</h3><p>${spec.description}</p><div class="svg-wrap">${sheet.svg}</div>`;
    card.addEventListener("click", () => {
      document.querySelector('[data-tab="inspector"]').click();
      document.getElementById("urd").value = sheet.urd;
      showSheet(sheet, document.getElementById("inspector-svg"), document.getElementById("inspector-facts"));
    });
    container.appendChild(card);
  });
}

// --- wire-up ---------------------------------------------------------------

initTabs();
renderGrid();
refreshDesigner();
document.querySelectorAll("[data-gen]").forEach((btn) => {
  btn.addEventListener("click", () => designerGenerate(btn.dataset.gen));
});
initInspector();
initZoo();
