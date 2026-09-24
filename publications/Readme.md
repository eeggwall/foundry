This document is collecting ideas and notes about 
potential future publications and forums for
dissemination of research for the Enfilade Center
for Castle Research.

It is notes, not a spec. Some things below are settled and carry
their reasoning; others are stated as open. Nothing here has been
implemented, and no document has been numbered yet.


## What has to be decided, and in what order

Three questions, and they only work in this order:

1. **The unit.** What set of things gets an identifier.
2. **The string.** What that identifier looks like.
3. **The layer on top.** Pointers, collections, shelf marks - things
   that refer to identified documents without being documents.

A proposal that answers 2 before 1 is not an answer yet. The sections
below are mostly about 2 and 3, because that is where the thinking
started; the unit question is still open and is the one that would
change the most.


## The corpus this has to serve

Facts as of 2026-09-20, so the scheme is sized against the real thing:

* Wiki is 110 pages: 30 Sources, 51 Concepts, 29 Analyses.
* 133 IDEAS items: 76 open, 57 done.
* Nine departments in `DEPARTMENTS.md`: R E N Z Q S T F X. More expected.
* Twelve seminar arcs

Artifact types the plans already name, scattered and not yet reconciled
with anything below: technical report, working note, algorithm note,
instrument report, field guide, sequence register, representation atlas, 
discrepancies register, seminar material.

## Laying out the concepts

### Document classes

Each class has to answer the same three questions, recorded in the three columns,
and the blanks are where the thinking stops.

| Class | Mutable | Gets an accession number | Example in the corpus |
|---|---|---|---|
| Wiki pages    | yes, continuously     | no        | all 110 pages |
| Publications  | no, frozen at issue   | yes       | none yet |
| Periodicals   | no, frozen at issue   | no        | none yet |

Wiki pages are the "external brain" for the center and are already
typed one level down - Sources, Concepts, Analyses. That is the same
idea as a publication series, running one layer below it. 

The two systems should be built to look alike deliberately, or the 
resemblance will become confusing later.

The registers row is a key blank. "Living pointers, citable"
does not pin down how exactly they are cited. The answer will
determine whether registers are a class at all.

### No department letters in identifiers

DO NOT put the department name/letter in any document identifier.
This makes the document identifiers too rigid, it gets away from the
intended purpose as canonical identifiers.

**Department must stay out of the identifier.**

Furthermore, DO NOT put the publication type in any document identifier
(for example, inserting "TR" into the identifier if it is a technical report).
While the publication type cannot be changed after publication
(since different publication types require different information),
it introduces confusion and makes identifiers unpredictable, in addition
to requiring its users to understand our internal schema.

**Publication type must stay out of the identifier.**

Principle: one canonical identifier, no knowledge of internals needed
to read or compare it.

### Series

Series names the type of publication:
* Technical Report (completed work containing results others can use)
* Working Note (documenting preliminary or failed approach)
* Computational Record (repository with notebook/data/environment details)
* Seminar Notes
* Problem Set
* Erratum

(This is a provisional list. Computational Record is the most fuzzy,
since it is most likely to need to evolve. Current plan is to have this
be a record that points to a GitHub repository tag/commit hash.)

**The series is metadata on the record. No metadata appears in the identifier.** 

`ECR-00001` is the whole ID, one form only, no ambiguity.
"Technical Report ECR-00001" is ordinary prose, not a second form of the
name. This canonical identifier is the entire, unique, and only ID. 
Documents do not have any "alternative" IDs.

Series never changes for a given document, because documents freeze. A
working note that grows into a report does not get relabelled - a new
report is issued that obsoletes the note, and both stay reachable.

The Working Note is intended to capture results that are not theorems
but deserve publication anyway. These unsuccessful approaches should be 
preserved and have a place to live - hence the Working Note series.

(Frozen-on-publication may not be right for all of these documents.
Problem Set, in particular, should be able to be updated with errata
in the same document, rather than publishing it in a separate document.)

**Obsoletes/updates.** Metadata field `obsoletes` and `obsoleted by`
allow documents to remain published and reachable forever, but also
allows one document to render another obsolete. This preserves the
documents as they were when published (errors get erratum, not silent
fixes). This characteristic makes the series archival.

To replace a document with a new version, you publish a new document with
a new identifier, and add `obsoletes` to its metadata (and update the 
`obsoleted by` metadata of the obsolete document).

One report can carry multiple take-homes (proofs, conjectures, observations),
so we DO NOT attempt to classify documents according to a
"this is a proof" or "this is a conjecture" system.

### Periodicals

We have two shapes for periodicals, and they should not be combined - 
different authors, different readers, different intent:

* **Circulars** - circulate outward, from the director to everyone.
  Institution-wide, administrative, landing-page material. Plan 03 has a
  tone sample for Circular No. 1.
* **Bulletins** - a department reporting its own news to whoever follows
  that department.

Collapsing them means the director's voice has to carry nine
departments' worth of technical news.

Periodicals are news, so they are treated differently from all other
published documents: they do not get official accession numbers,
they are not tracked in the publications database, and they are not
subject to the same restrictions as official publications.

(So, the department letter can and should be in the periodical title.)

However, Periodicals are still required to have a title and a number.
The title should be a basic description, and the number should be
a simple sequential number. Examples:
* Director's Circular 14
* F Department Bulletin 7

**Periodical issues are not in the unit set of published documents.**

Principle: do not treat periodicals like other published documents.

### Seminars

Seminars can be thought of as a "story arc" covering concepts in a particular
order, plus whatever the delivery is intended to produce. It is a curated
path through a body of material.

A delivered arc emits a Seminar Notes document, which is frozen and
given an accession number.

## Wiki pages

The wiki is an "external brain" that the entire Center uses to share ideas.
They change quickly, are under version control, and should never receive
an accession number. The wiki page editing and publishing process is
completely and totally separate.

**Wiki pages are not in the unit set of published documents.**

## Summary

In summary:
* The unit of publication is frozen documents written for a reader.
* Wiki pages and periodical issues are not in the unit set of published documents.
* Published documents should be thought of as documents that stand on their own 
  content and references, they should not lean on the wiki. The wiki content
  is the constantly-changing body of knowledge. Publications draw from that
  to produce standalone publications.
* The periodicals and wiki pages will be read by me and anyone else that's 
  "in" on the project.
* The published documents are intended to stand on their own, be something that
  could actually be citable (like Dijkstra's EWD memos), and contain real math
  that is understandable outside of the fictional universe of the "Enfilade Center".
* Constraints: small team, and using static GH Pages site (pelican to generate site, 
  JSON for catalog).
