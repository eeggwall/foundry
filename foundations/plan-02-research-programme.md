# Plan 02: A Research Programme Beyond Euler 502

Status: proposed programme; projects and results below are not claimed to be complete.

Lead: Enumeration (E), with Representations (R), Numbers (N), and Zoo (Z).

## Purpose

Turn the work on Project Euler 502 into a sustained programme of mathematical investigation. The original problem is a productive starting point, not the permanent boundary of the Center's interests. Castle Foundry becomes one research instrument among several, rather than the place where every future experiment must be implemented.

The programme should produce definitions, proofs, counterexamples, algorithms, sequences, software, and teaching material. Its success is measured by useful, checkable work, not the number of proposed divisions or repositories.

Use the conventions and evidence model in [Plan 01](plan-01-taxonomy-atlas.md). Programmes below are research directions, not software package boundaries. The existing R/E/N/Z divisions remain the starting institutional structure.

## Source Dossier

Begin with a curated reading dossier, preserving the distinction between a historical approach, a current mathematical claim, and the behavior of an implementation.

| Source | Role in the programme |
| --- | --- |
| [Euler 502 overview](https://charlesreid1.com/wiki/Project_Euler/502) | Problem statement, published checkpoints, and entry to the source collection |
| [Problem Setup](https://charlesreid1.com/wiki/Project_Euler/502/Problem_Setup) | Research history from 2017 to 2026 and the transition away from direct enumeration |
| [Representations](https://charlesreid1.com/wiki/Project_Euler/502/Representations) | Binary, height, and URD viewpoints; convex-castle attempts; generalized Dyck grammar |
| [Observations](https://charlesreid1.com/wiki/Project_Euler/502/Observations) | Independence, parity, and lessons from the investigation |
| [Solution](https://charlesreid1.com/wiki/Project_Euler/502/Solution) | Signed counts, rational generating functions, and distinct large-parameter regimes |
| [Implementation Notes](https://charlesreid1.com/wiki/Project_Euler/502/Implementation_Notes) | Java algorithm dispatch, coefficient extraction, and numerical assumptions |
| [Brute Force](https://charlesreid1.com/wiki/Project_Euler/502/Brute_Force) | Independent column-height reasoning and small-case computational checks |

Local foundations include `castles/`, `notes/`, `tests/`, and the browser-side JavaScript port in `webapp/castles.js`. Treat these paths as an inventory of the current repository, not portable dependencies of the future Atlas.

For each imported result, capture the source revision or retrieval date, notation, hypotheses, and supporting derivation. Follow the cited polyomino literature in a separate reading phase; a paper title in the wiki is a lead, not proof of an equivalence with castle objects.

Preserve the unsuccessful approaches. An approach that failed to count every Euler-valid castle might still generate a family, expose a useful invariant, or furnish a good teaching example.

## Shared Mathematical Spine

Use these symbols consistently unless a report explicitly translates another source's notation:

- `A(w,h)`: geometric castles of width `w` and exact height `h`, without parity restriction.
- `F(w,h)`: the even-block subset of `A(w,h)`.
- `T(k,L)`: towers of height at most `k` above a supporting block of length `L`, excluding that block.
- `P(k,L)`: the signed sum over those towers, weighting each tower by `(-1)^b` for its block count `b`.

For positive `w,h`, the unrestricted geometric count is `A(w,h) = h^w - (h-1)^w`. For nonnegative `k`, `T(k,L) = (k+1)^L` follows from the column-height interpretation or the independent sub-block decomposition.

For `h >= 2`, the central parity formula is:

```text
F(w,h) = (h^w - (h-1)^w - P(h-1,w) + P(h-2,w)) / 2
```

Handle `h = 1` separately: a base-only castle has one block, so `F(w,1) = 0`. Do not introduce an undefined negative-height `P` merely to apply the displayed formula at a boundary.

This provides the shared route through the programme:

```text
geometry -> encodings -> decomposition -> generating functions
         -> recurrences -> efficient computation -> new questions
```

## Project Portfolio

### R-01: Comparative Representations

Question: which encodings are genuinely equivalent, on which domains, and what information is lost by simplification?

Compare absolute heights, above-base profiles, URD words, column masks, and coordinate-labeled containment trees. Investigate the relation to Dyck-style grammars without casually identifying these words with ordinary Dyck words. Separate geometric tree encodings from abstract rooted tree shapes.

First experiment: round-trip a curated set of valid geometric specimens, including odd-block objects, and collect malformed encodings that each parser should reject. Draw the same specimen in each representation.

First artifact: a representation atlas with conversion diagrams, explicit domain restrictions, and small proof obligations. Progress means each claimed equivalence has an inverse argument; round-trip tests alone do not establish a general bijection.

### E-01: Signed Enumeration

Question: how do the grammar and column-height viewpoints independently recover the same parity count?

Develop a parallel derivation of the signed grammar generating function and the last-column-height dynamic programme. Explain why the base reverses the parity being selected, and why subtraction of adjacent height bounds imposes exact height.

First experiment: compare full enumeration, grammar counts, and height-state counts on a small, explicitly bounded grid. Check both parities, not just their even subset.

First artifact: a technical report whose derivations can be followed without reading the solver. Progress means disagreements lead to a documented counterexample or correction rather than a patched table of expected answers.

### E/N-02: Extreme Dimensions

Question: why does enormous width favor one recurrence direction while enormous height favors another?

Reproduce the rational-function and coefficient-extraction routes documented for the Java solver. Compare direct series extraction with Kitamasa, then study recurrence discovery in the height direction. Distinguish algorithmic regimes from implementation-specific crossover constants.

First experiment: reproduce the published moderate-size checkpoints before attempting the three extreme Euler inputs. Record runtime, peak memory when measurable, arithmetic domain, and algorithm selection on the actual machine used.

First artifact: an instrument report and regime map. Include the cost of generating recurrence data, not only the final jump to a distant index.

Berlekamp-Massey identifies a recurrence consistent with supplied terms over a field. A finite fit and a held-out check are evidence, not a general proof. Investigate structural recurrence bounds or another certification argument before labeling distant extrapolation mathematically established. Record prime-modulus assumptions and exceptional cases explicitly.

### N-01: Sequence Observatory

Question: which sequences and arithmetic patterns appear when dimensions, parity, or structural properties are fixed?

Survey rows, columns, diagonals, block distributions, symmetry counts, and selected family counts. Investigate oscillation in signed counts, divisibility patterns, and possible asymptotic behavior. Treat numerical matches to known sequences as leads requiring definition-level comparison.

First experiment: produce a small exact table with parameter order, offsets, counted domain, and reproduction command. Cross-check a subset by a genuinely different method.

First artifact: a sequence register with sourced OEIS correspondences where verified and clearly marked candidate correspondences elsewhere. No submission to an external sequence database is implied by this plan.

### Z-01: Comparative Morphology

Question: which shape properties lead to useful classifications and tractable enumeration?

Investigate unimodality, monotonicity, rectangles, strict versus plateau valleys, root degree, and reflection symmetry. Keep a family predicate separate from a specimen nickname. Distinguish counting reflection-fixed objects from counting objects modulo reflection.

First experiment: use minimal specimens to expose overlaps and differences among predicates. For unimodal skylines, investigate the row-run argument that the block count equals the height; scope any resulting counting formula to the correct parity domain.

First artifact: a field guide with membership tests, counterexamples, and initial family counts. Later work can use Burnside's lemma for reflection classes, after defining the action and the counted set.

### E/Z-02: Sampling And Addresses

Question: can specimens be sampled uniformly and assigned reversible addresses without listing the entire size class?

Investigate completion-count dynamic programming, ranking/unranking, exact-height conditioning, and later conditioning on block count or other features. Specify the sample space before discussing uniformity. Uniformity over oriented castles is not uniformity over reflection classes.

First experiment: compare rank/unrank round trips on tiny exhaustive classes and test a sampler against exact probabilities. State which rejection steps remain and their acceptance rates.

First artifact: an algorithm note and reference implementation. A frequency plot is a diagnostic, not proof of uniformity; supply the probability argument separately. Preserve Atlas accession IDs rather than replacing them with implementation-dependent ranks.

### E/R-03: Beyond Parity

Question: what becomes visible when block count is retained as a variable rather than collapsed to a sign?

Introduce a block marker `q` and study block-count polynomials or generating functions. Evaluations at `q = 1` and `q = -1` recover unsigned and signed information under stated base conventions. Explore moments, exact-block counts, area refinements, and residue classes beyond parity.

First experiment: compare small block-count polynomials from enumeration and a weighted recurrence. Check that coefficient sums and alternating sums match independent counts.

First artifact: a working note defining the weighted model and separating derived formulas from proposed extensions. Root-of-unity filters are a prospective tool, not a reason to omit coefficient-domain assumptions.

### R/E-04: Altered Rules

Question: which results survive when one castle rule changes?

Candidate variations include larger mandatory gaps, bounded block lengths, colored blocks, changed boundary conditions, and relaxed support. Change one rule at a time. In particular, allowing overhangs may destroy the skyline representation and sibling independence; it is a new model, not a toggle on the existing proofs.

First experiment: define one variant, enumerate tiny cases directly, and identify the first place where an existing decomposition succeeds or fails.

First artifact: a variant dossier with a rule comparison, minimal examples, and a list of retained and broken arguments. Connections to bargraphs, polyominoes, automata, or statistical mechanics should be investigated through explicit definitions rather than analogy alone.

## Research Conduct

- Give each active project a one-page charter: question, sources, known results, unknowns, first experiment, expected artifact, and stopping rule.
- Preserve exact arithmetic for reference calculations; record modular arithmetic separately. Browser floating-point output is not an oracle for large integers.
- Record software revision, environment, inputs, seed when applicable, and resource limits with each computational result.
- Begin expensive calculations with a bounded pilot. Do not describe an exponential enumeration as practical merely because both dimensions look small.
- Use independent derivations when possible; agreement between direct ports can preserve the same error.
- Search for counterexamples before broadening a conjecture. Store failed conjectures and unsuccessful methods with their limitations.
- Attribute original notes and external work accurately. A fictional faculty name does not replace source credit.

## First Research Cycle

### A. Reconciliation

Build the source dossier and a short discrepancies register. Settle enough notation to run a small common experiment. Leave unresolved terminology explicitly unresolved rather than delaying all research for a perfect ontology.

### B. Two Active Projects

Start E-01 and a narrow Z-01 investigation into unimodality and block parity. Use R-01 only as supporting work where conversions need clarification. These projects are close to the existing tools and can supply a complete first publication cycle without a new computing platform.

### C. Publication And Review

Produce an Atlas update, a reproducible small-case experiment, a working note or report, and seminar material. The publication process will be specified in Plan 04. Use objections raised in review to revise definitions and tests.

### D. Next Allocation

Select the next project based on what the cycle exposed. Performance limits may justify E/N-02; classification ambiguity may justify deeper Z-01 work. Keep the rest of the portfolio dormant with explicit next actions, not nominally active.

## Completion Criteria

- The source dossier preserves both the successful solution and the history of attempts.
- Every portfolio project has a concrete first question and artifact, not just a topic name.
- The first cycle produces a connected definition, experiment, and explanatory document.
- Claimed proofs, computational observations, and speculative directions are distinguishable.
- At least one result is checked by independent reasoning or an independent implementation.
- Resource costs and unresolved discrepancies are recorded, including useful negative results.
- Further projects can move outside Foundry without taking their definitions or evidence out of circulation.

## Decision Gate

Review the first research cycle before allocating more active projects. Eggwall's institutional role will be developed in Plan 03; reports and seminars in Plan 04; software and repository independence in Plan 05. None of those plans requires all eight research directions to start at once.
