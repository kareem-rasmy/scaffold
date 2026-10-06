"""The knowledge base: a folder of Entry files, plus queries."""
from __future__ import annotations

from pathlib import Path

from .entry import KINDS, Entry


class KnowledgeBase:
    def __init__(self, root="kb"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.entries: dict[str, Entry] = {}
        for p in sorted(self.root.glob("*/*.md")):
            e = Entry.from_text(p.read_text(encoding="utf-8"))
            self.entries[e.id] = e

    # ---- write ---------------------------------------------------------------
    def _path(self, e: Entry) -> Path:
        return self.root / e.kind / f"{e.id}.md"

    def save(self, e: Entry) -> Entry:
        if e.kind not in KINDS:
            raise ValueError(f"unknown kind {e.kind!r}; add it to KINDS if intended")
        old = self.entries.get(e.id)
        if old and old.kind != e.kind:
            self._path(old).unlink(missing_ok=True)
        p = self._path(e)
        p.parent.mkdir(exist_ok=True)
        p.write_text(e.to_text(), encoding="utf-8")
        self.entries[e.id] = e
        return e

    def add(self, id, kind, title, *, expr=None, compact=None, owner=None, **kw) -> Entry:
        """
        Create or merge.
        `owner` is the source key when called by an import, None when you call
        it yourself; entries you add yourself are marked `curated`.
        Lists (sources, depends_on, tags) are unioned. Title and statement:
          - curated entry (yours, or `curated: true` set by hand in the file):
            existing wording always wins
          - entry that came only from `owner`: re-importing replaces it
          - entry shared between sources: existing wording wins
        """
        new = Entry(id=id, kind=kind, title=title, **kw)
        new.curated = new.curated or owner is None
        new.set_sympy(expr, compact)
        old = self.entries.get(id)
        if old:
            for f in ("sources", "depends_on", "tags"):
                cur = getattr(old, f)
                setattr(new, f, cur + [x for x in getattr(new, f) if x not in cur])
            new.curated = new.curated or old.curated
            solely_owned = owner and old.sources and all(s["paper"] == owner for s in old.sources)
            if old.curated or not solely_owned:
                new.title = old.title or new.title
                new.statement = old.statement or new.statement
                if old.kind == "theorem" and new.kind == "claim":
                    new.kind = old.kind
            if not new.expr:
                new.expr, new.symbols, new.compact = old.expr, old.symbols, old.compact
            for f in ("statement", "domain", "codomain", "checked_in", "notes"):
                if not getattr(new, f):
                    setattr(new, f, getattr(old, f))
            if new.status == "stated" and old.status != "stated":
                new.status = old.status
        return self.save(new)

    # ---- read / query --------------------------------------------------------
    def __getitem__(self, id) -> Entry:
        return self.entries[id]

    def __contains__(self, id) -> bool:
        return id in self.entries

    def find(self, kind=None, tag=None, paper=None, status=None, text=None) -> list[Entry]:
        out = []
        for e in self.entries.values():
            if kind and e.kind != kind:
                continue
            if tag and tag not in e.tags:
                continue
            if status and e.status != status:
                continue
            if paper and paper not in {s["paper"] for s in e.sources}:
                continue
            if text and text.lower() not in f"{e.title} {e.statement} {e.notes}".lower():
                continue
            out.append(e)
        return sorted(out, key=lambda e: (e.kind, e.id))

    def dependents(self, id) -> list[str]:
        """Everything that (transitively) relies on `id`."""
        seen, todo = set(), [id]
        while todo:
            cur = todo.pop()
            for e in self.entries.values():
                if cur in e.depends_on and e.id not in seen:
                    seen.add(e.id)
                    todo.append(e.id)
        return sorted(seen)

    def broken_links(self) -> dict[str, list[str]]:
        return {e.id: [d for d in e.depends_on if d not in self.entries]
                for e in self.entries.values() if any(d not in self.entries for d in e.depends_on)}

    def write_index(self, path=None) -> Path:
        path = Path(path or self.root / "INDEX.md")
        L = ["# Knowledge base index", ""]
        for kind in sorted({e.kind for e in self.entries.values()}):
            L += [f"## {kind}", "", "| id | title | status | sources |", "|---|---|---|---|"]
            for e in self.find(kind=kind):
                srcs = "; ".join(f"{s['paper']} {s['label']} {s.get('where', '')}".strip() for s in e.sources)
                L.append(f"| [{e.id}]({kind}/{e.id}.md) | {e.title} | {e.status} | {srcs} |")
            L.append("")
        path.write_text("\n".join(L), encoding="utf-8")
        return path
