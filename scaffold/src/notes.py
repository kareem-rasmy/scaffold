"""PaperNotes: structured, checkable notes for one paper."""
from __future__ import annotations

import sympy as sp
from sympy.categories import Diagram, NamedMorphism, Object

from .category import Functor, describe_diagram, to_xypic
from .claims import Claim, Status, check_residual


class PaperNotes:
    source_type = "paper"

    def __init__(self, key, title, authors, year, source=""):
        self.key, self.title, self.authors, self.year, self.source = key, title, authors, year, source
        self.symbols: dict[str, tuple] = {}
        self.defs: dict[str, tuple[sp.Expr, str]] = {}
        self.claims: dict[str, Claim] = {}
        self.objects: dict[str, tuple[Object, str]] = {}
        self.morphisms: dict[str, tuple[NamedMorphism, str]] = {}
        self.diagrams: dict[str, tuple[Diagram, str]] = {}
        self.commutations: list[tuple] = []          # (label, path1, path2, statement)
        self.questions: list[str] = []
        self.current_section = ""
        self.where: dict[str, str] = {}              # name -> location

    # ---- notation & definitions -------------------------------------------
    def sym(self, name, meaning, latex=None, **assumptions):
        s = sp.Symbol(latex or name, **assumptions)
        self.symbols[name] = (s, meaning)
        return s

    def func(self, name, meaning, latex=None):
        f = sp.Function(latex or name)
        self.symbols[name] = (f, meaning)
        return f

    def define(self, name, expr, meaning):
        self.defs[name] = (expr, meaning)
        self.where[name] = self.current_section
        return expr

    # ---- claims -------------------------------------------------------------
    def claim(self, label, statement, residual=None, depends_on=(), note="", kind=None):
        c = Claim(label, statement, residual, list(depends_on), note=note, kind=kind,
                  where=self.current_section)
        if residual is None:
            c.status = Status.OPEN
        self.claims[label] = c
        return c

    def _plain_symbols(self):
        return [s for s, _ in self.symbols.values() if isinstance(s, sp.Symbol)]

    def check(self, label, n_numeric=20, simplifier=sp.simplify):
        c = self.claims[label]
        if c.residual is None:
            return c.status                  # open / stated / set by a functor check
        c.status, extra = check_residual(c.residual, self._plain_symbols(), n_numeric, simplifier)
        if extra:
            c.note = (c.note + " | " + extra).strip(" |")
        return c.status

    def check_all(self, **kw):
        return {lbl: self.check(lbl, **kw) for lbl in self.claims}

    # ---- category layer -----------------------------------------------------
    def obj(self, name, meaning):
        o = Object(name)
        self.objects[name] = (o, meaning)
        self.where[name] = self.current_section
        return o

    def mor(self, name, dom, cod, meaning):
        m = NamedMorphism(dom, cod, name)
        self.morphisms[name] = (m, meaning)
        self.where[name] = self.current_section
        return m

    def diagram(self, name, premises, conclusions=None, meaning=""):
        d = Diagram(premises, conclusions or {})
        self.diagrams[name] = (d, meaning)
        return d

    def commutes(self, label, path1, path2, statement):
        if path1.domain != path2.domain or path1.codomain != path2.codomain:
            raise ValueError("paths must be parallel")
        self.commutations.append((label, path1, path2, statement))
        self.claim(label, statement)

    def check_commutation(self, label, F: Functor):
        for lbl, p1, p2, _ in self.commutations:
            if lbl == label:
                c = self.claims[label]
                c.status = Status.VERIFIED if F.equal(F(p1), F(p2)) else Status.FAILED
                c.note = f"checked under functor {F.name}"
                return c.status
        raise KeyError(label)

    def describe(self, name, show_identities=False):
        d, meaning = self.diagrams[name]
        comms = [(l, p1, p2, self.claims[l].status.value) for l, p1, p2, _ in self.commutations]
        return describe_diagram(d, name, meaning, {n: m for n, (_, m) in self.objects.items()},
                                comms, show_identities)

    def xypic(self, name):
        return to_xypic(self.diagrams[name][0])
