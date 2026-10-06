"""
Tutorial 5 — the build pipeline on a copy of your real notes.

Run:  python tutorials/05_build_pipeline.py
Same thing from the terminal, on the real notes:  python -m scaffold.src build
"""
import shutil
import tempfile
from pathlib import Path

from _lib import build, lib, project_root, section, show

root = project_root()
work = Path(tempfile.mkdtemp(prefix="build-tutorial-"))
for d in ("papers", "books"):
    shutil.copytree(root / d, work / d)
if (root / "concepts.py").exists():
    shutil.copy(root / "concepts.py", work)

section("1. build(): discover -> check -> render -> import -> index")
report = build(work)
print(report.summary())

section("2. What it produced")
for p in sorted((work / "rendered").glob("*.md")):
    show("rendered", p.name)
kb = lib.KnowledgeBase(work / "kb")
kinds = {}
for e in kb.entries.values():
    kinds[e.kind] = kinds.get(e.kind, 0) + 1
show("kb entries by kind", dict(sorted(kinds.items())))

section("3. Builds are idempotent: running again changes nothing")
before = {p: p.read_text(encoding="utf-8") for p in (work / "kb").rglob("*.md")}
build(work)
after = {p: p.read_text(encoding="utf-8") for p in (work / "kb").rglob("*.md")}
show("identical", before == after)

section("4. A broken source does not stop the build")
(work / "papers" / "broken.py").write_text("notes = undefined_name\n", encoding="utf-8")
report = build(work)
for f, err in report.errors.items():
    show(f, err)

section("5. A wrong claim makes the build fail (exit code 1 from the CLI)")
(work / "papers" / "broken.py").unlink()
(work / "papers" / "typo.py").write_text(f"""\
from {lib.__name__} import PaperNotes
notes = PaperNotes("Typo", "typo demo", "x", 2026)
x = notes.sym("x", "x", real=True)
notes.claim("(1)", "(x+1)^2 = x^2 + 1", residual=(x + 1)**2 - (x**2 + 1))
""", encoding="utf-8")
report = build(work)
show("failed claims", report.failed)

section("Terminal equivalents (run from the repo root)")
for cmd in ("python -m scaffold.src build",
            "python -m scaffold.src check scaffold/papers/bs_measures.py",
            "python -m scaffold.src find --kind exercise --status open",
            "python -m scaffold.src deps girsanov-theorem",
            "python -m scaffold.src describe scaffold/papers/bs_measures.py measures"):
    print("  " + cmd)
print(f"\n(temporary build folder: {work})")
