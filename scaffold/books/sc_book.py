"""Notes: a stochastic calculus textbook (placeholder key and numbering)."""
import sympy as sp

from scaffold.src import BookNotes

notes = b = BookNotes(key="SC-book", title="Stochastic Calculus (textbook)",
                      authors="(author)", year=2004, edition="1st")

link = {"Thm 5.2.3": "girsanov-theorem", "Z": "rn-density-girsanov"}

t     = b.sym("t", "time", positive=True)
theta = b.sym("theta", "Girsanov kernel (constant)", latex="theta", real=True)
sigma = b.sym("sigma", "volatility", latex="sigma", positive=True)
x     = b.sym("x", "integration variable", real=True)
W     = b.sym("W_t", "Brownian motion at time t", real=True)


def phi(y, var):
    """N(0, var) density."""
    return sp.exp(-y**2 / (2*var)) / sp.sqrt(2*sp.pi*var)


with b.section("3.2", "Brownian motion"):
    b.define("mgf_W", sp.exp(sigma**2 * t / 2), "E[exp(sigma W_t)]")
    b.exercise("Ex 3.2.4", "Compute E[exp(sigma W_t)]",
               solution=sp.integrate(sp.exp(sigma*x)*phi(x, t), (x, -sp.oo, sp.oo))
                        - sp.exp(sigma**2*t/2))
    b.exercise("Ex 3.2.7", "Show W_t^2 - t is a martingale")     # to do

with b.section("5.2", "Girsanov's theorem"):
    b.define("Z", sp.exp(-theta*W - theta**2*t/2), "Radon–Nikodym density process")
    b.example("Ex 5.2.1", "Z has expectation 1 under P",
              residual=sp.integrate(sp.exp(-theta*x - theta**2*t/2)*phi(x, t),
                                    (x, -sp.oo, sp.oo)) - 1, depends_on=["Z"])
    b.claim("Thm 5.2.3", "Under dQ = Z_T dP, W_t + theta t is a Q-Brownian motion",
            depends_on=["Z"])
    b.remark("Rmk 5.2.4", "For non-constant theta, Novikov's condition makes Z a true martingale")
