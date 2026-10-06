# AGENTS.md — guide to the `scaffold` repository

This file is for AI assistants (LLMs, coding agents) working in this repo. Read
it fully before making changes. It describes what the project is, how it is
laid out, the contracts between its parts, and the conventions that must be
kept.

---

## 1. What this project is

`scaffold` is a personal system for taking **checkable notes on mathematical
papers and textbooks** (mainly mathematical finance), built on SymPy.

- Each paper or textbook gets one Python file. In it, the reader records
  notation, definitions, claims (theorems, lemmas, equations, exercises) and a
  categorical skeleton (objects, morphisms, diagrams).
- Claims can be **checked mechanically**. A claim carries a *residual*, a SymPy
  expression that should be identically zero. The library simplifies it
  symbolically and falls back to numeric spot-checks.
- Commutative-diagram claims are checked by interpreting the diagram through a
  **functor** into a concrete category (e.g. Radon–Nikodym densities under
  multiplication, or matrices under matrix product).
- All sources feed a **central knowledge base** (`kb/`): one Markdown file per
  entry, linked across sources, queryable, and kept in git.

The purpose is to keep the reader honest: every claim has a visible status, and
FAILED means either a typo in the source or a misreading.

---

## 2. Repository layout

The repo root is `branch1/scaffold/`. The importable package is `scaffold/`, and
the library code lives in the **subpackage `scaffold.src`**. Note that `src` here
is a package name, not a src-layout folder.

```
<repo root>/
├─ scaffold/                    # the importable package
│  ├─ __init__.py
│  ├─ version.txt               # single source of the version number
│  ├─ src/                      # LIBRARY CODE  (import as scaffold.src)
│  │  ├─ __init__.py            # public API re-exports
│  │  ├─ __main__.py            # CLI  (python -m scaffold.src / `scaffold`)
│  │  ├─ claims.py              # Claim, Status, check_residual, numeric checks, sympy_equal
│  │  ├─ category.py            # Functor, morphism_name, describe_diagram, to_xypic
│  │  ├─ notes.py               # PaperNotes
│  │  ├─ books.py               # BookNotes(PaperNotes): sections, examples, remarks, exercises
│  │  ├─ render.py              # to_markdown, compact_definitions
│  │  ├─ build.py               # discover → check → render → import → index; Report
│  │  └─ kb/
│  │     ├─ __init__.py
│  │     ├─ entry.py            # Entry dataclass + on-disk format, KINDS, slug
│  │     ├─ store.py            # KnowledgeBase: add/merge, find, dependents, broken_links, index
│  │     └─ importer.py         # import_notes(kb, notes, ...)
│  ├─ papers/                   # USER CONTENT: one .py per paper   (no __init__.py)
│  ├─ books/                    # USER CONTENT: one .py per textbook (no __init__.py)
│  ├─ concepts.py               # USER CONTENT: hand-written general KB entries
│  ├─ kb/                       # GENERATED + hand-editable knowledge base (committed)
│  └─ rendered/                 # GENERATED Markdown per source (git-ignored)
├─ tests/                       # pytest suite
├─ tutorials/                   # runnable walkthroughs 01–05, plus _lib.py helper
├─ whl/                         # built wheels
├─ pyproject.toml               # all packaging config (there is no setup.py)
├─ build.bat / build.sh         # python -m build --wheel --outdir whl
├─ install-dev.bat
├─ setup-hooks.bat / .sh, .githooks/
└─ README.md
```

The **notes root** (the folder holding `papers/`, `books/`, `kb/`,
`concepts.py`, `rendered/`) is `scaffold/`, i.e.
`Path(scaffold.src.__file__).resolve().parents[1]`. The CLI, `tests/test_build.py`
and `tutorials/_lib.py` all locate it this way. Never assume the current working
directory is the notes root.

---

## 3. Imports: rules that must hold

- **Inside `scaffold/src/`**, always use relative imports (`from .claims import
  Status`, `from ..kb import ...`). The library must not depend on its own
  package name.
- **Everywhere else** (papers, books, tests, tutorials), import from
  `scaffold.src`:

  ```python
  from scaffold.src import PaperNotes, BookNotes, Functor, sympy_equal
  from scaffold.src.build import build
  from scaffold.src.kb import KnowledgeBase, import_notes
  ```

