"""
Functors and natural transformations.
"""

from .core import Category, Object, Morphism, CompositionError
from typing import Dict, Callable
from abc import ABC, abstractmethod


class Functor:
    """
    A structure-preserving map between categories.
    """
    def __init__(self, domain: Category, codomain: Category, name: str = None):
        self._domain = domain
        self._codomain = codomain
        self._name = name or f"F_{id(self)}"
        self._object_map: Dict[Object, Object] = {}
        self._morphism_map: Dict[Morphism, Morphism] = {}
    
    @property
    def domain(self) -> Category:
        return self._domain
    
    @property
    def codomain(self) -> Category:
        return self._codomain
    
    @property
    def name(self) -> str:
        return self._name
    
    def map_object(self, obj: Object) -> Object:
        """Map an object. Must be defined before use."""
        if obj not in self._object_map:
            raise ValueError(f"No object mapping defined for {obj}")
        return self._object_map[obj]
    
    def map_morphism(self, mor: Morphism) -> Morphism:
        """Map a morphism. Must be defined before use."""
        if mor not in self._morphism_map:
            raise ValueError(f"No morphism mapping defined for {mor}")
        return self._morphism_map[ mor]
    
    def set_object_mapping(self, source: Object, target: Object):
        """Define the mapping for an object."""
        self._object_map[source] = target
    
    def set_morphism_mapping(self, source: Morphism, target: Morphism):
        """Define the mapping for a morphism."""
        self._morphism_map[source] = target
    
    def verify(self) -> bool:
        """
        Verify functoriality:
        1. F(id_A) = id_{F(A)}
        2. F(g ∘ f) = F(g) ∘ F(f)
        """
        # Check identity preservation
        for obj in self._domain.objects:
            F_obj = self._object_map.get(obj)
            if F_obj is None:
                print(f"Missing object mapping for {obj}")
                return False
            
            id_original = obj.identity()
            id_mapped = self._morphism_map.get(id_original)
            if id_mapped is None:
                print(f"Missing morphism mapping for {id_original}")
                return False
            
            id_expected = F_obj.identity()
            if id_mapped != id_expected:
                print(f"Identity not preserved for {obj}")
                return False
        
        # Check composition preservation (simplified)
        # For all composable pairs in hom-sets...
        for (src, mid), mors1 in self._domain._hom_sets.items():
            for f in mors1:
                if (mid, f.codomain) in self._domain._hom_sets:
                    for g in self._domain._hom_sets[(mid, f.codomain)]:
                        if f.codomain != g.domain:
                            continue
                        
                        F_f = self._morphism_map.get(f)
                        F_g = self._morphism_map.get(g)
                        if F_f is None or F_g is None:
                            continue
                        
                        composite = self._domain.compose(g, f)
                        F_composite = self._morphism_map.get(composite)
                        
                        if F_composite is None:
                            print(f"Missing mapping for composite {composite}")
                            return False
                        
                        expected = self._codomain.compose(F_g, F_f)
                        if F_composite != expected:
                            print(f"Composition not preserved: {composite}")
                            return False
        
        return True
    
    def __call__(self, x):
        """Apply the functor to an object or morphism."""
        if isinstance(x, Object):
            return self.map_object(x)
        elif isinstance(x, Morphism):
            return self.map_morphism(x)
        else:
            raise TypeError(f"Cannot apply functor to {type(x)}")
    
    def __repr__(self):
        return f"Functor({self._name}: {self._domain.name} → {self._codomain.name})"


class ForgetfulFunctor(Functor):
    """
    The forgetful functor Grp → FinSet that forgets group structure.
    """
    def __init__(self, domain, codomain):
        super().__init__(domain, codomain, "Forgetful")
    
    def setup(self, group_obj_map: Dict):
        """
        Set up the forgetful mapping.
        group_obj_map: maps GroupObject -> FinSetObject
        """
        for group_obj, set_obj in group_obj_map.items():
            self.set_object_mapping(group_obj, set_obj)
        
        # For each group homomorphism, create the corresponding set function
        for (src, tgt), mors in self._domain._hom_sets.items():
            for mor in mors:
                if src in self._object_map and tgt in self._object_map:
                    F_src = self._object_map[src]
                    F_tgt = self._object_map[tgt]
                    
                    # The underlying function on the set elements
                    mapping = {x: mor(x) for x in src.elements}
                    from scaffold.categories.sets import SetMorphism
                    
                    set_mor = SetMorphism(F_src, F_tgt, mapping, 
                                         f"U({mor.name})")
                    self.set_morphism_mapping(mor, set_mor)
                    self._codomain._add_morphism(set_mor)


class NaturalTransformation:
    """
    A natural transformation between two functors F, G: C → D.
    """
    def __init__(self, F: Functor, G: Functor, name: str = None):
        if F.domain != G.domain:
            raise ValueError("Functors must have same domain")
        if F.codomain != G.codomain:
            raise ValueError("Functors must have same codomain")
        
        self._F = F
        self._G = G
        self._name = name or f"α_{id(self)}"
        self._components: Dict[Object, Morphism] = {}
    
    def set_component(self, obj: Object, morphism: Morphism):
        """Set the component α_A: F(A) → G(A)."""
        self._components[obj] = morphism
    
    def verify_naturality(self) -> bool:
        """
        Verify naturality: for all f: A → B, G(f) ∘ α_A = α_B ∘ F(f)
        """
        C = self._F.domain
        D = self._F.codomain
        
        for (A, B), mors in C._hom_sets.items():
            for f in mors:
                F_A = self._F.map_object(A)
                F_B = self._F.map_object(B)
                G_A = self._G.map_object(A)
                G_B = self._G.map_object(B)
                
                F_f = self._F.map_morphism(f)
                G_f = self._G.map_morphism(f)
                
                α_A = self._components.get(A)
                α_B = self._components.get(B)
                
                if α_A is None or α_B is None:
                    continue
                
                # G(f) ∘ α_A
                lhs = D.compose(G_f, α_A)
                # α_B ∘ F(f)
                rhs = D.compose(α_B, F_f)
                
                if lhs != rhs:
                    print(f"Naturality fails for {f}: {lhs} ≠ {rhs}")
                    return False
        
        return True
