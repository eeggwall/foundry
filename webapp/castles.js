// castles.js — a JavaScript port of the core `castles` library.
//
// Replaces the Pyodide bridge: the whole app runs natively in the browser, no
// WASM download, no JS<->Python hops.  Behaviour matches castles/*.py exactly
// for the range the app uses (w, h <= 12).

// ---- geometry -------------------------------------------------------------

export function blockCount(profile) {
  // base block (1) + one block per maximal run at each tower level.
  const height = 1 + Math.max(...profile, 0);
  let count = 1;
  for (let level = 1; level < height; level++) {
    let inRun = false;
    for (const col of profile) {
      if (col >= level) {
        if (!inRun) { count += 1; inRun = true; }
      } else {
        inRun = false;
      }
    }
  }
  return count;
}

export const isEvenBlocks = (profile) => blockCount(profile) % 2 === 0;

// ---- URD strings ----------------------------------------------------------

export function towerWord(profile) {
  let out = "";
  let prev = 0;
  for (const h of profile) {
    out += h >= prev ? "U".repeat(h - prev) : "D".repeat(prev - h);
    out += "R";
    prev = h;
  }
  out += "D".repeat(prev);
  return out;
}

export const toUrd = (profile) => "U" + towerWord(profile) + "D";

function isTower(word) {
  // Recursive-descent recogniser for the E_k grammar.
  function rec(w, k) {
    if (!w) return true;                    // E_k -> empty
    if (w[0] === "R") return rec(w.slice(1), k);  // E_k -> R E_k
    if (w[0] === "U" && k > 0) {            // E_k -> U V D (empty | R E_k)
      for (let j = 2; j <= w.length; j++) {
        if (rec(w.slice(1, j), k - 1) && j < w.length && w[j] === "D") {
          const tail = w.slice(j + 1);
          if (tail === "") return true;
          if (tail[0] === "R" && rec(tail.slice(1), k)) return true;
        }
      }
      return false;
    }
    return false;
  }
  return rec(word, word.length);
}

export function parseUrd(s) {
  if (typeof s !== "string" || s.length < 2 || s[0] !== "U" || s[s.length - 1] !== "D") {
    throw new Error("a castle string must be 'U' (tower) 'D'");
  }
  const tower = s.slice(1, -1);
  if (!isTower(tower)) throw new Error("invalid tower word");
  const profile = [];
  let height = 0;
  for (const ch of tower) {
    if (ch === "U") height += 1;
    else if (ch === "D") height -= 1;
    else if (ch === "R") profile.push(height);
    else throw new Error(`invalid character ${JSON.stringify(ch)}`);
  }
  if (profile.length === 0) throw new Error("castle must be at least 1 column wide");
  return profile;
}

// ---- features -------------------------------------------------------------

export function isSymmetric(profile) {
  for (let i = 0, j = profile.length - 1; i < j; i += 1, j -= 1) {
    if (profile[i] !== profile[j]) return false;
  }
  return true;
}

export function isConvex(profile) {
  let i = 0;
  while (i + 1 < profile.length && profile[i] <= profile[i + 1]) i += 1;
  while (i + 1 < profile.length && profile[i] >= profile[i + 1]) i += 1;
  return i === profile.length - 1;
}

export function numValleys(profile) {
  let v = 0;
  for (let c = 1; c < profile.length - 1; c += 1) {
    if (profile[c - 1] > profile[c] && profile[c] < profile[c + 1]) v += 1;
  }
  return v;
}

export function isConcave(profile) {
  if (numValleys(profile) === 0) return false;
  let i = 0;
  while (i + 1 < profile.length && profile[i] >= profile[i + 1]) i += 1;
  while (i + 1 < profile.length && profile[i] <= profile[i + 1]) i += 1;
  return i === profile.length - 1;
}

export function degree(profile) {
  let runs = 0;
  let inRun = false;
  for (const h of profile) {
    if (h >= 1) {
      if (!inRun) { runs += 1; inRun = true; }
    } else {
      inRun = false;
    }
  }
  return runs;
}

export function nickname(profile) {
  const parts = [];
  if (isSymmetric(profile)) parts.push("symmetric");
  if (isConvex(profile)) parts.push("convex");
  else if (isConcave(profile)) parts.push("concave");
  else parts.push("complex");
  const v = numValleys(profile);
  if (v > 0) parts.push(`${v}-valley`);
  return parts.join(" ");
}

// ---- counting (grammar DP) ------------------------------------------------

const towerMemo = new Map();

function towerCounts(k, w) {
  const key = `${k},${w}`;
  if (towerMemo.has(key)) return towerMemo.get(key);
  let result;
  if (k < 0) result = w === 0 ? [1, 0] : [0, 0];
  else if (w < 0) result = [0, 0];
  else if (w === 0) result = [1, 0];
  else {
    let even = towerCounts(k, w - 1)[0];
    let odd = towerCounts(k, w - 1)[1];
    for (let v = 1; v <= w; v += 1) {
      const [ve, vo] = towerCounts(k - 1, v);
      const [pe, po] = [vo, ve]; // the peak flips parity (+1 block)
      if (v === w) {
        even += pe; odd += po;
      } else {
        const [te, to] = towerCounts(k, w - v - 1);
        even += pe * te + po * to;
        odd += pe * to + po * te;
      }
    }
    result = [even, odd];
  }
  towerMemo.set(key, result);
  return result;
}

