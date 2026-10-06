"""Claims and the machinery that checks them."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

import sympy as sp


class Status(Enum):
    STATED = "stated"            # recorded, not checked
    VERIFIED = "verified"        # symbolic check passed
    NUMERIC = "numeric-only"     # symbolic check inconclusive, numeric spot-checks passed
    FAILED = "FAILED"            # a check found a counterexample
    OPEN = "open"                # no mechanical check (yet)


@dataclass
class Claim:
    label: str                         # the source's own label: "Prop 2.3", "(4.1)"
    statement: str                     # in your words
    residual: sp.Expr | None = None    # should be identically 0
    depends_on: list[str] = field(default_factory=list)
    status: Status = Status.STATED
    note: str = ""
    kind: str | None = None            # theorem / lemma / example / exercise / remark ...
    where: str = ""                    # "§5.2", "p. 41"


def sample_value(s: sp.Symbol) -> sp.Float:
    """Random test value respecting the symbol's sign assumption."""
    if s.is_positive:
        return sp.Float(random.uniform(0.1, 3.0))
    return sp.Float(random.uniform(-2.0, 2.0))


def numerically_zero(expr, symbols, n=20, tol=1e-9) -> bool:
    for _ in range(n):
        subs = {s: sample_value(s) for s in symbols if s in expr.free_symbols}
        if abs(complex(sp.N(expr.subs(subs)))) > tol:
            return False
    return True


def check_residual(residual, symbols, n_numeric=20, simplifier=sp.simplify):
    """Return (Status, note) for a residual that should vanish."""
    if residual is None:
        return Status.OPEN, ""
    r = simplifier(residual)
    if r == 0:
        return Status.VERIFIED, ""
    if numerically_zero(residual, symbols, n_numeric):
        return Status.NUMERIC, f"residual simplified to: {r}"
    return Status.FAILED, ""


def sympy_equal(a, b) -> bool:
    """Equality test for functor targets made of SymPy expressions."""
    return sp.simplify(a - b) == 0
