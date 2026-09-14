# Plan 05: A Federation Of Independent Projects

Status: proposed architecture and migration plan; no repositories, services, or integrations are created by this document.

Lead: Director Engelbert Eggwall for programme ownership; individual maintainers for each project and release.

## Purpose

Let the Center grow into many research projects without turning Castle Foundry into a monolith or creating a fleet of empty repositories. Projects should share mathematical language and evidence while remaining free to choose different implementations, publication formats, and release schedules.

The Center is the umbrella. Foundry is an instrument. The Atlas is the mathematical memory. Publications explain results, and the institutional site helps readers find them. None needs to become the runtime dependency of all the others.

This document completes the planning sequence:

1. [Plan 01: Taxonomy Atlas](plan-01-taxonomy-atlas.md) defines portable mathematical memory.
2. [Plan 02: Research Programme](plan-02-research-programme.md) identifies investigations and first artifacts.
3. [Plan 03: Institution And Eggwall](plan-03-institution-and-eggwall.md) establishes the editorial persona and setting.
4. [Plan 04: Reports And Seminars](plan-04-reports-and-seminars.md) defines publication and teaching practice.
5. Plan 05 defines ownership, interfaces, and conditions for separation.

The plans propose future work; their completion is not the completion of those systems. The original root `PLAN.md` describes Foundry's earlier implementation programme. Do not silently treat its historical monorepo and browser-technology choices as instructions for every future Center project.

## Proposed Homes

Names are working names, not instructions to create repositories immediately.

| Home | Owns | Does not own |
| --- | --- | --- |
| Castle Foundry | Existing Python library, browser instrument, construction, inspection, rendering, and local tests | All Center research, institutional canon, or the authoritative taxonomy |
| `enfilade-atlas` | Definitions, families, specimens, claims, source records, and curated experiment summaries | Every executable experiment or the public application's runtime |
| Focused laboratories | Experimental code, notebooks, benchmarks, and algorithm-specific evidence | Private redefinitions of shared mathematical terms presented as universal |
| `enfilade-publications` | Publication catalogue, document sources, seminar packets, revisions, and small supporting assets | A second independently edited specimen database |
| `enfilade-center` | Institutional canon, project directory, public navigation, and actual announcements | Authority over mathematical truth or mandatory hosting for all artifacts |

The Atlas may incubate in Foundry as the isolated `enfilade-atlas/` folder specified in Plan 01. Institutional material could similarly begin under `enfilade-center/institution/`, and publication sources under `enfilade-publications/`, if keeping them here is useful. Alternatively, start those later projects separately when a maintainer and first artifact exist. Do not create all these folders now just to reserve names.

Keep `foundations/` as the planning record. It is not the Atlas, a source-code package, or an operational control plane.

## Ownership And Authority

Assign a clear home to each kind of record:

- Mathematical definitions and curated claims belong to the Atlas, with status, sources, and revisions.
- An implementation owns its actual behavior and supported input contract. Disagreement with a definition is documented and investigated, not concealed by changing one side silently.
- An experiment's executable procedure belongs beside its code. The Atlas records the conclusion, scope, and evidence reference rather than maintaining another copy of the program.
- A report owns its argument at a particular version. It cites the definitions and evidence used, even if those later change.
- The institutional bible owns fictional canon and voice. It does not confer proof status or substitute for source attribution.

Mathematics is not made true by being in the designated repository. The point of ownership is to make corrections and disagreements discoverable, not to suppress independent interpretations.

## Minimum Shared Contracts

Begin with documented conventions and a small fixture set, not a universal client library or network API.

### Definitions And Citations

Use stable Atlas IDs plus an identifiable content revision. Describe incompatible convention changes explicitly: a revised meaning of valley or a different height convention must not appear to be a harmless title update.

Human-readable links may point to a stable landing page. Reproducibility references must also identify the version actually used. External repository links should use revisions where correctness depends on their contents, rather than assuming the default branch never changes.

### Specimens And Counts

A minimal exchange record should identify the specimen accession when present, the encoding and convention version, its geometry, and the relevant dimension and parity interpretation. Keep nicknames separate from identity.

