import sympy as sp

from scaffold.src import BookNotes, KnowledgeBase, PaperNotes, import_notes


def test_roundtrip_with_assumptions(tmp_path):
    kb = KnowledgeBase(tmp_path)
    x = sp.Symbol("x", positive=True)
    kb.add("e", "definition", "e", expr=sp.exp(-x) * sp.erf(x), statement="σ → ∘")
    kb2 = KnowledgeBase(tmp_path)
    e = kb2["e"].sympy
    assert e == sp.exp(-x) * sp.erf(x)
    assert next(iter(e.free_symbols)).is_positive
    assert kb2["e"].statement == "σ → ∘"


def test_merge_rules(tmp_path):
    kb = KnowledgeBase(tmp_path)
    kb.add("thm", "theorem", "My wording", statement="mine")
    kb.add("thm", "claim", "Thm 1", statement="theirs", owner="P1",
           sources=[{"paper": "P1", "label": "Thm 1"}])
    e = kb["thm"]
    assert (e.title, e.statement, e.kind) == ("My wording", "mine", "theorem")
    assert e.sources[0]["paper"] == "P1"

    kb.add("own", "claim", "(1)", statement="v1", owner="P1",
           sources=[{"paper": "P1", "label": "(1)"}])
    kb.add("own", "claim", "(1)", statement="v2", owner="P1",
           sources=[{"paper": "P1", "label": "(1)"}])
    assert kb["own"].statement == "v2" and len(kb["own"].sources) == 1


def test_import_book_and_paper_link(tmp_path):
    kb = KnowledgeBase(tmp_path)
    b = BookNotes("Book", "b", "me", 2000)
    with b.section("1.1"):
        b.claim("Thm 1.1.1", "core theorem")
        b.exercise("Ex 1", "do it")
    p = PaperNotes("Pap", "p", "me", 2020)
    p.claim("Prop 2", "uses core", depends_on=["core"])
    import_notes(kb, b, link={"Thm 1.1.1": "core"})
    import_notes(kb, p, link={"core": "core"})
    assert kb["core"].kind == "theorem"
    assert kb["core"].sources[0]["where"] == "§1.1"
    assert kb.dependents("core") == ["pap.prop-2"]
    assert [e.id for e in kb.find(kind="exercise", status="open")] == ["book.ex-1"]
    assert kb.broken_links() == {}
    assert b.todo() == ["Ex 1"]
