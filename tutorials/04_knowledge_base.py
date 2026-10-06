"""
Tutorial 4 — the central knowledge base: import, link, merge, query.
Works in a temporary folder, so your real kb/ is untouched.

Run:  python tutorials/04_knowledge_base.py
"""
import tempfile
from pathlib import Path

import sympy as sp

from _lib import lib, section, show

tmp = Path(tempfile.mkdtemp(prefix="kb-tutorial-"))
kb = lib.KnowledgeBase(tmp / "kb")

section("1. Your own entry (curated: imports never overwrite its wording)")
kb.add("ito-isometry", "theorem", "Itô isometry",
       statement="E[(int H dW)^2] = E[int H^2 dt] for suitable H",
       tags=["stochastic-calculus"])
show("curated", kb["ito-isometry"].curated)

section("2. A textbook and two papers, linked to shared ids")
book = lib.BookNotes("Book-A", "A textbook", "author", 2010)
with book.section("4.3", "Itô integral"):
    book.claim("Thm 4.3.1", "Itô isometry for simple integrands")
    book.exercise("Ex 4.3.2", "Compute E[(int_0^t W dW)^2]")
import_book = dict(link={"Thm 4.3.1": "ito-isometry"})

p1 = lib.PaperNotes("Paper-1", "Variance swaps", "someone", 2019)
p1.claim("Prop 2", "fair variance strike via the isometry", depends_on=["iso"])
p1.claim("Cor 3", "replication by a log contract", depends_on=["Prop 2"])

p2 = lib.PaperNotes("Paper-2", "Rough volatility", "someone else", 2022)
p2.claim("Lemma 1", "a different use of the isometry", depends_on=["iso"])

lib.import_notes(kb, book, notes_file="books/book_a.py", **import_book)
lib.import_notes(kb, p1, notes_file="papers/p1.py", link={"iso": "ito-isometry"})
lib.import_notes(kb, p2, notes_file="papers/p2.py", link={"iso": "ito-isometry"})

e = kb["ito-isometry"]
show("title kept", e.title)
show("sources", [f"{s['paper']} {s['label']}" for s in e.sources])

section("3. Queries")
show("theorems", [x.id for x in kb.find(kind="theorem")])
show("from Paper-1", [x.id for x in kb.find(paper="Paper-1")])
show("open exercises", [x.id for x in kb.find(kind="exercise", status="open")])
show("text 'replication'", [x.id for x in kb.find(text="replication")])

section("4. Impact analysis: what relies on the isometry?")
for dep in kb.dependents("ito-isometry"):
    show("  ↳", dep)
print("  -> if you find a gap in the theorem's hypotheses, these inherit it.")

section("5. SymPy expressions round-trip exactly, assumptions included")
s = sp.Symbol("sigma", positive=True)
kb.add("vol-scaling", "definition", "variance scaling", expr=sp.sqrt(s**2 * 4))
reloaded = lib.KnowledgeBase(tmp / "kb")["vol-scaling"].sympy
show("stored then reloaded", reloaded)
show("positivity survived", next(iter(reloaded.free_symbols)).is_positive)

section("6. Health checks")
p1.claim("Cor 4", "cites something not in the KB yet", depends_on=["girsanov"])
lib.import_notes(kb, p1, link={"iso": "ito-isometry"})
show("broken links", kb.broken_links())
show("index written to", kb.write_index())

section("7. What an entry looks like on disk")
print((tmp / "kb" / "theorem" / "ito-isometry.md").read_text(encoding="utf-8"))
