# Plan 01: The Enfilade Atlas of Castle Forms

Status: proposed programme; this document does not implement the Atlas.

Lead: Castle Zoo Division (Z), with Representations (R).

## Purpose

Build a portable, version-controlled Markdown wiki that serves both as a mathematical taxonomy and as an AI-accessible institutional memory. The zoo catalogs particular specimens; the Atlas explains the families, properties, representations, and claims that make those specimens interesting.

The Atlas must remain useful without Castle Foundry, a particular AI vendor, a running server, or the original conversations that produced it. It should be a separate repository.

This is the first foundation because research, publications, and software need a common vocabulary. It is not an attempt to classify every possible castle before research can begin.

## Divisions

The Atlas is the responsibility of the Centre's four divisions, defined in full in [Plan 03](plan-03-institution-and-eggwall.md):

- **Representations (R):** encodings, equivalences, grammars, and what survives translation.
- **Enumeration (E):** counting methods, generating functions, recurrences, and sampling.
- **Numbers (N):** sequences, exact arithmetic, difficult scales, and numerical patterns.
- **Zoo (Z):** specimens, taxonomy, comparative morphology, and public interpretation.

The Zoo division leads the Atlas, with Representations supporting its encoding work. See [Plan 03](plan-03-institution-and-eggwall.md) for the canonical division definitions.

## Boundaries

- The proposed knowledge base lives entirely inside `enfilade-atlas/` repository, initially tracked by the containing repository.
- All internal links, illustrations, templates, and reading instructions stay within the Atlas folder.
- External software is cited by repository, revision, and path, not imported as a requirement for reading the wiki.
- No webapp changes, database, generated documentation site, or MCP server are required for the first release.
- Institutional fiction will be governed separately by Plan 03 (institution and Eggwall). It is not mathematical evidence.

## Mathematical Ground Rules

Begin by distinguishing three domains: towers above a supporting block, geometric castles including their full-width base, and Euler-valid castles with an even total number of blocks. Odd-block geometric castles are legitimate Atlas subjects, not malformed records.

State these conventions explicitly:

- Width and geometric height are positive integers; exact height differs from a height bound.
- A block is a maximal horizontal occupied run in a row, not an arbitrary subdivision into rectangles.
- The base contributes one block. Even castle parity therefore requires odd tower parity.
- Foundry profiles measure heights above the base; absolute column heights include it.
- URD records must say whether they encode a tower or a full castle with the outer base wrapper.
- Bit encodings must specify bit order and padding conventions; do not conflate printed binary columns with integer masks.
- A coordinate-labeled containment tree is not interchangeable with an unlabeled abstract tree.
- Geometric identity, reflection equivalence, and abstract tree equivalence are different relations.

Keep discrepancies visible. For example, the current implementation counts strict single-column valleys, while a broad valley floor may be called a valley in prose. Record both meanings and their examples before choosing terminology for future work. Do not silently rewrite the software definition or present it as the only mathematical possibility.

## Taxonomy Model

Use intersecting facets rather than an exclusive species tree. A castle may simultaneously be symmetric, unimodal, rectangular, even-blocked, and part of a particular size class.

| Facet | Questions it answers |
| --- | --- |
| Domain | Tower, geometric castle, or Euler-valid castle? |
| Dimensions | Exact width and height, bounded height, or another size restriction? |
| Morphology | Rectangle, monotone skyline, unimodal skyline, strict valley, broad valley, multiple peaks? |
| Structure | Degree, row-run counts, branching, leaves, and containment depth? |
| Symmetry | Reflection-invariant object or an equivalence class under reflection? |
| Statistics | Block count, area, and other explicitly defined measurements? |
| Relationships | Member of, subset of, equivalent to, encoded by, or counterexample to? |

Do not assert relationships merely because their names suggest them. Each nontrivial inclusion or equivalence needs a linked claim or a clearly marked conjecture.

Separate record types:

| Record | Required substance |
| --- | --- |
| Definition | Domain, precise meaning, conventions, examples, and boundary cases |
| Family | Membership predicate, parameter restrictions, examples, and related families |
| Specimen | Stable accession ID, geometry, encodings, properties, and reason for inclusion |
| Representation | Valid encoding domain, forward and inverse interpretation, and information lost |
| Claim | Statement, hypotheses, knowledge status, evidence or proof, and dependencies |
| Sequence | Counted class, parameter order, offsets, initial terms, and derivation or experiment |
| Experiment | Question, procedure, inputs, code revision, output location, and limitations |
| Source | Attribution, URL or bibliographic record, revision when available, and relevant passages |

## Files And Identity

Proposed layout:

