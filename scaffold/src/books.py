"""BookNotes: PaperNotes plus sections, examples, remarks and exercises."""
from __future__ import annotations

from contextlib import contextmanager

from .claims import Status
from .notes import PaperNotes


class BookNotes(PaperNotes):
    source_type = "book"

    def __init__(self, key, title, authors, year, edition="", source=""):
        super().__init__(key, title, authors, year, source)
        self.edition = edition
        self.sections: list[tuple[str, str]] = []

    @contextmanager
    def section(self, number, title=""):
        """with book.section("5.2", "Girsanov"): ...  — stamps everything inside."""
        self.current_section = f"§{number}"
        self.sections.append((number, title))
        try:
            yield self
        finally:
            self.current_section = ""

    def example(self, label, statement, residual=None, depends_on=(), note=""):
        return self.claim(label, statement, residual, depends_on, note, kind="example")

    def remark(self, label, statement, depends_on=(), note=""):
        c = self.claim(label, statement, None, depends_on, note, kind="remark")
        c.status = Status.STATED
        return c

    def exercise(self, label, statement, solution=None, depends_on=(), note=""):
        """`solution`: residual encoding your answer. None -> open (a to-do)."""
        return self.claim(label, statement, solution, depends_on, note, kind="exercise")

    def todo(self):
        return [c.label for c in self.claims.values()
                if c.kind == "exercise" and c.status in (Status.OPEN, Status.FAILED)]
