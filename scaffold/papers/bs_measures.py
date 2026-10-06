"""Notes: Black-Scholes pricing and changes of numeraire (example paper)."""
import sympy as sp

from scaffold.src import Functor, PaperNotes, sympy_equal

notes = n = PaperNotes(
    key="BS-numeraire",
    title="Black-Scholes pricing and changes of numeraire",
    authors="(example)", year=2026,
    source="Sec. 2 (model), Sec. 3 (pricing PDE), Sec. 4 (measure changes)",
)

# Local label -> global KB id, for concepts shared with other sources.
link = {
    "P": "measure-P", "Q": "measure-Q",
    "girsanov": "change-P-to-Q",
    "d1": "bs-d1", "d2": "bs-d2", "C": "bs-call",
}

# ---- 1. Notation -----------------------------------------------------------
S     = n.sym("S", "spot price", positive=True)
K     = n.sym("K", "strike", positive=True)
r     = n.sym("r", "risk-free rate (constant)", positive=True)
sigma = n.sym("sigma", "volatility", latex="sigma", positive=True)
tau   = n.sym("tau", "time to maturity T - t", latex="tau", positive=True)
T     = n.sym("T", "maturity", positive=True)
theta = n.sym("theta", "market price of risk (mu - r)/sigma", latex="theta", real=True)
W     = n.sym("W_T", "P-Brownian motion at T", real=True)

# ---- 2. Definitions --------------------------------------------------------
N  = lambda x: (1 + sp.erf(x / sp.sqrt(2))) / 2
d1 = n.define("d1", (sp.log(S/K) + (r + sigma**2/2)*tau) / (sigma*sp.sqrt(tau)), "eq. (3.2)")
d2 = n.define("d2", d1 - sigma*sp.sqrt(tau), "eq. (3.2)")
C  = n.define("C", S*N(d1) - K*sp.exp(-r*tau)*N(d2), "call price, eq. (3.3)")

# ---- 3. Claims -------------------------------------------------------------
pde = -sp.diff(C, tau) + r*S*sp.diff(C, S) + sigma**2*S**2/2*sp.diff(C, S, 2) - r*C
n.claim("(3.1)", "C solves the BS PDE in (S, tau)", residual=pde, depends_on=["C"])
delta = n.define("Delta", sp.diff(C, S), "delta")
n.claim("Lemma 3.1", "Delta = N(d1)", residual=delta - N(d1), depends_on=["C"])
n.claim("Prop 3.2", "Put-call parity",
        note="TODO: define P and add residual C - P - S + K e^{-r tau}")

# ---- 4. Categorical skeleton -----------------------------------------------
P  = n.obj("P",  "physical measure")
Q  = n.obj("Q",  "risk-neutral measure (bank-account numeraire)")
QS = n.obj("QS", "share measure (stock numeraire)")

g_PQ  = n.mor("girsanov", P, Q, "Girsanov with kernel theta, eq. (4.1)")
g_QQS = n.mor("numeraire", Q, QS, "numeraire change B -> S, eq. (4.3)")
g_PQS = n.mor("direct", P, QS, "paper's direct density, eq. (4.5)")

n.diagram("measures", [g_PQ, g_QQS, g_PQS], meaning="Sec. 4 measure changes")
n.commutes("Thm 4.2", g_QQS * g_PQ, g_PQS,
           "going P -> Q -> QS equals the direct change P -> QS")

# Functor into densities (composition = multiplication), all in terms of W = W^P_T.
WQ = W + theta*T
F = Functor(
    name="RN-density",
    on_objects={P: "*", Q: "*", QS: "*"},
    on_morphisms={
        g_PQ:  sp.exp(-theta*W - theta**2*T/2),
        g_QQS: sp.exp(sigma*WQ - sigma**2*T/2),
        g_PQS: sp.exp((sigma - theta)*W - (sigma - theta)**2*T/2),
    },
    compose=lambda g, f: g*f,
    identity=lambda _: sp.Integer(1),
    equal=sympy_equal,
)
n.check_commutation("Thm 4.2", F)

# ---- 5. Questions ----------------------------------------------------------
n.questions.append("Does Sec. 5 need theta deterministic, or just Novikov?")
