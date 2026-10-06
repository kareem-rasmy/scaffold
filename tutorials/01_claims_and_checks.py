"""
Tutorial 1 — symbols, definitions, claims, and how they get checked.

Run:  python tutorials/01_claims_and_checks.py
"""
import sympy as sp

from _lib import lib, section, show

n = lib.PaperNotes(key="TUT-1", title="Tutorial 1", authors="you", year=2026)

section("1. Symbols carry assumptions — and assumptions change what is provable")
x_pos = n.sym("x", "a positive quantity", positive=True)
x_real = sp.Symbol("x", real=True)                      # not registered, just for contrast
show("sqrt(x^2) with x > 0", sp.sqrt(x_pos**2))
show("sqrt(x^2) with x real", sp.sqrt(x_real**2))
print("  -> state the paper's hypotheses (positive=True etc.) or simplify can't use them.")

section("2. Definitions are named SymPy expressions")
S     = n.sym("S", "spot", positive=True)
K     = n.sym("K", "strike", positive=True)
r     = n.sym("r", "rate", positive=True)
sigma = n.sym("sigma", "volatility", latex="sigma", positive=True)
tau   = n.sym("tau", "time to maturity", latex="tau", positive=True)

N  = lambda z: (1 + sp.erf(z / sp.sqrt(2))) / 2
d1 = n.define("d1", (sp.log(S/K) + (r + sigma**2/2)*tau) / (sigma*sp.sqrt(tau)), "eq. (1)")
d2 = n.define("d2", d1 - sigma*sp.sqrt(tau), "eq. (1)")
C  = n.define("C", S*N(d1) - K*sp.exp(-r*tau)*N(d2), "call, eq. (2)")
P  = n.define("P", K*sp.exp(-r*tau)*N(-d2) - S*N(-d1), "put, eq. (3)")
show("d2", d2)

section("3. A claim = a residual that should be identically zero")
n.claim("Prop 1", "put-call parity: C - P = S - K e^{-r tau}",
        residual=C - P - (S - K*sp.exp(-r*tau)), depends_on=["C", "P"])

vega = sp.diff(C, sigma)
phi = lambda z: sp.exp(-z**2/2) / sp.sqrt(2*sp.pi)
n.claim("Lemma 2", "vega = S phi(d1) sqrt(tau)",
        residual=vega - S*phi(d1)*sp.sqrt(tau), depends_on=["C"])

# A typo, as you might copy it from a paper: tau instead of sqrt(tau)
n.claim("Lemma 2 (typo)", "vega = S phi(d1) tau",
        residual=vega - S*phi(d1)*tau, depends_on=["C"])

n.claim("Thm 3", "the hedge is self-financing", note="proof idea only, nothing to compute")

for lbl, st in n.check_all().items():
    show(lbl, st.value)
print("  -> the typo is caught: FAILED means a mistake in the source or in your reading.")

section("4. When simplify gives up, numeric spot-checks still give evidence")
a = n.sym("a", "angle", real=True)
n.claim("Identity", "sin^2 + cos^2 = 1", residual=sp.sin(a)**2 + sp.cos(a)**2 - 1)
show("with simplify", n.check("Identity").value)
show("with no simplification", n.check("Identity", simplifier=lambda e: e).value)
print(f"  note: {n.claims['Identity'].note}")
print("  -> 'numeric-only' = passed at random points; treat as strong evidence, not proof.")

section("5. Everything renders to Markdown (open it with Ctrl+Shift+V)")
print(lib.to_markdown(n).split("## Claims")[1])
