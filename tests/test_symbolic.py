"""Tests for the symbolic enhancement layer (SymPy integration)."""
import pytest
from sympy import symbols, Lambda, FiniteSet, Interval, oo, Symbol

from scaffold.symbolic import (
    SymbolicFinSet, SymbolicSetObject, SymbolicSetMorphism,
    SymbolicPropLogic, SymbolicProposition, SymbolicProof,
    UniversalPropertyVerifier, CategoryPrinter,
)
from scaffold.categories.sets import FinSet
from scaffold.core import CompositionError


class TestSymbolicSetObject:
    def test_finite_set_not_infinite(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
        assert not A.is_infinite

    def test_finite_set_elements(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
        assert A.elements == frozenset({1, 2, 3})

    def test_interval_is_infinite(self):
        C = SymbolicFinSet()
        R = C.create_symbolic_set("R", expr=Interval(-oo, oo))
        assert R.is_infinite

    def test_symbolic_expression_preserved(self):
        C = SymbolicFinSet()
        expr = FiniteSet(1, 2, 3)
        A = C.create_symbolic_set("A", expr=expr)
        assert A.symbolic_expression == expr

    def test_repr_contains_name(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("MySet", expr=FiniteSet(1))
        assert "MySet" in repr(A)

    def test_registered_in_category(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        assert A in C.objects


class TestSymbolicSetMorphism:
    def test_morphism_on_finite_domain_is_callable(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
        B = C.create_symbolic_set("B", expr=FiniteSet(2, 4, 6))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2 * x), "double")
        assert f(1) == 2
        assert f(2) == 4
        assert f(3) == 6

    def test_morphism_on_infinite_domain_evaluates_symbolically(self):
        C = SymbolicFinSet()
        x = symbols('x')
        R = C.create_symbolic_set("R", expr=Interval(-oo, oo))
        R2 = C.create_symbolic_set("R2", expr=Interval(-oo, oo))
        square = C.create_symbolic_morphism(R, R2, Lambda(x, x ** 2), "sq")
        result = square(x)
        assert result == x ** 2

    def test_symbolic_function_property(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2))
        B = C.create_symbolic_set("B", expr=FiniteSet(2, 4))
        x = symbols('x')
        lam = Lambda(x, 2 * x)
        f = C.create_symbolic_morphism(A, B, lam, "f")
        assert f.symbolic_function == lam

    def test_composition_on_finite_domain(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2))
        B = C.create_symbolic_set("B", expr=FiniteSet(2, 4))
        D = C.create_symbolic_set("D", expr=FiniteSet(4, 8))
        x = symbols('x')
        double = C.create_symbolic_morphism(A, B, Lambda(x, 2 * x), "double")
        quad = C.create_symbolic_morphism(B, D, Lambda(x, 2 * x), "quad")
        composed = quad @ double
        assert composed(1) == 4
        assert composed(2) == 8

    def test_composition_on_infinite_domain(self):
        C = SymbolicFinSet()
        x = symbols('x')
        R = C.create_symbolic_set("R", expr=Interval(-oo, oo))
        f = C.create_symbolic_morphism(R, R, Lambda(x, x + 1), "inc")
        g = C.create_symbolic_morphism(R, R, Lambda(x, x * 2), "dbl")
        h = g @ f  # double(inc(x)) = 2(x+1)
        from sympy import simplify
        assert simplify(h(x) - 2 * (x + 1)) == 0

    def test_composition_name_contains_both_names(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        B = C.create_symbolic_set("B", expr=FiniteSet(2))
        D = C.create_symbolic_set("D", expr=FiniteSet(4))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2), "f")
        g = C.create_symbolic_morphism(B, D, Lambda(x, 4), "g")
        h = g @ f
        assert "f" in h.name and "g" in h.name

    def test_composition_incompatible_raises(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        B = C.create_symbolic_set("B", expr=FiniteSet(2))
        D = C.create_symbolic_set("D", expr=FiniteSet(3))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2), "f")
        g = C.create_symbolic_morphism(A, D, Lambda(x, 3), "g")
        with pytest.raises(CompositionError):
            f @ g

    def test_composition_with_non_symbolic_raises(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        B = C.create_symbolic_set("B", expr=FiniteSet(2))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2), "f")
        with pytest.raises(CompositionError):
            f.compose("not a morphism")


