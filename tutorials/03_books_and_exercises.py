"""
Tutorial 3 — textbook notes: sections, examples, remarks, exercises.

Run:  python tutorials/03_books_and_exercises.py
"""
import sympy as sp

from _lib import lib, section, show

b = lib.BookNotes(key="TUT-BOOK", title="Tutorial textbook", authors="you",
                  year=2026, edition="2nd")

t = b.sym("t", "time", positive=True)
x = b.sym("x", "integration variable", real=True)
mu = b.sym("mu", "drift", latex="mu", real=True)
sigma = b.sym("sigma", "volatility", latex="sigma", positive=True)
density = lambda y, var: sp.exp(-y**2/(2*var)) / sp.sqrt(2*sp.pi*var)   # N(0, var)
E = lambda g: sp.integrate(g(x)*density(x, t), (x, -sp.oo, sp.oo))     # E[g(W_t)]

section("1. Sections stamp every entry with its location")
with b.section("2.1", "Brownian motion"):
    b.define("var_W", t, "Var(W_t) = t")
    b.example("Ex 2.1.1", "E[W_t^2] = t", residual=E(lambda w: w**2) - t)
    b.remark("Rmk 2.1.2", "W has independent, stationary increments")

with b.section("2.3", "Geometric Brownian motion"):
    b.define("S_T", sp.exp((mu - sigma**2/2)*t + sigma*x), "GBM at t, with W_t = x")

for name in b.defs:
    show(f"definition {name}", f"recorded in {b.where[name]}")

section("2. Exercises: your solution is a residual; no solution = to-do")
with b.section("2.1", "Brownian motion"):
    b.exercise("Ex 2.1.5", "E[W_t^4] = 3 t^2",
               solution=E(lambda w: w**4) - 3*t**2)
    b.exercise("Ex 2.1.6", "E[W_t^3] = t^3   (my first attempt)",
               solution=E(lambda w: w**3) - t**3)
with b.section("2.3", "Geometric Brownian motion"):
    b.exercise("Ex 2.3.2", "E[S_t] = exp(mu t)",
               solution=E(lambda w: sp.exp((mu - sigma**2/2)*t + sigma*w)) - sp.exp(mu*t))
    b.exercise("Ex 2.3.4", "Show S is a martingale iff mu = 0")    # not attempted

for lbl, st in b.check_all().items():
    c = b.claims[lbl]
    show(f"{c.where} {lbl} [{c.kind}]", st.value)

section("3. Your to-do list")
show("open or failed exercises", b.todo())
print("  -> Ex 2.1.6 FAILED: odd moments vanish; fix the solution to 0 and rerun.")

section("4. Rendered notes include a 'sections read' trail")
print(lib.to_markdown(b).split("## Sections read")[1])
