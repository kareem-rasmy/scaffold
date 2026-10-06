"""Category layer: thin helpers over sympy.categories plus functors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from sympy.categories import (
    CompositeMorphism, Diagram, DiagramGrid, IdentityMorphism, Object,
    XypicDiagramDrawer,
)


def morphism_name(m) -> str:
    """Short name: composites written g∘f, identities id_A."""
    if isinstance(m, IdentityMorphism):
        return f"id_{m.domain.name}"
    if isinstance(m, CompositeMorphism):
        return "∘".join(morphism_name(c) for c in reversed(m.components))
    return m.name


@dataclass
class Functor:
    """
    F: C -> D, specified on generators.
      compose(g_img, f_img) -> image of g∘f   (g after f)
      identity(obj_img)     -> image of an identity
      equal(a, b)           -> bool
    Composites are mapped by functoriality.
    """
    name: str
    on_objects: dict
    on_morphisms: dict
    compose: Callable
    identity: Callable
    equal: Callable

    def __call__(self, m):
        if isinstance(m, Object):
            return self.on_objects[m]
        if isinstance(m, IdentityMorphism):
            return self.identity(self.on_objects[m.domain])
        if isinstance(m, CompositeMorphism):
            img = self(m.components[0])
            for comp in m.components[1:]:
                img = self.compose(self(comp), img)
            return img
        return self.on_morphisms[m]


def to_xypic(d: Diagram) -> str:
    return XypicDiagramDrawer().draw(d, DiagramGrid(d))


def describe_diagram(d: Diagram, name="", meaning="", object_meanings=None,
                     commutations=(), show_identities=False) -> str:
    """Readable text summary: objects, hom-sets, commutativity claims, layout.
    `commutations` is an iterable of (label, path1, path2, status_str)."""
    object_meanings = object_meanings or {}
    objs = sorted(d.objects, key=lambda o: o.name)
    L = [f"Diagram '{name}': {meaning}", "", "Objects:"]
    L += [f"  {o.name:<6} {object_meanings.get(o.name, '')}" for o in objs]
    L += ["", "Hom-sets (premises):"]
    for A in objs:
        for B in objs:
            prem, concl = d.hom(A, B)
            ms = [m for m in prem if show_identities or not isinstance(m, IdentityMorphism)]
            if ms:
                L.append(f"  Hom({A.name}, {B.name}) = {{{', '.join(sorted(map(morphism_name, ms)))}}}")
            if concl:
                L.append(f"  conclusions {A.name} -> {B.name}: {', '.join(map(morphism_name, concl))}")
    rel = [c for c in commutations if c[1] in d.premises or c[2] in d.premises]
    if rel:
        L += ["", "Commutativity claims:"]
        L += [f"  [{st}] {lbl}: {morphism_name(p1)} = {morphism_name(p2)}" for lbl, p1, p2, st in rel]
    g = DiagramGrid(d)
    w = max(len(o.name) for o in d.objects) + 4
    L += ["", "Layout:"]
    for i in range(g.height):
        L.append("  " + "".join((g[i, j].name if g[i, j] else ".").ljust(w) for j in range(g.width)))
    return "\n".join(L)
