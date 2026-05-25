"""Tests for the Grp category (groups and group homomorphisms)."""
import pytest
from scaffold.categories.groups import Grp, GroupObject, GroupHomomorphism
from scaffold.core import CompositionError


def _Z2():
    C = Grp()
    Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
    return C, Z2


def _Z4():
    C = Grp()
    Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
    return C, Z4


class TestGroupObject:
    def test_elements_stored_as_frozenset(self):
        _, Z2 = _Z2()
        assert Z2.elements == frozenset({0, 1})

    def test_identity_element(self):
        _, Z2 = _Z2()
        assert Z2.identity == 0

    def test_operate(self):
        _, Z2 = _Z2()
        assert Z2.operate(1, 1) == 0  # 1 + 1 mod 2 = 0
        assert Z2.operate(0, 1) == 1
        assert Z2.operate(0, 0) == 0

    def test_registered_in_category(self):
        C, Z2 = _Z2()
        assert Z2 in C.objects

    def test_repr_contains_name(self):
        _, Z2 = _Z2()
        assert "Z₂" in repr(Z2)


class TestGroupHomomorphism:
    def test_valid_reduction_mod2(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "mod2")
        assert phi(0) == 0
        assert phi(1) == 1
        assert phi(2) == 0
        assert phi(3) == 1

    def test_valid_trivial_homomorphism(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        T = C.create_object("T", {0}, lambda a, b: 0, 0)
        trivial = C.create_morphism(Z4, T, lambda x: 0, "trivial")
        for x in Z4.elements:
            assert trivial(x) == 0

    def test_invalid_does_not_preserve_identity_raises(self):
        C = Grp()
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        Z2b = C.create_object("Z₂b", {0, 1}, lambda a, b: (a + b) % 2, 0)
        with pytest.raises(ValueError, match="identity"):
            C.create_morphism(Z2, Z2b, lambda x: 1 - x, "flip")  # 0 ↦ 1, breaks identity

    def test_invalid_does_not_preserve_operation_raises(self):
        C = Grp()
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        with pytest.raises(ValueError):
            # Not a valid homomorphism Z₂ → Z₄ (maps 0→0, 1→1 but 1+1≠0+0 in Z₄)
            C.create_morphism(Z2, Z4, lambda x: x, "bad")

    def test_composition_of_homomorphisms(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        T = C.create_object("T", {0}, lambda a, b: 0, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        psi = C.create_morphism(Z2, T, lambda x: 0, "psi")
        composed = psi @ phi
        assert composed.domain is Z4
        assert composed.codomain is T
        for x in Z4.elements:
            assert composed(x) == 0

    def test_composition_incompatible_raises(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        psi = C.create_morphism(Z4, Z2, lambda x: x % 2, "psi")
        with pytest.raises(CompositionError):
            phi @ psi  # psi.codomain (Z2) != phi.domain (Z4)

    def test_compose_with_non_homomorphism_raises(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        with pytest.raises(CompositionError):
            phi.compose("not a homomorphism")

    def test_homomorphism_call(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        assert phi(2) == 0
        assert phi(3) == 1


class TestGrpCategory:
    def test_identity_is_valid_homomorphism(self):
        C, Z2 = _Z2()
        id_Z2 = C.identity(Z2)
        for x in Z2.elements:
            assert id_Z2(x) == x

    def test_identity_domain_codomain(self):
        C, Z2 = _Z2()
        id_Z2 = C.identity(Z2)
        assert id_Z2.domain is Z2
        assert id_Z2.codomain is Z2

    def test_identity_registered_in_category(self):
        C, Z2 = _Z2()
        id_Z2 = C.identity(Z2)
        assert id_Z2 in C.morphisms(Z2, Z2)

    def test_compose_method(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        id_Z2 = C.identity(Z2)
        composed = C.compose(id_Z2, phi)
        for x in Z4.elements:
            assert composed(x) == phi(x)

    def test_homomorphism_preserves_operation(self):
        C = Grp()
        Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        phi = C.create_morphism(Z4, Z2, lambda x: x % 2, "phi")
        for a in Z4.elements:
            for b in Z4.elements:
                lhs = phi(Z4.operate(a, b))
                rhs = Z2.operate(phi(a), phi(b))
                assert lhs == rhs
