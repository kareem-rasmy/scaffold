"""Tests for the FinSet category (finite sets and functions)."""
import pytest
from scaffold.categories.sets import FinSet, FinSetObject, SetMorphism
from scaffold.core import CompositionError


class TestFinSetObject:
    def test_elements_stored_as_frozenset(self):
        C = FinSet()
        A = C.create_object("A", {1, 2, 3})
        assert isinstance(A.elements, frozenset)
        assert A.elements == frozenset({1, 2, 3})

    def test_size(self):
        C = FinSet()
        A = C.create_object("A", {1, 2, 3})
        assert A.size == 3

    def test_empty_set_size_is_zero(self):
        C = FinSet()
        E = C.create_object("E", set())
        assert E.size == 0

    def test_repr_contains_name(self):
        C = FinSet()
        A = C.create_object("MySet", {1})
        assert "MySet" in repr(A)

    def test_repr_contains_elements(self):
        C = FinSet()
        A = C.create_object("A", {42})
        assert "42" in repr(A)


class TestSetMorphism:
    def test_valid_morphism_created(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x", "y"})
        f = C.create_morphism(A, B, {1: "x", 2: "y"}, "f")
        assert f.domain is A
        assert f.codomain is B

    def test_mapping_property_returns_copy(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {"x"})
        f = C.create_morphism(A, B, {1: "x"}, "f")
        m = f.mapping
        m[99] = "z"
        assert 99 not in f.mapping

    def test_call_applies_function(self):
        C = FinSet()
        A = C.create_object("A", {1, 2, 3})
        B = C.create_object("B", {"odd", "even"})
        f = C.create_morphism(A, B, {1: "odd", 2: "even", 3: "odd"}, "f")
        assert f(1) == "odd"
        assert f(2) == "even"
        assert f(3) == "odd"

    def test_missing_domain_element_raises(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x"})
        with pytest.raises(ValueError, match="has no image"):
            SetMorphism(A, B, {1: "x"}, "bad")  # 2 missing

    def test_extra_element_not_in_domain_raises(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {"x"})
        with pytest.raises(ValueError):
            SetMorphism(A, B, {1: "x", 99: "x"}, "bad")  # 99 not in A

    def test_image_not_in_codomain_raises(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {"x"})
        with pytest.raises(ValueError, match="not in codomain"):
            SetMorphism(A, B, {1: "z"}, "bad")  # "z" not in B

    def test_empty_domain_valid(self):
        C = FinSet()
        empty = C.create_object("∅", set())
        B = C.create_object("B", {1})
        f = C.create_morphism(empty, B, {}, "empty_func")
        assert f.domain is empty

    def test_compose_produces_correct_result(self):
        C = FinSet()
        A = C.create_object("A", {1, 2, 3})
        B = C.create_object("B", {"x", "y"})
        D = C.create_object("D", {True, False})
        f = C.create_morphism(A, B, {1: "x", 2: "y", 3: "x"}, "f")
        g = C.create_morphism(B, D, {"x": True, "y": False}, "g")
        h = g.compose(f)
        assert h(1) is True
        assert h(2) is False
        assert h(3) is True

    def test_compose_incompatible_raises(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        D = C.create_object("D", {3})
        f = C.create_morphism(A, B, {1: 2}, "f")
        g = C.create_morphism(A, D, {1: 3}, "g")
        with pytest.raises(CompositionError):
            f.compose(g)  # g.codomain (D) != f.domain (B)

    def test_compose_non_set_morphism_raises(self):
        C = FinSet()
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "f")
        with pytest.raises(CompositionError):
            f.compose("not a morphism")


class TestFinSetCategory:
    def test_identity_maps_each_element_to_itself(self):
        C = FinSet()
        A = C.create_object("A", {1, 2, 3})
        id_A = C.identity(A)
        for x in A.elements:
            assert id_A(x) == x

    def test_identity_domain_and_codomain_are_same(self):
        C = FinSet()
        A = C.create_object("A", {1})
        id_A = C.identity(A)
        assert id_A.domain is A
        assert id_A.codomain is A

    def test_identity_registered_in_category(self):
        C = FinSet()
        A = C.create_object("A", {1})
        id_A = C.identity(A)
        assert id_A in C.morphisms(A, A)

    def test_matmul_composition(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x", "y"})
        D = C.create_object("D", {10, 20})
        f = C.create_morphism(A, B, {1: "x", 2: "y"}, "f")
        g = C.create_morphism(B, D, {"x": 10, "y": 20}, "g")
        h = g @ f
        assert h(1) == 10
        assert h(2) == 20

    def test_category_compose_method(self):
        C = FinSet()
        A = C.create_object("A", {1})
        B = C.create_object("B", {2})
        D = C.create_object("D", {3})
        f = C.create_morphism(A, B, {1: 2}, "f")
        g = C.create_morphism(B, D, {2: 3}, "g")
        h = C.compose(g, f)
        assert h(1) == 3

    def test_identity_is_left_unit(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x", "y"})
        f = C.create_morphism(A, B, {1: "x", 2: "y"}, "f")
        id_B = C.identity(B)
        assert (id_B @ f).mapping == f.mapping

    def test_identity_is_right_unit(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"x", "y"})
        f = C.create_morphism(A, B, {1: "x", 2: "y"}, "f")
        id_A = C.identity(A)
        assert (f @ id_A).mapping == f.mapping

    def test_composition_associativity(self):
        C = FinSet()
        A = C.create_object("A", {1, 2})
        B = C.create_object("B", {"p", "q"})
        D = C.create_object("D", {10, 20})
        E = C.create_object("E", {"yes", "no"})
        f = C.create_morphism(A, B, {1: "p", 2: "q"}, "f")
        g = C.create_morphism(B, D, {"p": 10, "q": 20}, "g")
        h = C.create_morphism(D, E, {10: "yes", 20: "no"}, "h")
        lhs = (h @ g) @ f
        rhs = h @ (g @ f)
        assert lhs.mapping == rhs.mapping

    def test_terminal_is_singleton_with_star(self):
        C = FinSet()
        T = C.terminal
        assert T.size == 1
        assert "*" in T.elements

    def test_initial_is_empty_set(self):
        C = FinSet()
        I = C.initial
        assert I.size == 0

    def test_unique_morphism_to_terminal(self):
        C = FinSet()
        T = C.terminal
        A = C.create_object("A", {"x", "y", "z"})
        bang = C.create_morphism(A, T, {a: "*" for a in A.elements}, "!")
        for a in A.elements:
            assert bang(a) == "*"

    def test_unique_morphism_from_initial(self):
        C = FinSet()
        I = C.initial
        A = C.create_object("A", {1, 2})
        empty_mor = C.create_morphism(I, A, {}, "absurd")
        assert empty_mor.domain is I
        assert empty_mor.codomain is A

    def test_product_universal_property(self):
        C = FinSet()
        A = C.create_object("A", {"a1", "a2"})
        B = C.create_object("B", {"b1", "b2"})
        AxB_elems = {(a, b) for a in A.elements for b in B.elements}
        AxB = C.create_object("A×B", AxB_elems)
        pi1 = C.create_morphism(AxB, A, {(a, b): a for (a, b) in AxB_elems}, "π₁")
        pi2 = C.create_morphism(AxB, B, {(a, b): b for (a, b) in AxB_elems}, "π₂")

        X = C.create_object("X", {"x1", "x2"})
        f = C.create_morphism(X, A, {"x1": "a1", "x2": "a2"}, "f")
        g = C.create_morphism(X, B, {"x1": "b1", "x2": "b2"}, "g")
        mediating = C.create_morphism(X, AxB,
                                      {"x1": ("a1", "b1"), "x2": ("a2", "b2")},
                                      "⟨f,g⟩")
        assert (pi1 @ mediating).mapping == f.mapping
        assert (pi2 @ mediating).mapping == g.mapping
