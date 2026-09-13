# Plan 04: Reports, Seminars, And Public Research

Status: proposed publication programme; titles and sessions below are not completed publications or scheduled events.

Lead: Director Engelbert Eggwall, with an editor and research owner assigned per artifact. These are responsibilities, not new permanent departments.

## Purpose

Give the Center a regular way to explain, challenge, correct, and circulate its work. Research should leave behind more than code and a conversation: a reader should be able to follow the question, reproduce the experiment, understand the result, and find what remains unresolved.

Use the projects in [Plan 02](plan-02-research-programme.md), the mathematical memory in [Plan 01](plan-01-taxonomy-atlas.md), and the institutional voice in [Plan 03](plan-03-institution-and-eggwall.md). Publications cite the Atlas but do not require a reader to reconstruct an argument from scattered wiki entries.

The goal is a small, credible body of work, not a simulated university press with empty series and invented peer review.

## Publication Forms

| Form | Purpose | Minimum useful artifact |
| --- | --- | --- |
| Technical report (`TR`) | A substantial derivation, algorithm, or synthesis | A complete argument with assumptions, evidence, limitations, and references |
| Working note (`WN`) | Partial results, promising approaches, and open questions | A precise question and a clear boundary between established and unfinished work |
| Specimen bulletin (`SB`) | Explain one specimen or family | Geometry, accession references, defining properties, and why the example matters |
| Instrument manual (`IM`) | Explain a program as a research instrument | Input/output contract, conventions, arithmetic limits, reproducible examples, and failure modes |
| Seminar notes (`SN`) | Teach a route through a question | Prerequisites, worked examples, an argument, exercises, and references |

Do not require every investigation to produce every form. Errata belong to the document they correct, rather than becoming an additional publication series. Negative results may be working notes or technical reports depending on the completeness of the investigation.

A report is not required to prove a new theorem. A careful reconciliation of two derivations, a documented algorithm comparison, or a useful counterexample can justify publication if its contribution is explicit.

## Identity And Revisions

Assign stable identifiers such as `ECRM-TR-001` when an artifact is registered. Keep the identifier independent of its title, filename, author persona, and hosting repository. A central lightweight catalogue allocates IDs; do not build an identifier service.

Each registered artifact records its title, contributors, document type, editorial status, version, dates, source location, and related Atlas records or projects. Distinguish a publication's editorial status from the knowledge status of individual mathematical claims.

Suggested editorial lifecycle:

```text
draft -> ready-for-review -> released -> revised or withdrawn
```

Review may return a document to draft. Describe review honestly: author-checked, internally reviewed, or externally reviewed only when those activities actually occurred. An AI critique is not independent human peer review.

Released versions remain identifiable. Citations should be able to specify a document ID and version, with a corresponding source revision. Do not silently replace a released PDF while keeping the same version label.

If a working note develops into a technical report, give the report its own ID and link the relationship. Do not erase the exploratory record. If a claim fails, retain the affected version with a visible correction or withdrawal notice and explain the consequences.

## Technical Report Contract

A report should answer these questions without relying on institutional lore:

1. What question does this document address, and what does it contribute?
2. Which objects, parameter ranges, conventions, and arithmetic domains are in use?
3. What was already known, and where did it come from?
4. What is the argument or algorithm, including its boundary cases?
5. Which claims are proved, experimentally observed, conjectured, or left open?
6. How can a reader check the examples and reproduce the reported computation?
7. What limitations, unsuccessful approaches, and next questions remain?

Begin with a short abstract and at least one small example. Restate essential definitions while citing the relevant Atlas revision. A long proof may have a separate intuitive overview, but the overview must not quietly substitute an analogy for the argument.

Use descriptive figures with captions, explicit axes and parameter order in tables, and a notation list when needed. Distinguish exact integers, modular residues, and approximations visibly. Use citations for external results and clearly label any adaptation of the original Euler notes.

Eggwall may introduce a report in a short foreword. The mathematical body should remain readable without knowing who he is. Actual authorship, source credit, and substantive AI assistance should be described under an agreed attribution policy rather than hidden behind fictional staff names.

## Reproducible Evidence

Every computational artifact needs an evidence record containing:

- The question being tested and the exact set of inputs.
- Code repository and commit, entry point, dependencies, and relevant environment information.
- Arithmetic domain and precision, including modulus where applicable.
- Random seed and sampling method when randomness is used.
- Commands for a small check and, separately, the full reported experiment.
- Expected outputs, validation method, and known limits on what agreement establishes.
- Runtime and memory budget where computation is substantial.
- Output locations and checksums for separately stored artifacts when appropriate.

The small check must be feasible on an ordinary development machine. A reader should not have to repeat an extreme-parameter computation merely to confirm that the example and implementation agree.

Where independent verification is claimed, explain its independence. A second programming language using the same translated recurrence is a useful implementation check, but not necessarily an independent mathematical derivation.

Generated plots and tables need a traceable source. Keep lightweight canonical examples in version control; store large outputs as versioned release artifacts when warranted, not as unexplained binary additions. Document expected differences for nondeterministic timing measurements instead of promising byte-for-byte reproducibility of everything.

## The Seminar Programme

Working title: the Enfilade Evening Seminar. Begin with an occasional series tied to available research, not a weekly schedule the project cannot sustain.