export function count(w, h) {
  if (w < 1 || h < 1) return 0;
  if (h === 1) return 0;
  return towerCounts(h - 1, w)[1] - towerCounts(h - 2, w)[1];
}

// ---- canonical index ------------------------------------------------------

const MAX_INDEX = 100000;

export function canonicalIndex(profile) {
  if (!isEvenBlocks(profile)) return null;
  const w = profile.length;
  const h = 1 + Math.max(...profile, 0);
  if (h ** w > MAX_INDEX) return null;
  const key = profile.join(",");
  const valid = [];
  const walk = (prefix) => {
    if (prefix.length === w) {
      if (Math.max(...prefix) === h - 1 && isEvenBlocks(prefix)) valid.push(prefix.join(","));
      return;
    }
    for (let x = 0; x < h; x += 1) walk(prefix.concat(x));
  };
  walk([]);
  return valid.indexOf(key);
}

// ---- rendering -------------------------------------------------------------

export function renderSVG(profile) {
  const w = profile.length;
  const h = 1 + Math.max(...profile, 0);
  const blocks = [[1, 1, w]]; // base block: [row, col0, col1]
  for (let level = 1; level < h; level += 1) {
    let start = null;
    for (let c = 0; c < w; c += 1) {
      if (profile[c] >= level) {
        if (start === null) start = c;
      } else if (start !== null) {
        blocks.push([level + 1, start + 1, c]);
        start = null;
      }
    }
    if (start !== null) blocks.push([level + 1, start + 1, w]);
  }
  const rects = blocks
    .map(([row, c0, c1]) => `<rect x="${c0 - 1}" y="${h - row}" width="${c1 - c0 + 1}" height="1"/>`)
    .join("\n");
  const CELL = 20;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w * CELL}" height="${h * CELL}">\n` +
    "<style>rect{fill:#4a6fa5;stroke:#2c3e50;stroke-width:0.04;}</style>\n" +
    `${rects}\n</svg>`
  );
}

export function renderAscii(profile) {
  const h = 1 + Math.max(...profile, 0);
  const lines = [];
  for (let row = h; row >= 1; row -= 1) {
    let line = "";
    for (let c = 0; c < profile.length; c += 1) {
      line += row <= profile[c] + 1 ? "#" : ".";
    }
    lines.push(line);
  }
  return lines.join("\n");
}

// ---- fact sheet -----------------------------------------------------------

export function factSheet(profile) {
  const w = profile.length;
  const h = 1 + Math.max(...profile, 0);
  return {
    urd: toUrd(profile),
    width: w,
    height: h,
    profile: profile.slice(),
    blocks: blockCount(profile),
    valid: isEvenBlocks(profile),
    degree: degree(profile),
    valleys: numValleys(profile),
    features: {
      symmetric: isSymmetric(profile),
      convex: isConvex(profile),
      concave: isConcave(profile),
      has_valley: numValleys(profile) > 0,
    },
    nickname: nickname(profile),
    count: count(w, h),
    canonical_index: canonicalIndex(profile),
    ascii: renderAscii(profile),
    svg: renderSVG(profile),
  };
}

// ---- generators -----------------------------------------------------------

export function randomCastle(w, h, rng = Math.random) {
  if (count(w, h) === 0) throw new Error(`no castles of width ${w} and height ${h}`);
  for (;;) {
    const profile = Array.from({ length: w }, () => Math.floor(rng() * h));
    if (Math.max(...profile) === h - 1 && isEvenBlocks(profile)) return profile;
  }
}

export function randomFiltered(w, h, features = {}, rng = Math.random) {
  for (let i = 0; i < 5000; i += 1) {
    const profile = randomCastle(w, h, rng);
    if (
      (!features.symmetric || isSymmetric(profile)) &&
      (!features.convex || isConvex(profile)) &&
      (!features.concave || isConcave(profile))
    ) {
      return profile;
    }
  }
  throw new Error("no castle matching the requested features");
}

export const tallest = (w, h) => [h - 1, ...Array(w - 1).fill(0)];
export const widest = (w, h) => Array(w).fill(h - 1);

// ---- zoo ------------------------------------------------------------------

export const ZOO = [
  { name: "The Fortress", description: "A solid rectangle of stacked blocks.", profile: [3, 3, 3, 3, 3] },
  { name: "The Pyramid", description: "A symmetric peak rising to a single column.", profile: [1, 2, 3, 2, 1] },
  { name: "Staircase", description: "A monotone climb from left to right.", profile: [0, 1, 2, 3] },
  { name: "The Terrace", description: "A stepped shelf descending to the right.", profile: [3, 2, 1, 0] },
  { name: "The Spire", description: "A single tall column.", profile: [3] },
  { name: "The Battlement", description: "A crenellated wall, neither convex nor concave.", profile: [1, 2, 1, 2, 1] },
  { name: "The Canyon", description: "A deep symmetric valley.", profile: [3, 2, 1, 2, 3] },
];
