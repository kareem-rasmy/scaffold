"""Copy a PaperNotes / BookNotes object into the knowledge base."""
from __future__ import annotations

import sympy as sp

from ..render import compact_definitions

from .entry import slug
from .store import KnowledgeBase

_PREFIXES = (("thm", "theorem"), ("theorem", "theorem"), ("lem", "lemma"),
             ("prop", "proposition"), ("cor", "corollary"))


def _kind_from_label(label: str) -> str:
    return next((k for p, k in _PREFIXES if label.lower().startswith(p)), "claim")


def import_notes(kb: KnowledgeBase, n, notes_file=None, link=None, include_symbols=False):
    """
    Labels become ids "<sourcekey>.<label>" unless `link` maps them to a global
    id — that is how one theorem from several sources becomes one entry.
    Claims are catalogued (status, deps, pointer to `notes_file`); residuals stay
    in the notes file, which is the executable source of truth.
    """
    link = link or {}
    key = slug(n.key)

    def gid(label):
        return link.get(label, f"{key}.{slug(label)}")

    def src(label, where=""):
        where = where or n.where.get(label, "")
        return [{"paper": n.key, "label": label, **({"where": where} if where else {})}]

    common = dict(owner=n.key)
    if include_symbols:
        for name, (s, meaning) in n.symbols.items():
            kb.add(gid(name), "symbol", name, statement=meaning,
                   expr=s if isinstance(s, sp.Symbol) else None, sources=src(name), **common)
    short = compact_definitions(n)        # d2 = d1 - sigma*sqrt(tau), not the expansion
    for name, (e, meaning) in n.defs.items():
        kb.add(gid(name), "definition", name, statement=meaning, expr=e, compact=short[name],
               sources=src(name), **common)
    for name, (_, meaning) in n.objects.items():
        kb.add(gid(name), "object", name, statement=meaning, sources=src(name), **common)
    for name, (m, meaning) in n.morphisms.items():
        kb.add(gid(name), "morphism", name, statement=meaning, sources=src(name),
               domain=gid(m.domain.name), codomain=gid(m.codomain.name), **common)
    for label, c in n.claims.items():
        kb.add(gid(label), c.kind or _kind_from_label(label), label, statement=c.statement,
               status=c.status.value, checked_in=notes_file,
               depends_on=[gid(d) for d in c.depends_on], sources=src(label, c.where),
               notes=c.note, **common)
    for i, q in enumerate(n.questions, 1):
        kb.add(f"{key}.q{i}", "question", f"{n.key} question {i}", statement=q, status="open",
               sources=[{"paper": n.key, "label": "reading"}], **common)
