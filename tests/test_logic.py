"""Tests for the PropLogic category (Curry-Howard correspondence)."""
import pytest
from scaffold.categories.logic import PropLogic, Proposition, Proof, Connective
from scaffold.core import CompositionError


class TestProposition:
    def test_atomic_is_atomic(self):
        L = PropLogic()
        P = L.atomic("P")
        assert P.is_atomic
        assert P.name == "P"

    def test_atomic_registered_in_category(self):
        L = PropLogic()
        P = L.atomic("P")
        assert P in L.objects

    def test_truth_is_terminal(self):
        L = PropLogic()
        T = L.truth
        assert T.connective == Connective.TRUE
        assert "⊤" in repr(T)

    def test_falsehood_is_initial(self):
        L = PropLogic()
        F = L.falsehood
        assert F.connective == Connective.FALSE

    def test_truth_singleton(self):
        L = PropLogic()
        assert L.truth is L.truth  # same object

    def test_falsehood_singleton(self):
        L = PropLogic()
        assert L.falsehood is L.falsehood

    def test_conjunction_connective(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        assert not PQ.is_atomic
        assert PQ.connective == Connective.AND

    def test_conjunction_name(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        assert "P" in PQ.name and "Q" in PQ.name

    def test_conjunction_repr_contains_symbol(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        assert "∧" in repr(PQ)

    def test_implication_connective(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        impl = L.implication(P, Q)
        assert not impl.is_atomic
        assert impl.connective == Connective.IMPLIES

    def test_implication_repr(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        impl = L.implication(P, Q)
        assert "⊃" in repr(impl)

    def test_atomic_repr(self):
        L = PropLogic()
        P = L.atomic("P")
        assert repr(P) == "P"


class TestProof:
    def test_axiom_is_identity_proof(self):
        L = PropLogic()
        P = L.atomic("P")
        ax = L.axiom(P)
        assert ax.domain is P
        assert ax.codomain is P
        assert ax.rule_name.startswith("ax")

    def test_axiom_registered_in_category(self):
        L = PropLogic()
        P = L.atomic("P")
        ax = L.axiom(P)
        assert ax in L.morphisms(P, P)

    def test_conjunction_creates_projections(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        morphisms = L.all_morphisms()
        # There should be projections π₁: P∧Q → P and π₂: P∧Q → Q
        projs_to_P = [m for m in morphisms if m.domain is PQ and m.codomain is P]
        projs_to_Q = [m for m in morphisms if m.domain is PQ and m.codomain is Q]
        assert len(projs_to_P) == 1
        assert len(projs_to_Q) == 1

    def test_proof_premises(self):
        L = PropLogic()
        P = L.atomic("P")
        ax = L.axiom(P)
        assert ax.premises == []

    def test_proof_composition_cut(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        PQ = L.conjunction(P, Q)
        fst = next(m for m in L.morphisms(PQ, P))
        ax_P = L.axiom(P)
        cut = ax_P @ fst  # (P → P) ∘ (P∧Q → P) = P∧Q → P
        assert cut.domain is PQ
        assert cut.codomain is P

    def test_proof_composition_records_premises(self):
        L = PropLogic()
        P = L.atomic("P")
        ax1 = L.axiom(P)
        ax2 = L.axiom(P)
        composed = ax1 @ ax2
        assert len(composed.premises) == 2

    def test_proof_composition_incompatible_raises(self):
        L = PropLogic()
        P = L.atomic("P")
        Q = L.atomic("Q")
        ax_P = L.axiom(P)
        ax_Q = L.axiom(Q)
        with pytest.raises(CompositionError):
            ax_P @ ax_Q  # P ≠ Q

    def test_proof_composition_with_non_proof_raises(self):
        L = PropLogic()
        P = L.atomic("P")
        ax = L.axiom(P)
        with pytest.raises(CompositionError):
            ax.compose("not a proof")

    def test_proof_repr(self):
        L = PropLogic()
        P = L.atomic("P")
        ax = L.axiom(P)
        r = repr(ax)
        assert "P" in r
        assert "⊢" in r

    def test_implication_intro(self):
        L = PropLogic()
        P = L.atomic("P")
        ax_P = L.axiom(P)
        proof = L.prove_implication_intro(P, P, ax_P)
        assert proof.domain is L.truth
        assert proof.codomain.connective == Connective.IMPLIES

    def test_implication_intro_registered(self):
        L = PropLogic()
        P = L.atomic("P")
        ax_P = L.axiom(P)
        proof = L.prove_implication_intro(P, P, ax_P)
        assert proof in L.all_morphisms()


class TestPropLogicCategory:
    def test_identity_is_axiom(self):
        L = PropLogic()
        P = L.atomic("P")
        id_P = L.identity(P)
        assert id_P.domain is P
        assert id_P.codomain is P

    def test_compose_is_cut(self):
        L = PropLogic()
        P = L.atomic("P")
        ax1 = L.axiom(P)
        ax2 = L.axiom(P)
        composed = L.compose(ax1, ax2)
        assert composed.domain is P
        assert composed.codomain is P
        assert "cut" in composed.rule_name


class TestConnective:
    def test_all_connectives_distinct(self):
        values = [Connective.AND, Connective.OR, Connective.IMPLIES,
                  Connective.TRUE, Connective.FALSE]
        assert len(set(values)) == 5
