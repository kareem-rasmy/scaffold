# Tutorials

Run from the project folder, in order. Each prints what it demonstrates;
none of them touch your real `kb/`.

| script | shows |
|---|---|
| `01_claims_and_checks.py` | assumptions, definitions, claims, verified / FAILED / numeric-only, catching a typo |
| `02_categories_and_functors.py` | objects, morphisms, category laws, diagrams, functors that decide commutativity, Xy-pic |
| `03_books_and_exercises.py` | `BookNotes`: sections, examples, remarks, exercises as checked solutions, to-do list |
| `04_knowledge_base.py` | curated entries, linking one theorem across a book and papers, queries, impact analysis |
| `05_build_pipeline.py` | `build()` end to end, idempotence, error isolation, failing builds, CLI equivalents |

```
python tutorials/01_claims_and_checks.py
```

`_lib.py` imports from `scaffold.src` and locates your notes via the
`scaffold` package, so the scripts work from any working directory.