For count fixtures, specify the counted class, parameter order, exact versus bounded height, and exact versus modular arithmetic. Include the modulus with a residue. Encode integers outside interoperable JSON numeric precision as decimal strings under an explicit field contract; do not silently round them in a browser.

The initial fixture set should include geometric odd-block specimens, height-one and width-one boundaries, broad versus strict valleys, representation round trips, and published count checkpoints. Include malformed encodings separately from valid geometry that merely fails Euler parity.

Store curated shared fixtures with the Atlas or its release artifacts once there is an actual consumer. A consumer may pin a small snapshot with its source revision and checksum. Its own algorithm tests remain local. Creating a dedicated fixture repository is unnecessary until maintenance genuinely requires one.

### Experiments And Publications

Use the evidence contract from Plan 04: code revision, inputs, arithmetic domain, environment, commands, and output references. A publication ID links the report to that evidence without requiring its source tree to import the whole laboratory.

Prefer small text formats and explicit schemas where automated exchange exists. Do not build serialization for hypothetical consumers. Add fields and versioning rules in response to real use, preserving any already published contracts that people rely on.

## Dependency Direction

Aim for optional, versioned consumption:

```text
Atlas release -> curated specimen and definition snapshot -> Foundry exhibit
Atlas revision + laboratory evidence -> publication
Project and publication catalogues -> Center directory
```

These arrows describe content consumption, not compulsory network calls. A laboratory can read or vendor the small materials it needs. Atlas contributions return through reviewed records and patches, not through a live dependency on every experiment.

Avoid a build cycle in which the Atlas requires Foundry to render every page while Foundry requires the Atlas service to start. Avoid a site build that needs every laboratory installed. An unavailable project should not take the entire Center offline.

## Foundry Integration

Keep the current webapp functional while the Atlas develops independently. Do not replace its curated specimen data until an export contract and a reviewed Atlas snapshot exist.

A first integration can be a small static export of selected accession IDs, encodings, short descriptions, and source links. Record the Atlas revision in the export and make regeneration explicit. The application remains deployable without an Atlas server.

Before replacing existing specimen definitions, compare encodings, names, and fact sheets against the current zoo. Resolve differences rather than treating the export as automatically correct. New classification terms should not silently change the meaning of existing filters.

Display the content version or provide a source link where useful. If an update fails validation, retain the last reviewed snapshot. Keep editorial writes in the Atlas workflow instead of turning the webapp into an unreviewed memory editor.

Cross-language arithmetic and feature-definition differences are separate correctness work. This plan does not promise that importing an Atlas snapshot fixes the browser's large-number limitations or changes the current implementation's mathematical semantics.

## Languages And Interpretations

Choose languages to support different kinds of work, not to fill a roster:

| Language or environment | Candidate role | Reason to start a separate implementation |
| --- | --- | --- |
| Python | Readable reference algorithms, small exact checks, and experiments | Already present; extend it where it remains the clearest instrument |
| Java | Existing large-parameter Euler solver | Reproduce and document the original computational route before considering relocation |
| JavaScript | Interactive public construction and explanation | Browser interaction and static deployment, with explicit numerical limits |
| SageMath or Julia | Symbolic exploration, recurrences, and numerical experiments | A concrete investigation benefits from the environment's mathematical tools |
| Rust or C++ | Performance-oriented enumeration or recurrence experiments | Measurements demonstrate a bottleneck and the project can maintain the extra implementation |
| Lean or another proof assistant | Selected definitions and machine-checked arguments | The mathematical statement is stable enough to formalize and a contributor can maintain it |

Do not move or republish the existing external Euler solver merely because this federation is proposed. Reference it first, check licensing and ownership, then decide whether a new maintained home would actually help.

An independent interpretation can be more valuable than a direct translation. Grammar-based and column-height algorithms should expose their reasoning so agreement tests more than shared code. Benchmark implementations only on equivalent domains and arithmetic contracts.

## When To Split

Create a separate repository when it has a concrete artifact, an accountable maintainer, a bounded purpose, and a benefit from independent history or releases. Common triggers include distinct dependencies, different audiences, a sustained experiment programme, or an established consumer outside Foundry.