- Never import from `mathnotes`. That was an earlier standalone name for this
  library and no longer exists here.
- The package must be installed in editable mode for these imports to work:
  `pip install -e ".[dev]"`.

---

## 4. Core concepts and data model

### 4.1 Claims (`claims.py`)

```python
class Status(Enum):
    STATED   = "stated"        # recorded, not checked (e.g. remarks)
    VERIFIED = "verified"      # residual simplified to 0, or functor check passed
    NUMERIC  = "numeric-only"  # simplify inconclusive; random numeric spot-checks passed
    FAILED   = "FAILED"        # counterexample found
    OPEN     = "open"          # no mechanical check (yet); open exercises = to-do list

@dataclass
class Claim:
    label: str                       # the source's own label: "Prop 2.3", "(4.1)", "Ex 3.2.4"
    statement: str                   # in the reader's words
    residual: sp.Expr | None = None  # should be identically 0
    depends_on: list[str] = []       # LOCAL names: definition names or other claim labels
    status: Status = STATED
    note: str = ""
    kind: str | None = None          # theorem/lemma/example/exercise/remark...; None = infer from label
    where: str = ""                  # location, e.g. "§5.2" (set automatically inside book sections)
```

How a check works: `simplifier(residual) == 0` gives VERIFIED. Otherwise, if
the residual is numerically ~0 at random points (symbols sampled respecting
`positive=True`), it is NUMERIC. Otherwise it is FAILED. A claim with no
residual is OPEN.

**Symbol assumptions matter.** `positive=True` or `real=True` on symbols is what
lets `simplify` prove things like `sqrt(x**2) == x`. They encode the source's
hypotheses.

### 4.2 Notes objects (`notes.py`, `books.py`)

`PaperNotes(key, title, authors, year, source="")`:

| method | purpose |
|---|---|
| `sym(name, meaning, latex=None, **assumptions)` | register a symbol; returns `sp.Symbol` |
| `func(name, meaning, latex=None)` | register an undefined function |
| `define(name, expr, meaning)` | named definition; returns `expr` |
| `claim(label, statement, residual=None, depends_on=(), note="", kind=None)` | record a claim |
| `check(label, n_numeric=20, simplifier=sp.simplify)` / `check_all(**kw)` | run checks |
| `obj(name, meaning)` / `mor(name, dom, cod, meaning)` | sympy.categories `Object` / `NamedMorphism` |
| `diagram(name, premises, conclusions=None, meaning="")` | sympy.categories `Diagram` |
| `commutes(label, path1, path2, statement)` | record "path1 = path2" as an OPEN claim |
| `check_commutation(label, functor)` | decide it under a `Functor` → VERIFIED / FAILED |
| `describe(name)` / `xypic(name)` | text summary / Xy-pic LaTeX of a diagram |
| `questions` (list) | open questions while reading |

`BookNotes(key, title, authors, year, edition="", source="")` adds:

| method | purpose |
|---|---|
| `with b.section("5.2", "Girsanov"):` | stamps everything inside with `§5.2`; reopening a section is fine |
| `example(label, statement, residual=None, ...)` | kind="example" |
| `remark(label, statement, ...)` | kind="remark", status STATED |
| `exercise(label, statement, solution=None, ...)` | `solution` is a residual encoding the reader's answer; None → OPEN |
| `todo()` | exercises that are OPEN or FAILED |

Composition is written `g * f` and means g∘f (f first). sympy.categories
enforces associativity, the identity laws, and composability. Composing in the
wrong order raises `ValueError`.

**`check()` leaves claims without a residual untouched.** So a status set by
`check_commutation` survives a later `check_all()`.

### 4.3 Functors (`category.py`)

```python
Functor(name, on_objects: dict, on_morphisms: dict,   # images of generators only
        compose: Callable,    # compose(g_img, f_img) -> image of g∘f
        identity: Callable,   # identity(obj_img) -> image of id
        equal: Callable)      # equal(a, b) -> bool
```

Composites are mapped by functoriality. For SymPy scalar targets use
`equal=sympy_equal`. For matrices use
`lambda X, Y: (X - Y).applyfunc(sp.simplify).is_zero_matrix`, because
`sympy_equal` compares a matrix to 0 and would be wrong.

