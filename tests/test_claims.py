import sympy as sp

from scaffold.src import PaperNotes, Status


def make():
    n = PaperNotes("T", "test", "me", 2026)
    x = n.sym("x", "x", positive=True)
    return n, x


def test_verified_and_failed():
    n, x = make()
    n.claim("good", "(x+1)^2 expands", residual=(x + 1)**2 - (x**2 + 2*x + 1))
    n.claim("bad", "wrong", residual=(x + 1)**2 - (x**2 + 1))
    n.claim("open", "no check")
    st = n.check_all()
    assert st == {"good": Status.VERIFIED, "bad": Status.FAILED, "open": Status.OPEN}


def test_numeric_fallback():
    n, x = make()
    # identity that plain simplify may leave untouched -> still not FAILED
    n.claim("trig", "sin^2 + cos^2 = 1", residual=sp.sin(x)**2 + sp.cos(x)**2 - 1)
    assert n.check("trig", simplifier=lambda e: e) == Status.NUMERIC
