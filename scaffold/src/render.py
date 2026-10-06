"""Markdown rendering of a notes object."""
import sympy as sp


def compact_definitions(n):
    """Rewrite each definition in terms of the definitions before it,
    so C shows up as S N(d1) - ... instead of fully expanded."""
    out, names = {}, list(n.defs)
    for i, k in enumerate(names):
        e = n.defs[k][0]
        for prev in reversed(names[:i]):
            e = e.subs(n.defs[prev][0], sp.Symbol(prev))
        out[k] = e
    return out


def to_markdown(n, compact=True) -> str:
    title = n.title + (f" ({n.edition} ed.)" if getattr(n, "edition", "") else "")
    L = [f"# {title}", f"*{n.authors} ({n.year})* — {n.source_type} `{n.key}`", "", n.source, ""]
    L += ["## Notation", "", "| symbol | meaning |", "|---|---|"]
    L += [f"| ${sp.latex(s)}$ | {m} |" for s, m in n.symbols.values()]
    if n.defs:
        L += ["", "## Definitions", ""]
        shown = compact_definitions(n) if compact else {k: e for k, (e, _) in n.defs.items()}
        for k, (_, m) in n.defs.items():
            loc = f" {n.where[k]}" if n.where.get(k) else ""
            L += [f"**{k}**{loc} — {m}", "", "$$", sp.latex(shown[k]), "$$", ""]
    if n.objects:
        L += ["", "## Categorical skeleton", "", "Objects:", ""]
        L += [f"- `{k}`: {m}" for k, (_, m) in n.objects.items()]
        L += ["", "Morphisms:", ""]
        L += [f"- `{k}: {o.domain.name} → {o.codomain.name}`: {m}" for k, (o, m) in n.morphisms.items()]
    L += ["", "## Claims", "", "| where | label | kind | status | statement | depends on | note |",
          "|---|---|---|---|---|---|---|"]
    L += [f"| {c.where} | {c.label} | {c.kind or ''} | {c.status.value} | {c.statement} "
          f"| {', '.join(c.depends_on)} | {c.note} |" for c in n.claims.values()]
    if n.questions:
        L += ["", "## Open questions", ""] + [f"- {q}" for q in n.questions]
    if getattr(n, "sections", None):
        L += ["", "## Sections read", ""] + [f"- §{num} {t}" for num, t in n.sections]
    return "\n".join(L) + "\n"
