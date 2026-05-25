"""Tests for core abstract framework (Object, Morphism, Category)."""
import pytest
from scaffold.core import Object, Morphism, Category, CompositionError
from scaffold.categories.sets import FinSet, SetMorphism


class TestObject:
    def test_registers_in_category_on_creation(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        assert A in C.objects

    def test_name(self):
        C = FinSet()
        A = C.create_object("A", {1})
        assert A.name == "A"

    def test_category_reference(self):
        C = FinSet()
        A = C.create_object("A", {1})
        assert A.category is C

    def test_identity_equality(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {1})
        assert A == A
        assert A != B
        assert B == B

    def test_hash_consistent_with_equality(self):
        C = FinSet()
        A = C.create_object("A", {1})
        s = {A}
        assert A in s

    def test_repr_contains_name(self):
        C = FinSet()
        A = C.create_object("MyObj", {1})
        assert "MyObj" in repr(A)

    def test_identity_morphism_via_object(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        id_A = A.identity()
        assert id_A.domain is A
        assert id_A.codomain is A


class TestMorphism:
    def test_domain_and_codomain(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        f = C.create_morphism(A, B, {1: 2}, "f")
        assert f.domain is A
        assert f.codomain is B

    def test_name(self):
        C = FinSet()
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "my_morphism")
        assert f.name == "my_morphism"

    def test_auto_name_when_none_given(self):
        C = FinSet()
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1})
        assert f.name is not None and len(f.name) > 0

    def test_repr_contains_name_and_objects(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        f = C.create_morphism(A, B, {1: 2}, "f")
        r = repr(f)
        assert "f" in r
        assert "A" in r
        assert "B" in r

    def test_matmul_composes_right_to_left(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x", "y"})
        D = C.create_object("D", {True, False})
        f = C.create_morphism(A, B, {1: "x", 2: "y"}, "f")
        g = C.create_morphism(B, D, {"x": True, "y": False}, "g")
        h = g @ f  # g @ f
        assert h.domain is A
        assert h.codomain is D

    def test_matmul_with_non_morphism_returns_not_implemented(self):
        C = FinSet()
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "f")
        assert f.__matmul__("not a morphism") is NotImplemented


class TestCategory:
    def test_name(self):
        C = FinSet()
        assert C.name == "FinSet"

    def test_repr_contains_name(self):
        C = FinSet()
        assert "FinSet" in repr(C)

    def test_objects_returns_copy(self):
        C = FinSet()
        A = C.create_object("A", {1})
        snapshot = C.objects
        snapshot.discard(A)
        assert A in C.objects  # original unchanged

    def test_morphisms_empty_for_unregistered_pair(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        assert C.morphisms(A, B) == set()

    def test_morphisms_contains_registered_morphism(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        f = C.create_morphism(A, B, {1: 2}, "f")
        assert f in C.morphisms(A, B)

    def test_all_morphisms_aggregates_all_hom_sets(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x"})
        f = C.create_morphism(A, B, {1: "x", 2: "x"}, "f")
        g = C.create_morphism(A, A, {1: 2, 2: 1}, "g")
        all_m = C.all_morphisms()
        assert f in all_m
        assert g in all_m

    def test_add_morphism_rejects_foreign_domain(self):
        C1 = FinSet()
        C2 = FinSet()
        A = C1.create_object("A", {1})
        B = C2.create_object("B", {2})
        with pytest.raises(ValueError):
            mor = SetMorphism(A, B, {1: 2}, "f")
            C1._add_morphism(mor)  # B is not in C1

    def test_add_morphism_rejects_foreign_codomain(self):
        C1 = FinSet()
        C2 = FinSet()
        A = C1.create_object("A", {1})
        B = C2.create_object("B", {1})
        A2 = C1.create_object("A2", {2})
        with pytest.raises(ValueError):
            mor = SetMorphism(A2, B, {2: 1}, "f")
            C1._add_morphism(mor)


class TestCompositionError:
    def test_is_an_exception(self):
        assert issubclass(CompositionError, Exception)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(CompositionError):
            raise CompositionError("test error")

    def test_incompatible_composition_raises(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        D = C.create_object("D", {3})
        f = C.create_morphism(A, B, {1: 2}, "f")
        g = C.create_morphism(A, D, {1: 3}, "g")
        # f.domain (A) != g.codomain (D)
        with pytest.raises(CompositionError):
            f @ g
