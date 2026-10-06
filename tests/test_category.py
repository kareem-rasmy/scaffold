import sympy as sp

from scaffold.src import Functor, PaperNotes, Status, sympy_equal


def triangle(direct_density):
    n = PaperNotes("T", "test", "me", 2026)
    a = n.sym("a", "a", real=True)
    A, B, C = n.obj("A", ""), n.obj("B", ""), n.obj("C", "")
    f, g, h = n.mor("f", A, B, ""), n.mor("g", B, C, ""), n.mor("h", A, C, "")
    n.diagram("tri", [f, g, h])
    n.commutes("comm", g * f, h, "g∘f = h")
    F = Functor("mult", {A: 0, B: 0, C: 0},
                {f: sp.exp(a), g: sp.exp(2*a), h: direct_density(a)},
                compose=lambda g_, f_: g_ * f_, identity=lambda _: 1, equal=sympy_equal)
    return n, F


def test_commutation_verified():
    n, F = triangle(lambda a: sp.exp(3*a))
    assert n.check_commutation("comm", F) == Status.VERIFIED
    assert "g∘f = h" in n.describe("tri") or "f∘" in n.describe("tri")


def test_commutation_failed():
    n, F = triangle(lambda a: sp.exp(4*a))
    assert n.check_commutation("comm", F) == Status.FAILED


def test_xypic_output():
    n, _ = triangle(lambda a: sp.exp(3*a))
    assert "\\xymatrix" in n.xypic("tri")
