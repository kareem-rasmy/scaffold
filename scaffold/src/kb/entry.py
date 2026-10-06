"""One knowledge-base entry and its on-disk format (YAML front matter + Markdown)."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

import sympy as sp
import yaml

KINDS = {"symbol", "definition", "theorem", "lemma", "proposition", "corollary", "claim",
         "object", "morphism", "question", "example", "exercise", "remark", "concept"}


@dataclass
class Entry:
    id: str                                   # global, stable id
    kind: str
    title: str
    statement: str = ""
    expr: str | None = None                   # srepr of a SymPy expression
    status: str = "stated"
    sources: list[dict] = field(default_factory=list)   # [{"paper": key, "label": ..., "where": ...}]
    depends_on: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    domain: str | None = None                 # morphisms only
    codomain: str | None = None
    checked_in: str | None = None             # notes file that runs the check
    curated: bool = False                     # hand-written: imports never overwrite title/statement
    notes: str = ""                           # Markdown body

    @property
    def sympy(self):
        return None if self.expr is None else sp.sympify(self.expr)

    def set_sympy(self, e):
        self.expr = None if e is None else sp.srepr(e)

    def to_text(self) -> str:
        meta = {k: v for k, v in asdict(self).items() if k != "notes" and v not in (None, [], "", False)}
        if self.expr is not None:
            meta["latex"] = sp.latex(self.sympy)          # display only; ignored on load
        front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=100)
        body = self.notes or ""
        if self.expr is not None:
            body = f"$$\n{meta['latex']}\n$$\n\n" + body
        return f"---\n{front}---\n\n{body}".rstrip() + "\n"

    @classmethod
    def from_text(cls, text: str) -> "Entry":
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        if not m:
            raise ValueError("missing YAML front matter")
        meta = yaml.safe_load(m.group(1))
        meta.pop("latex", None)
        body = m.group(2)
        if meta.get("expr") is not None:
            body = re.sub(r"^\s*\$\$\n.*?\n\$\$\n\n?", "", body, count=1, flags=re.S)
        return cls(**meta, notes=body.strip())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