**Caveat:** commuting under one functor is evidence, not proof, unless the
functor is faithful. sympy.categories itself cannot decide commutativity.

### 4.4 Knowledge base (`kb/`)

Each entry is a Markdown file `kb/<kind>/<id>.md` with YAML front matter and a
free-form Markdown body:

```yaml
---
id: girsanov-theorem          # global, stable id (file name)
kind: theorem                 # one of KINDS (see below)
title: Girsanov theorem
statement: ...
expr: <srepr string>          # optional SymPy expression; round-trips exactly incl. assumptions
status: open
sources:                      # where it appears
- paper: SC-book              # source key; the field is called `paper` for books too (historical)
  label: Thm 5.2.3
  where: §5.2
depends_on: [rn-density-girsanov]
tags: [stochastic-calculus]
domain: measure-P             # morphisms only
codomain: measure-Q
checked_in: books/sc_book.py  # notes file that runs the check
curated: true                 # hand-written; imports never overwrite title/statement
latex: ...                    # display copy of expr; ignored on load
---
free-form notes
```

`KINDS = {symbol, definition, theorem, lemma, proposition, corollary, claim,
object, morphism, question, example, exercise, remark, concept}`. Add to `KINDS`
deliberately if a new kind is needed.

**Ids.** Local names become `<slug(source key)>.<slug(label)>` (e.g.
`bs-numeraire.lemma-3-1`) unless the source's `link` dict maps them to a
global id. Linking is how one concept from several sources becomes one entry.

**Merge rules (`KnowledgeBase.add`).** These are critical; keep them.

- `sources`, `depends_on` and `tags` are unioned.
- A `curated` entry (created with `owner=None`, i.e. by hand or in
  `concepts.py`, or with `curated: true` set in its file) always keeps its
  title and statement.
- An entry whose sources all come from the importing `owner` gets its
  title and statement refreshed on re-import.
- An entry shared by several sources keeps its existing wording.
- Empty fields inherit from the existing entry.
- Builds never delete entries. Stale files from renamed labels must be
  removed by hand; `broken_links()` reports dangling `depends_on`.

**Residuals are NOT stored in the KB.** Claims are catalogued with status,
dependencies and `checked_in`. The notes file stays the executable source of
truth. Definitions do store `expr`.

Queries: `find(kind=, tag=, paper=, status=, text=)`, `dependents(id)`
(transitive impact analysis), `broken_links()`, `write_index()` (writes
`kb/INDEX.md`).

---

## 5. The notes-file contract

Every file in `papers/` or `books/` (names not starting with `_`) must:

1. define a module-level variable **`notes`**, a `PaperNotes` or `BookNotes`;
2. optionally define a module-level **`link`**: `dict[local name/label → global KB id]`;
3. import only from `scaffold.src` (plus sympy and the stdlib);
4. be deterministic and side-effect free apart from building `notes`. No file
   writes, no `if __name__ == "__main__"` logic that the build relies on.

Recommended structure, in this order: notation → definitions → claims →
categorical skeleton and functor checks → questions. See
`papers/bs_measures.py` and `books/sc_book.py` as templates.

`concepts.py` defines `register(kb)` and is run **first** on every build, so the
reader's own wording wins.

---

## 6. Build pipeline and CLI

`build(root, kb_dir="kb", rendered_dir="rendered", files=None) -> Report`:

1. run `concepts.py:register(kb)` if present;
2. for each notes file: load by path, `notes.check_all()`, write
   `rendered/<stem>.md`, then `import_notes(kb, notes, notes_file=<rel path>, link=module.link)`;
3. write `kb/INDEX.md`; collect `broken_links`.

A file that raises is recorded in `Report.errors` and skipped; the build
continues. `Report.failed` lists `(file, label)` pairs with status FAILED.
**Builds are idempotent**: a second build changes no KB file. A test enforces
this.

CLI (the `scaffold` console script, or `python -m scaffold.src`). Its defaults
point at the notes root, so it works from any directory:

