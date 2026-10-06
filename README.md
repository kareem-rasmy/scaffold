# math-notes

Checkable notes for mathematical papers and textbooks, built on SymPy, with a
central knowledge base of definitions, theorems, claims, objects and morphisms.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (source .venv/bin/activate elsewhere)
pip install -e ".[dev]"
```

## Layout

```
scaffold/
├─ src/                  the library
│  ├─ claims.py          Claim, Status, symbolic + numeric checks
│  ├─ category.py        Functor, diagram printing, Xy-pic export
│  ├─ notes.py           PaperNotes
│  ├─ books.py           BookNotes (sections, examples, remarks, exercises)
│  ├─ render.py          Markdown rendering
│  ├─ build.py           discover → check → render → import into kb/
│  ├─ __main__.py        command line
│  └─ kb/                Entry (file format), KnowledgeBase (queries), importer
├─ papers/               one .py per paper      (you write these)
├─ books/                one .py per textbook   (you write these)
├─ concepts.py           your own general entries (optional)
├─ kb/                   the knowledge base: one .md per entry + INDEX.md (commit it)
├─ rendered/             generated notes per source (git-ignored)
└─ tests/
```

## Workflow

1. Copy `papers/bs_measures.py` or `books/sc_book.py` as a template. A source
   file must define a module-level `notes` (`PaperNotes` / `BookNotes`) and may
   define `link`, mapping local labels to global KB ids
   (e.g. `{"Thm 5.2.3": "girsanov-theorem"}`). Linking is how the same
   concept from several sources becomes one KB entry.
2. While reading: notation → definitions → claims (with a residual that should
   be 0, or none if not mechanically checkable) → categorical skeleton →
   questions.
3. Build:

```bash
scaffold build                         # check all, render, update kb/; exit 1 on failures
scaffold check papers/bs_measures.py   # just one file's checks
scaffold find --kind exercise --status open
scaffold find --text girsanov
scaffold deps girsanov-theorem         # what relies on it
scaffold describe papers/bs_measures.py measures
```

(`python -m scaffold ...` works too.)

## Statuses

| status | meaning |
|---|---|
| verified | residual simplified to 0, or a commutativity check passed under a functor |
| numeric-only | simplify was inconclusive, random numeric spot checks passed |
| FAILED | counterexample found: a typo in the source or a misreading |
| open | nothing to check mechanically (yet); open exercises are your to-do list |
| stated | recorded only (e.g. remarks) |

## KB merge rules

- Entries you create yourself (`concepts.py`, or `curated: true` in a file's
  front matter) keep their title and statement; imports only add sources,
  tags and dependencies.
- An entry that came from exactly one source is refreshed when that source is
  re-imported.
- An entry shared by several sources keeps its existing wording.

Builds don't delete entries. If you rename a label, delete the stale file in
`kb/`; `scaffold build` reports dependencies that point to missing ids.

## Notes

- `sympy.categories` records objects, morphisms and diagrams but cannot prove
  commutativity; `Functor` checks it under a concrete interpretation, which is
  evidence rather than proof unless the functor is faithful.
- Always write files with `encoding="utf-8"`; notes are full of Greek and arrows.