A seminar is a teaching and criticism event, not proof that a result has been validated. It may be delivered live, recorded with consent, or published as a self-contained reading session. Mark each format accurately; do not invent attendance, discussion, or events that never happened.

Proposed opening sequence:

| Session | Focus | Participant's concrete task |
| --- | --- | --- |
| What Exactly Is a Block? | Maximal runs, geometry, and conventions | Count blocks in a small skyline and explain why adjacent cells are not separate blocks |
| The Base Is Not Innocent | Tower and castle parity | Translate an example between tower and full-castle encodings |
| Sibling Independence | Decomposition into noninteracting sub-block towers | Identify precisely where the mandatory gap is used |
| Counting by Cancellation | Signed counts and parity extraction | Recover even and odd counts from a tiny enumerated class |
| A Trillion in Either Direction | Width and height recurrence regimes | Explain why a distant index is different from a large state space |
| The Counterexample Cabinet | Definitions, failed guesses, and evidence | Test a conjecture and accession a minimal witness if it fails |

These are a syllabus, not six launch commitments. Produce the first session before fixing the rest of the schedule.

Each session packet contains an abstract, intended audience, prerequisites, linked readings, worked examples, exercises with solutions or hints, and an unresolved question. Slides are optional. Notes must remain usable without audio, animated graphics, or a live demonstration.

A practical live format is a short example-led introduction, one sustained argument, and time for questions. Preserve substantive objections and resulting corrections with appropriate contributor permission and credit. A plain discussion note is sufficient; there is no need for invented proceedings.

## From Research To Exhibit

Use one chain of evidence across formats:

```text
question -> experiment -> Atlas update -> working note
         -> seminar and criticism -> revised report -> public exhibit
```

This is a useful path, not a mandatory order for every project. A counterexample may begin as a zoo specimen and lead back to a revised definition.

The Atlas stores durable definitions, claims, and specimen records. A report explains a sustained argument at a specific revision. A seminar teaches that argument. The zoo offers an approachable object through which to encounter it. These are distinct views, not competing sources that independently edit the same fact.

For example, the proposed unimodality investigation can supply a family definition, a small exact table, a short proof about row runs and block count, a specimen bulletin, and an exercise about parity. It does not need five independent research projects.

When a source claim changes, identify affected reports, session packets, and exhibits. Correct the shared record first where appropriate, then issue explicit publication revisions. A previously released report remains a historical document; do not make its meaning depend silently on the latest wiki edit.

## Production And Distribution

Start with Markdown sources, checked-in small illustrations, and a simple catalogue. Use LaTeX or another document tool when equations and typesetting justify it; do not migrate every note to a larger publishing system immediately.

An eventual `enfilade-publications/` home may contain the catalogue, templates, document sources, and small supporting assets. Code experiments stay with their maintained implementations and are cited by revision. Repository ownership and extraction are addressed in Plan 05.

Prefer readable HTML and printable output when a publishing pipeline is introduced. Ensure equations, figure descriptions, navigation, and contrast work without the CRT aesthetic. A report may borrow a restrained letterhead or accession stamp without sacrificing legibility.

Check source and asset licenses before redistribution. Select explicit licenses for new text and code rather than assuming the repository or website's existing terms cover every artifact. Preserve bibliographic attribution and avoid duplicating entire external sources unnecessarily.

Creating plans or drafts does not authorize external publication, mailing lists, event registration, or submissions to journals or databases. Those are later, explicit actions.

## First Release Cycle

### A. Minimal Editorial Kit

Create a catalogue format, one report template, and one seminar packet template. Define ID allocation, versioning, and the correction process. Reuse the research evidence records rather than inventing a second experiment schema.

### B. Pilot Publication

Use the signed-enumeration or unimodality work proposed in Plan 02. Produce one working note or report with a small reproduction command, clear claim status, and links to the relevant Atlas records. Do not assign a release date before the argument and evidence exist.

### C. Pilot Seminar

Develop the first session packet and a modest Eggwall introduction. Test whether a reader outside the project can complete its exercises without relying on unstated conventions. Publish it as reading material if no actual event is held.

### D. Correction Drill

During draft review, identify an ambiguity or intentionally marked test error, trace its dependencies, and verify the revision process. Do not seed a released document with a false result merely to exercise the workflow.

### E. Retrospective

Record the work needed to produce and maintain the artifacts. Decide whether the next cycle needs better templates, a rendering pipeline, or simply another investigation. Expand the series only when the first cycle has readers or a clear research purpose.

## Completion Criteria

- One substantive publication and one self-contained seminar packet exist, with their actual status clearly marked.
- A reader can find definitions, sources, evidence, and open questions from the publication itself.
- The small reproduction check succeeds in a clean documented environment.
- Published claims have appropriate proof or explicitly bounded computational evidence.
- Corrections preserve stable identity and make affected versions discoverable.
- Institutional flavor does not obscure attribution, accessibility, or mathematical meaning.
- The catalogue does not advertise unwritten reports or unheld seminars as completed work.
- The next cycle is small enough for the actual contributors to maintain.

## Decision Gate

Complete and review the pilot before adding a journal, annual conference, proceedings volume, or elaborate publishing platform. Those can become credible outcomes of sustained work rather than prerequisites for beginning it.
