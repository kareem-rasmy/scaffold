"""Tests for Functor, ForgetfulFunctor, and NaturalTransformation."""
import pytest
from scaffold.categories.sets import FinSet
from scaffold.categories.groups import Grp
from scaffold.functors import Functor, ForgetfulFunctor, NaturalTransformation


class TestFunctor:
    def test_domain_and_codomain(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        assert F.domain is C
        assert F.codomain is D

    def test_name(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "MyFunctor")
        assert F.name == "MyFunctor"

    def test_auto_name_when_none(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D)
        assert F.name is not None

    def test_repr_contains_name_and_categories(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        r = repr(F)
        assert "F" in r
        assert "FinSet" in r

    def test_map_object_raises_without_mapping(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1})
        with pytest.raises(ValueError):
            F.map_object(A)

    def test_map_morphism_raises_without_mapping(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "f")
        with pytest.raises(ValueError):
            F.map_morphism(f)

    def test_set_and_retrieve_object_mapping(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1, 2})
        B = D.create_object("B", {10, 20})
        F.set_object_mapping(A, B)
        assert F.map_object(A) is B

    def test_set_and_retrieve_morphism_mapping(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "f")
        B = D.create_object("B", {1})
        g = D.create_morphism(B, B, {1: 1}, "g")
        F.set_morphism_mapping(f, g)
        assert F.map_morphism(f) is g

    def test_call_on_object(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1})
        B = D.create_object("B", {1})
        F.set_object_mapping(A, B)
        assert F(A) is B

    def test_call_on_morphism(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        A = C.create_object("A", {1})
        f = C.create_morphism(A, A, {1: 1}, "f")
        B = D.create_object("B", {1})
        g = D.create_morphism(B, B, {1: 1}, "g")
        F.set_morphism_mapping(f, g)
        assert F(f) is g

    def test_call_on_invalid_type_raises(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        with pytest.raises(TypeError):
            F("not an object or morphism")


class TestForgetfulFunctor:
    def _setup(self):
        grp = Grp()
        Z2 = grp.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
        Z4 = grp.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
        phi = grp.create_morphism(Z4, Z2, lambda x: x % 2, "phi")

        fset = FinSet()
        Z2_set = fset.create_object("Z₂_set", {0, 1})
        Z4_set = fset.create_object("Z₄_set", {0, 1, 2, 3})

        U = ForgetfulFunctor(grp, fset)
        U.setup({Z2: Z2_set, Z4: Z4_set})
        return U, Z2, Z4, phi, Z2_set, Z4_set

    def test_maps_groups_to_their_underlying_sets(self):
        U, Z2, Z4, phi, Z2_set, Z4_set = self._setup()
        assert U.map_object(Z2) is Z2_set
        assert U.map_object(Z4) is Z4_set

    def test_maps_homomorphism_to_set_function(self):
        U, Z2, Z4, phi, Z2_set, Z4_set = self._setup()
        U_phi = U.map_morphism(phi)
        assert U_phi.domain is Z4_set
        assert U_phi.codomain is Z2_set

    def test_underlying_function_agrees_with_homomorphism(self):
        U, Z2, Z4, phi, Z2_set, Z4_set = self._setup()
        U_phi = U.map_morphism(phi)
        for x in Z4.elements:
            assert U_phi(x) == phi(x)


class TestNaturalTransformation:
    def test_creation_with_same_domain_and_codomain(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        G = Functor(C, D, "G")
        alpha = NaturalTransformation(F, G, "α")
        assert alpha._F is F
        assert alpha._G is G

    def test_different_domains_raises(self):
        C1 = FinSet()
        C2 = FinSet()
        D = FinSet()
        F = Functor(C1, D, "F")
        G = Functor(C2, D, "G")
        with pytest.raises(ValueError, match="same domain"):
            NaturalTransformation(F, G)

    def test_different_codomains_raises(self):
        C = FinSet()
        D1 = FinSet()
        D2 = FinSet()
        F = Functor(C, D1, "F")
        G = Functor(C, D2, "G")
        with pytest.raises(ValueError, match="same codomain"):
            NaturalTransformation(F, G)

    def test_auto_name_when_none(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D)
        G = Functor(C, D)
        alpha = NaturalTransformation(F, G)
        assert alpha._name is not None

    def test_set_component(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        G = Functor(C, D, "G")
        A = C.create_object("A", {1})
        FA = D.create_object("FA", {1})
        GA = D.create_object("GA", {1})
        F.set_object_mapping(A, FA)
        G.set_object_mapping(A, GA)
        alpha = NaturalTransformation(F, G, "α")
        component = D.create_morphism(FA, GA, {1: 1}, "α_A")
        alpha.set_component(A, component)
        assert alpha._components[A] is component

    def test_verify_naturality_empty_category(self):
        C = FinSet()
        D = FinSet()
        F = Functor(C, D, "F")
        G = Functor(C, D, "G")
        alpha = NaturalTransformation(F, G, "α")
        # No morphisms in C, naturality holds vacuously
        assert alpha.verify_naturality() is True