class TestSymbolicFinSet:
    def test_category_name(self):
        C = SymbolicFinSet()
        assert C.name == "SymbolicFinSet"

    def test_identity_maps_to_itself_symbolically(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
        id_A = C.identity(A)
        x = symbols('x')
        assert id_A(x) == x

    def test_identity_is_lambda_x_x(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(5))
        id_A = C.identity(A)
        x = symbols('x')
        assert id_A.symbolic_function(x) == x

    def test_identity_registered_in_category(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        id_A = C.identity(A)
        assert id_A in C.morphisms(A, A)

    def test_compose_delegates_to_morphism(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2))
        B = C.create_symbolic_set("B", expr=FiniteSet(2, 4))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2 * x), "f")
        id_B = C.identity(B)
        result = C.compose(id_B, f)
        assert result(1) == 2


class TestSymbolicPropLogic:
    def test_atomic_creates_proposition(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert P.name == "P"
        assert isinstance(P, SymbolicProposition)

    def test_atomic_sympy_expression_is_symbol(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert P.sympy_expression == Symbol("P")

    def test_conjunction_sympy_expression(self):
        from sympy import And
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        assert PQ.sympy_expression == And(Symbol("P"), Symbol("Q"))

    def test_implication_sympy_expression(self):
        from sympy import Implies
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        impl = L.implication(P, Q)
        assert impl.sympy_expression == Implies(Symbol("P"), Symbol("Q"))

    def test_disjunction_sympy_expression(self):
        from sympy import Or
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        disj = L.disjunction(P, Q)
        assert disj.sympy_expression == Or(Symbol("P"), Symbol("Q"))

    def test_negation_sympy_expression(self):
        from sympy import Not
        L = SymbolicPropLogic()
        P = L.atomic("P")
        neg = L.negation(P)
        assert neg.sympy_expression == Not(Symbol("P"))

    def test_is_theorem_A_implies_A(self):
        L = SymbolicPropLogic()
        A = L.atomic("A")
        assert L.is_theorem(L.implication(A, A))

    def test_is_theorem_excluded_middle(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert L.is_theorem(L.disjunction(P, L.negation(P)))

    def test_is_theorem_modus_ponens(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        # (P ^ (P => Q)) => Q
        mp = L.implication(L.conjunction(P, L.implication(P, Q)), Q)
        assert L.is_theorem(mp)

    def test_is_theorem_conjunction_implies_left(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        # (P ^ Q) => P
        assert L.is_theorem(L.implication(L.conjunction(P, Q), P))

    def test_is_theorem_double_negation_elimination(self):
        L = SymbolicPropLogic()
        A = L.atomic("A")
        not_not_A = L.negation(L.negation(A))
        # ~~A => A is a classical tautology
        assert L.is_theorem(L.implication(not_not_A, A))

    def test_not_a_theorem_bare_atom(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert not L.is_theorem(P)

    def test_not_a_theorem_conjunction_implies_negation(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        # (P ^ Q) => ~P  — not a tautology
        invalid = L.implication(L.conjunction(P, Q), L.negation(P))
        assert not L.is_theorem(invalid)

    def test_verify_proof_with_sympy_proof_flag(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        proof = SymbolicProof(P, P, "test", sympy_proof=True)
        assert L.verify_proof(proof) is True

    def test_verify_proof_non_symbolic_returns_false(self):
        from scaffold.categories.logic import Proof
        L = SymbolicPropLogic()
        P = L.atomic("P")
        # Plain Proof, not SymbolicProof
        plain = Proof(P, P, "plain")
        assert L.verify_proof(plain) is False

    def test_repr_latex_contains_dollar(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert "$" in P._repr_latex_()

    def test_conjunction_creates_symbolic_projections(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        projs = [m for m in L.all_morphisms()
                 if m.domain is PQ and isinstance(m, SymbolicProof)]
        assert len(projs) == 2


class TestUniversalPropertyVerifier:
    def test_verify_product_correct_projections(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {3, 4})
        elems = {(a, b) for a in A.elements for b in B.elements}
        P = C.create_object("AxB", elems)
        pi1 = C.create_morphism(P, A, {(a, b): a for (a, b) in elems}, "pi1")
        pi2 = C.create_morphism(P, B, {(a, b): b for (a, b) in elems}, "pi2")
        v = UniversalPropertyVerifier()
        assert v.verify_product(C, A, B, P, pi1, pi2) is True

    def test_verify_product_wrong_pi1_domain_fails(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {3, 4})
        elems = {(a, b) for a in A.elements for b in B.elements}
        P = C.create_object("AxB", elems)
        pi1 = C.create_morphism(P, A, {(a, b): a for (a, b) in elems}, "pi1")
        pi2 = C.create_morphism(P, B, {(a, b): b for (a, b) in elems}, "pi2")
        v = UniversalPropertyVerifier()
        # Pass A instead of P as the claimed product
        assert v.verify_product(C, A, B, A, pi1, pi2) is False

    def test_verify_product_wrong_pi2_codomain_fails(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {3, 4})
        elems = {(a, b) for a in A.elements for b in B.elements}
        P = C.create_object("AxB", elems)
        pi1 = C.create_morphism(P, A, {(a, b): a for (a, b) in elems}, "pi1")
        # pi2 points to A instead of B — wrong codomain
        pi2_wrong = C.create_morphism(P, A, {(a, b): a for (a, b) in elems}, "pi2_bad")
        v = UniversalPropertyVerifier()
        assert v.verify_product(C, A, B, P, pi1, pi2_wrong) is False

    def test_verify_terminal_passes_when_all_objects_have_morphism_to_t(self):
        C = FinSet()
        T = C.terminal
        C.identity(T)  # register id_T so T itself has a morphism to T
        A = C.create_object("A", {1, 2})
        C.create_morphism(A, T, {a: "*" for a in A.elements}, "!")
        v = UniversalPropertyVerifier()
        assert v.verify_terminal(C, T) is True

    def test_verify_terminal_fails_when_object_lacks_morphism_to_t(self):
        C = FinSet()
        T = C.terminal
        C.create_object("A", {1, 2})  # no morphism A -> T added
        v = UniversalPropertyVerifier()
        assert v.verify_terminal(C, T) is False


class TestCategoryPrinter:
    def test_print_category_outputs_name(self, capsys):
        C = SymbolicFinSet()
        C.create_symbolic_set("A", expr=FiniteSet(1, 2))
        CategoryPrinter.print_category(C)
        assert "SymbolicFinSet" in capsys.readouterr().out

    def test_print_object_outputs_name(self, capsys):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("TestSet", expr=FiniteSet(1, 2))
        CategoryPrinter.print_object(A)
        assert "TestSet" in capsys.readouterr().out

    def test_print_morphism_outputs_name(self, capsys):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1, 2))
        B = C.create_symbolic_set("B", expr=FiniteSet(2, 4))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2 * x), "my_func")
        CategoryPrinter.print_morphism(f)
        assert "my_func" in capsys.readouterr().out

    def test_to_latex_morphism_contains_dollars(self):
        C = SymbolicFinSet()
        A = C.create_symbolic_set("A", expr=FiniteSet(1))
        B = C.create_symbolic_set("B", expr=FiniteSet(2))
        x = symbols('x')
        f = C.create_symbolic_morphism(A, B, Lambda(x, 2), "f")
        assert "$" in CategoryPrinter.to_latex(f)

    def test_to_latex_proposition_contains_dollars(self):
        L = SymbolicPropLogic()
        P = L.atomic("P")
        assert "$" in CategoryPrinter.to_latex(P)

    def test_to_latex_plain_morphism_contains_dollars(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        f = C.create_morphism(A, B, {1: 2}, "f")
        assert "$" in CategoryPrinter.to_latex(f)