Do not split because every division needs a repository, every language needs a package, or an architectural diagram looks more impressive with additional boxes. A single exploratory script with a clear question can remain a local experiment until it earns a separate home.

Before extraction, record the decision: what moves, why, who maintains it, what remains here, and how references will work. Keep this decision short and adjacent to the affected project.

## Extraction Procedure

1. Identify the complete portable boundary, including assets, sources, licenses, templates, and necessary validation tools.
2. Check for parent-relative imports, machine-specific paths, hidden configuration requirements, and links that assume Foundry is present.
3. Test the folder in a clean location with documented setup and no access to the parent checkout.
4. Choose a history strategy: preserve relevant history in a new repository or import a snapshot with an explicit source-commit record. Do not rewrite the existing Foundry history.
5. Establish the destination only with explicit authorization for repository creation and publication. Verify that it contains no credentials or unrelated private material.
6. Run the destination's checks and verify that citations, accession IDs, and artifact provenance survive the move.
7. Update consumers and directories to the new versioned location. Leave a concise pointer at the former home where useful rather than two independently editable copies.
8. Remove or archive the old working copy only as an explicit migration step after destination verification, not as incidental cleanup.

Submodules, vendored snapshots, packages, and direct links are options with different maintenance costs. Choose one for a demonstrated consumer need. Plain citations and small reviewed snapshots are the default starting point; no universal cross-repository synchronization system is required.

## Maintenance And Releases

Each project documents its status as experimental, maintained, or archived; its owner; setup; verification commands; and supported contracts. The Center directory links to these records rather than inventing a separate source of truth about project health.

Release independently. A publication may cite an older Atlas revision while Foundry uses a newer specimen snapshot. Record that relationship rather than requiring all repositories to share one version number or release date.

Use lightweight automated checks where they add value: links and metadata for the Atlas, local tests for code, reproducibility checks for evidence, and document builds for publications. Do not require every change to build every language implementation.

Define explicit licenses before redistribution. Keep secrets and machine-specific AI client configuration out of portable content. Generated indexes and caches are disposable; source documents, specimen identity, and evidence provenance are not.

An archived project remains citable with its last known working revision and limitations. A failed experiment or unmaintained instrument can still be useful without pretending it is a supported service.

## Phased Adoption

### A. Preserve The Current Instrument

Leave Foundry's application, package, and original planning history intact. Adopt the proposed boundaries in new work rather than performing a speculative reorganization of the existing repository.

### B. Prove Atlas Portability

Build and validate the small isolated Atlas described in Plan 01. Its clean-location test is the first practical test of this architecture. A public site or separate repository is not required to pass it.

### C. Complete One Research Cycle

Use existing tools for the initial investigations in Plan 02. Create the minimal institutional and publication artifacts from Plans 03 and 04. Keep content ownership clear even if several folders temporarily share a repository.

### D. Add One Real Consumer

Choose either a reviewed Foundry specimen export or a second research implementation that uses shared fixtures. Pin the consumed revision and document an update process. Check that either project remains useful when the other is unavailable.

### E. Extract Where Justified

Apply the split criteria to the Atlas or a laboratory with an actual maintenance need. Establish a small Center directory when there are multiple real destinations to navigate. Expand from demonstrated use, not a predetermined repository count.

## Completion Criteria

- A reader can identify the authoritative home of definitions, code, evidence, publications, and fictional canon.
- The Atlas can move outside Foundry without losing internal links or meaning.
- At least one real consumer uses an explicit revision and a documented exchange contract.
- Shared fixtures distinguish domain, convention, and arithmetic differences without requiring one universal library.
- Independent projects can be tested, released, and archived without coordinated changes to every other project.
- Repository extraction preserves provenance and does not rewrite or destroy the original history.
- Existing application behavior is not changed as an unreviewed side effect of institutional expansion.
- New repositories have artifacts and maintainers rather than only names and aspirational READMEs.

## Programme Decision Gate

After the first portable collection and complete research cycle, review what the Center actually produced and what it can maintain. Choose the next investment among deeper mathematics, a better instrument, a clearer publication, or a new home for sustained work. The federation is successful when it makes those choices easier, not when every proposed component has been built.
