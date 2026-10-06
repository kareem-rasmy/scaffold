"""
Build pipeline: discover notes files, run checks, render, import into the KB.

Conventions
  papers/*.py, books/*.py   each defines a module-level `notes`
                            (PaperNotes / BookNotes) and optionally `link`
                            (dict: local label -> global KB id)
  concepts.py               optional; defines register(kb) for your own
                            general entries (runs first, so your wording wins)
  rendered/                 generated Markdown per source (git-ignored)
  kb/                       the knowledge base (committed)
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .claims import Status
from .kb import KnowledgeBase, import_notes
from .render import to_markdown

SOURCE_DIRS = ("papers", "books")


def load_module(path: Path):
    name = f"_scaffold_src_{path.parent.name}_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def discover(root: Path) -> list[Path]:
    return [p for d in SOURCE_DIRS for p in sorted((root / d).glob("*.py"))
            if not p.name.startswith("_")]


@dataclass
class Report:
    statuses: dict[str, dict[str, str]] = field(default_factory=dict)   # file -> label -> status
    errors: dict[str, str] = field(default_factory=dict)
    broken_links: dict[str, list[str]] = field(default_factory=dict)

    @property
    def failed(self):
        return [(f, l) for f, d in self.statuses.items() for l, s in d.items()
                if s == Status.FAILED.value]

    def summary(self) -> str:
        L = []
        for f, d in self.statuses.items():
            L.append(f)
            L += [f"  {lbl:<14} {st}" for lbl, st in d.items()]
        for f, err in self.errors.items():
            L.append(f"{f}\n  ERROR: {err}")
        if self.broken_links:
            L.append("Broken links: " + str(self.broken_links))
        L.append(f"{len(self.failed)} failed, {len(self.errors)} errors")
        return "\n".join(L)


def check_file(path: Path):
    mod = load_module(path)
    n = getattr(mod, "notes", None)
    if n is None:
        raise AttributeError("file defines no module-level `notes`")
    n.check_all()
    return mod, n


def build(root=".", kb_dir="kb", rendered_dir="rendered", files=None) -> Report:
    root = Path(root).resolve()
    kb = KnowledgeBase(root / kb_dir)
    out = root / rendered_dir
    out.mkdir(exist_ok=True)
    report = Report()

    concepts = root / "concepts.py"
    if concepts.exists():
        load_module(concepts).register(kb)

    for path in files or discover(root):
        rel = path.relative_to(root).as_posix()
        try:
            mod, n = check_file(path)
        except Exception as exc:                       # keep building the rest
            report.errors[rel] = f"{type(exc).__name__}: {exc}"
            continue
        report.statuses[rel] = {lbl: c.status.value for lbl, c in n.claims.items()}
        (out / f"{path.stem}.md").write_text(to_markdown(n), encoding="utf-8")
        import_notes(kb, n, notes_file=rel, link=getattr(mod, "link", None))

    kb.write_index()
    report.broken_links = kb.broken_links()
    return report
