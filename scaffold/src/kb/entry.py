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
    expr: str | None = None                   # readable SymPy expression, e.g. "d1 - sigma*sqrt(tau)" fully expanded
    symbols: dict = field(default_factory=dict)  # assumptions per symbol: {"sigma": "positive"}
    compact: str | None = None                # same expression in terms of other definitions (display)
    status: str = "stated"
    sources: list[dict] = field(default_factory=list)   # [{"paper": key, "label": ..., "where": ...}]
    depends_on: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    domain: str | None = None                 # morphisms only
    codomain: str | None = None
    checked_in: str | None = None             # notes file that runs the check
    curated: bool = False                     # hand-written: imports never overwrite title/statement
    notes: str = ""                           # Markdown body

    # ---- SymPy ---------------------------------------------------------------
    @property
    def sympy(self):
        if self.expr is None:
            return None
        return sp.sympify(self.expr, locals=_symbol_table(self.symbols))

    def set_sympy(self, e, compact=None):
        """Store `e` as readable text plus symbol assumptions. Falls back to
        srepr (exact but unreadable) in the rare case text doesn't round-trip."""
        self.compact = None if compact is None or compact == e else str(compact)
        if e is None:
            self.expr, self.symbols = None, {}
            return
        syms = set(e.free_symbols) | (set(compact.free_symbols) if self.compact else set())
        self.symbols = {s.name: _assumption_str(s) for s in
                        sorted(syms, key=lambda s: s.name) if isinstance(s, sp.Symbol)}
        self.expr = str(e)
        try:
            if self.sympy == e:
                return
        except Exception:
            pass
        self.expr, self.symbols = sp.srepr(e), {}

    def display_latex(self) -> str:
        shown = self.sympy
        if self.compact:
            shown = sp.sympify(self.compact, locals=_symbol_table(self.symbols))
        lhs = sp.latex(sp.Symbol(self.title)) if self.kind == "definition" else ""
        return (lhs + " = " if lhs else "") + sp.latex(shown)

    # ---- file format -----------------------------------------------------------
    def to_text(self) -> str:
        meta = {k: v for k, v in asdict(self).items()
                if k != "notes" and v not in (None, [], {}, "", False)}
        front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10**6)
        body = self.notes or ""
        if self.expr is not None:
            body = f"$$\n{self.display_latex()}\n$$\n\n" + body
        return f"---\n{front}---\n\n{body}".rstrip() + "\n"

    @classmethod
    def from_text(cls, text: str) -> "Entry":
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        if not m:
            raise ValueError("missing YAML front matter")
        meta = yaml.safe_load(m.group(1))
        meta.pop("latex", None)                    # written by older versions
        body = m.group(2)
        if meta.get("expr") is not None:           # drop the generated $$ block
            body = re.sub(r"^\s*\$\$\n.*?\n\$\$\n\n?", "", body, count=1, flags=re.S)
        e = cls(**meta, notes=body.strip())
        if e.expr is not None and not e.symbols and "Symbol(" in e.expr:
            e.set_sympy(e.sympy)                   # upgrade old srepr entries on load
        return e


def _assumption_str(s: sp.Symbol) -> str:
    orig = getattr(s, "_assumptions_orig", {}) or {}
    return ", ".join(k for k, v in orig.items() if v is True)


def _symbol_table(symbols: dict) -> dict:
    out = {}
    for name, a in (symbols or {}).items():
        kw = {k.strip(): True for k in (a or "").split(",") if k.strip()}
        out[name] = sp.Symbol(name, **kw)
    return out


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
