import shutil
from pathlib import Path

import scaffold
from scaffold.src.build import build
from scaffold.src.kb import KnowledgeBase

ROOT = Path(scaffold.__file__).resolve().parent


def test_build_examples(tmp_path):
    for d in ("papers", "books"):
        shutil.copytree(ROOT / d, tmp_path / d)
    shutil.copy(ROOT / "concepts.py", tmp_path)
    r = build(tmp_path)
    assert not r.errors and not r.failed, r.summary()
    kb = KnowledgeBase(tmp_path / "kb")
    assert kb["girsanov-theorem"].title == "Girsanov theorem"
    assert kb["change-P-to-Q"].domain == "measure-P"
    assert "change-P-to-Q" in kb.dependents("girsanov-theorem")
    assert (tmp_path / "rendered" / "bs_measures.md").exists()
    # idempotent: second build changes nothing
    before = {p: p.read_text(encoding="utf-8") for p in (tmp_path / "kb").rglob("*.md")}
    build(tmp_path)
    after = {p: p.read_text(encoding="utf-8") for p in (tmp_path / "kb").rglob("*.md")}
    assert before == after
