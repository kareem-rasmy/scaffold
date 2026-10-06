"""
Tutorial 2 — objects, morphisms, diagrams, and checking commutativity
with functors.

Run:  python tutorials/02_categories_and_functors.py
"""
import sympy as sp
from sympy.categories import IdentityMorphism

from _lib import lib, section, show

n = lib.PaperNotes(key="TUT-2", title="Tutorial 2", authors="you", year=2026)

section("1. Objects and morphisms; composition is written g * f (g after f)")
A = n.obj("A", "source space")
B = n.obj("B", "intermediate space")
C = n.obj("C", "target space")
D = n.obj("D", "another target")
f = n.mor("f", A, B, "first map")
g = n.mor("g", B, C, "second map")
h = n.mor("h", A, C, "direct map")
k = n.mor("k", C, D, "third map")
show("g * f", lib.morphism_name(g * f))
show("domain, codomain of g*f", f"{(g*f).domain.name} -> {(g*f).codomain.name}")

section("2. sympy.categories enforces the category laws for you")
show("associativity (k*g)*f == k*(g*f)", (k*g)*f == k*(g*f))
show("left identity  id_B * f == f", IdentityMorphism(B)*f == f)
show("right identity f * id_A == f", f*IdentityMorphism(A) == f)
try:
    f * g                                   # B->C after A->B ... wrong order
except ValueError as e:
    show("f * g (not composable)", f"ValueError: {e}")

section("3. A diagram and a commutativity claim")
n.diagram("triangle", [f, g, h], meaning="does going via B equal going direct?")
n.commutes("Prop 1", g * f, h, "g∘f = h")
print(n.describe("triangle"))
print("\n  -> sympy.categories records the claim but cannot decide it. A functor can.")

section("4. Functor into linear algebra: objects -> R^n, morphisms -> matrices")
t = n.sym("t", "parameter", real=True)
rot = lambda a: sp.Matrix([[sp.cos(a), -sp.sin(a)], [sp.sin(a), sp.cos(a)]])
mat_equal = lambda X, Y: (X - Y).applyfunc(sp.simplify).is_zero_matrix

F = lib.Functor(
    name="rotations",
    on_objects={A: 2, B: 2, C: 2, D: 2},           # every object -> R^2
    on_morphisms={f: rot(t), g: rot(2*t), h: rot(3*t), k: rot(-t)},
    compose=lambda G, Fm: G * Fm,                  # matrix product
    identity=lambda dim: sp.eye(dim),
    equal=mat_equal,
)
show("F(g*f) == F(h)  [R(2t)R(t) = R(3t)]", n.check_commutation("Prop 1", F).value)

F_wrong = lib.Functor("rotations-typo", F.on_objects,
                      {**F.on_morphisms, h: rot(4*t)}, F.compose, F.identity, mat_equal)
show("with h = R(4t) instead", n.check_commutation("Prop 1", F_wrong).value)
n.check_commutation("Prop 1", F)                   # restore

section("5. Same skeleton, different functor: densities under change of measure")
print("  (see papers/bs_measures.py: morphisms -> Radon–Nikodym densities,")
print("   composition -> multiplication; the triangle P -> Q -> QS commutes)")

section("6. Typeset the diagram for LaTeX / Overleaf  (\\usepackage[all]{xy})")
print(n.xypic("triangle"))