```
scaffold build                                    # exit 1 if any FAILED claim or errored file
scaffold check scaffold/papers/bs_measures.py     # one file's checks
scaffold find --kind exercise --status open
scaffold find --text girsanov
scaffold deps girsanov-theorem
scaffold describe scaffold/papers/bs_measures.py measures
```

The CLI reconfigures stdout to UTF-8 (Windows consoles default to cp1252).

---

## 7. Development

```
pip install -e ".[dev]"                 # editable install + pytest + build
pytest                                  # 9 tests: claims, category, kb, build
python tutorials/01_claims_and_checks.py   # ... through 05
build.bat  /  ./build.sh                # wheel into whl/
```

Packaging lives entirely in `pyproject.toml` (setuptools backend, no
`setup.py`):

- `[tool.setuptools.packages.find] include = ["scaffold", "scaffold.*"]`. Do
  **not** set `where = ["src"]`; there is no top-level `src/`.
- The version is dynamic: `dynamic = ["version"]` in `[project]` and
  `[tool.setuptools.dynamic] version = { file = "scaffold/version.txt" }`.
- TOML gotcha: a `[header]` starts a table that runs until the next header.
  All `[project]` keys must come before any `[tool...]` section.
- The console script is `scaffold = "scaffold.src.__main__:main"`.
- `papers/`, `books/` and `kb/` have no `__init__.py`, so they are not packaged
  into the wheel. That is intended.

Platform notes: the primary environment is Windows, VS Code, Python 3.13, in a
`.venv`. **Always pass `encoding="utf-8"`** to `open()`, `read_text()` and
`write_text()`. Notes contain Greek letters, `→` and `∘`, and the Windows
default encoding (cp1252) will raise `UnicodeEncodeError`.

---

## 8. Common tasks: how to do them correctly

**Add notes for a new paper.** Copy `scaffold/papers/bs_measures.py` and
change the key, title and content. Add `link` entries for any concept already
in the KB (check with `scaffold find --text ...`). Run `scaffold build`.

**Add a textbook.** Copy `scaffold/books/sc_book.py`. Use `with
b.section(...)`. Link canonical theorems to global ids so papers can depend on
them.

**Turn a claim into a checked claim.** Express it as `lhs - rhs` with the right
symbol assumptions. If `simplify` is slow or inconclusive, try a custom
`simplifier=` (e.g. `lambda e: sp.simplify(sp.expand(e))`) before accepting
NUMERIC.

**Expectations under a Gaussian.** Integrate against the density, e.g.
`sp.integrate(g(x) * exp(-x**2/(2*t))/sqrt(2*pi*t), (x, -oo, oo))`. See
`books/sc_book.py` and `tutorials/03_books_and_exercises.py`.

**Add a library feature.** Put it in the matching module, re-export it from
`scaffold/src/__init__.py` if public, add a test in `tests/`, and keep
`pytest` and the idempotence test passing. If it changes the on-disk entry
format, keep loading of existing files backward compatible (new fields need
defaults; omit falsy values when writing).

**Readable rendered output.** `render.to_markdown(n, compact=True)` rewrites
each definition in terms of earlier ones (so `C` shows `d1`/`d2`, not the
expansion). This affects display only, never the checks.

---

## 9. Things NOT to do

- Don't store residuals, or anything only reproducible by running code, in
  `kb/`.
- Don't overwrite curated KB wording from importers, and don't weaken the
  merge rules.
- Don't make the library import `scaffold.src` absolutely from inside itself.
- Don't assume the working directory is the notes root.
- Don't write files without `encoding="utf-8"`.
- Don't reintroduce `setup.py`, or `where = ["src"]` in `pyproject.toml`.
- Don't claim a diagram commutes because sympy.categories accepted it. It only
  records the claim.
- Don't edit files under `rendered/`. They are regenerated on every build.

---

## 10. Glossary

- **residual**: expression that should be identically 0 if a claim is true.
- **source key**: `PaperNotes.key` / `BookNotes.key`, e.g. `BS-numeraire`,
  `SC-book`.
- **link**: per-source mapping from local labels to global KB ids.
- **curated**: KB entry whose wording belongs to the reader.
- **notes root**: `scaffold/` folder holding `papers/`, `books/`, `kb/`,
  `concepts.py`.
- **functor check**: deciding a commutativity claim by mapping both paths into a
  concrete category and comparing.