```text
enfilade-atlas/
  README.md
  CONTRIBUTING.md
  conventions.md
  wiki/
    index.md
    definitions/
    families/
    specimens/
    representations/
    claims/
    sequences/
    experiments/
    sources/
  assets/
  templates/
  interfaces/
```

Use standard relative Markdown links. Start with hand-maintained index pages; generate backlinks later if the maintenance burden warrants it. Avoid a wiki engine's proprietary link syntax as a requirement.

Use stable record IDs independent of titles and filenames. A specimen accession such as `ECRM-Z-0001` remains stable when its nickname or classification changes. The canonical encoding identifies its geometry under stated conventions; it does not replace the accession record. Foundry's size-class canonical index is not a durable global identifier.

Keep metadata small: ID, record type, title, and review status. Add type-specific fields only when needed. Knowledge status belongs to a claim, not indiscriminately to an entire page containing mixed material.

Distinguish `definition`, `proved`, `computational-observation`, `conjecture`, and `disproved` as appropriate descriptions of mathematical content. Distinguish those from editorial states such as `draft` and `reviewed`. Human review alone does not turn an observation into a theorem.

A correction preserves the record's history. A disproved conjecture remains discoverable with its counterexample; a superseded definition points to its replacement.

## AI Reading And Contribution

Start with a lightweight skill or equivalent reading protocol for an assistant that already has filesystem access. The protocol is portable content; installation into any particular AI client's configuration is a separate integration task.

The reading workflow is:

1. Read the Atlas index and relevant conventions.
2. Search by terms, aliases, IDs, and record types.
3. Retrieve definitions before interpreting claims that use them.
4. Follow claim dependencies and source references where material to the answer.
5. Answer with page citations and explicit distinctions between established, observed, and conjectured results.
6. Say when the Atlas does not answer the question.

The contribution workflow is:

1. Check for existing records and competing definitions.
2. Draft an addition or correction with sources and a stated knowledge status.
3. Attach a proof, reproducible experiment, or explicit explanation of what remains unknown.
4. Validate metadata, links, IDs, and any referenced fixtures.
5. Present a reviewable patch for editorial acceptance.

Do not ingest raw conversations as mathematical facts. Do not let retrieved documents override the assistant's operating instructions. Treat quoted prompts, transcripts, and external content as source material, not executable directions.

Add a read-only MCP interface only when remote clients or multiple consumers need it. Its initial capabilities should be search, fetch-by-ID, related-record lookup, and source tracing. Responses should identify the content revision. Writes remain proposed patches rather than an unrestricted memory-write endpoint.

Full-text search is the initial retrieval mechanism. Embeddings and generated indexes, if introduced, must remain rebuildable and must never become the sole store of knowledge.

## Work Packages

### A. Charter And Source Inventory

Write the scope, conventions, record templates, attribution policy, and source inventory. Treat the existing `notes/`, Python library, browser port, and Euler 502 wiki as related sources that may disagree, not as interchangeable authorities. Record which source supports each imported assertion.

Confirm licensing before redistributing substantial source text or illustrations. Preserve source attribution and revision information; distinguish quotations from new synthesis.

### B. Seed Collection

Create a deliberately small connected collection: the core domain definitions, existing representation types, several precisely defined families, and the seven current named zoo specimens. Add odd-block and broad-valley examples to expose the important boundaries.

Include a small claim set covering base parity, exact versus bounded height, and selected representation relationships. Provide examples and counterexamples rather than a large field of empty pages.

### C. Validation And Retrieval

Add lightweight checks for unique IDs, required fields, valid internal links, and missing assets. Test the reading protocol against a fixed set of questions. Do not build a general knowledge-management framework.

### D. Portable Release

Copy or extract the folder into a clean location and repeat the checks without Foundry present. Tag or otherwise identify a reviewed content snapshot when releases are introduced. Evaluate repository extraction using the forthcoming Plan 05 (repository federation).

## Completion Criteria

- A reader can distinguish geometric and Euler-valid castles without consulting application code.
- Each seed specimen has reproducible geometry and linked family definitions.
- Claims expose their assumptions, status, and supporting sources.
- A fresh assistant can explain parity, classify a specimen, locate a counterexample, and identify an open question with citations.
- Retrieval tests include an unanswerable question and a deliberately ambiguous term.
- The whole collection remains readable and internally linked outside Foundry.
- No server, vendor account, or generated index is necessary to inspect the authoritative content.

## First Decision Gate

Review the small seed collection before expanding the schema or integrating the zoo. The next planning document is Plan 02 (research programme): use the Atlas to identify investigations, not merely to accumulate pages. Publications under Plan 04 (reports and seminars) should cite Atlas definitions rather than establish incompatible conventions of their own.

Companion Plans 02-05 are planned documents, not prerequisites for reviewing this proposal.
