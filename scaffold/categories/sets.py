"""
The category FinSet: objects are finite sets, morphisms are functions.
"""

from ..core import Category, Object, Morphism, CompositionError
from typing import Set, Any, Dict


class FinSetObject(Object):
    """
    A finite set as an object. We make a small concession to computability
    by storing the elements internally, but the categorical structure treats
    this as opaque.
    """
    def __init__(self, name: str, category: 'FinSet', elements: Set[Any]):
        self._elements = frozenset(elements)
        super().__init__(name, category)
    
    @property
    def elements(self) -> frozenset:
        return self._elements
    
    @property
    def size(self) -> int:
        return len(self._elements)
    
    def __repr__(self):
        return f"SetObj({self.name} = {set(self._elements)})"


class SetMorphism(Morphism):
    """
    A function between finite sets.
    """
    def __init__(self, domain: FinSetObject, codomain: FinSetObject, 
                 mapping: Dict[Any, Any], name: str = None):
        # Validate mapping
        for x in domain.elements:
            if x not in mapping:
                raise ValueError(f"Element {x} in domain has no image")
        for x, y in mapping.items():
            if x not in domain.elements:
                raise ValueError(f"Element {x} not in domain")
            if y not in codomain.elements:
                raise ValueError(f"Image {y} not in codomain")
        
        self._mapping = dict(mapping)
        super().__init__(domain, codomain, name)
    
    @property
    def mapping(self) -> Dict[Any, Any]:
        return self._mapping.copy()
    
    def __call__(self, x):
        """Apply the function to an element."""
        return self._mapping[x]
    
    def compose(self, other: 'SetMorphism') -> 'SetMorphism':
        """Compose self ∘ other (self after other)."""
        if not isinstance(other, SetMorphism):
            raise CompositionError("Can only compose SetMorphism with SetMorphism")
        if other.codomain != self.domain:
            raise CompositionError(
                f"Cannot compose: {other.codomain} ≠ {self.domain}"
            )
        
        # Build the composite function: self(other(x))
        new_mapping = {x: self._mapping[other._mapping[x]] 
                      for x in other._mapping}
        new_name = f"({self._name} ∘ {other._name})"
        
        return SetMorphism(other.domain, self.codomain, new_mapping, new_name)


class FinSet(Category):
    """
    The category of finite sets and functions.
    """
    def __init__(self):
        super().__init__("FinSet")
    
    def create_object(self, name: str, elements: Set[Any]) -> FinSetObject:
        """Create a new finite set object."""
        return FinSetObject(name, self, elements)
    
    def create_morphism(self, domain: FinSetObject, codomain: FinSetObject,
                        mapping: Dict[Any, Any], name: str = None) -> SetMorphism:
        """Create and register a function between finite sets."""
        morphism = SetMorphism(domain, codomain, mapping, name)
        self._add_morphism(morphism)
        return morphism
    
    def identity(self, obj: FinSetObject) -> SetMorphism:
        """Identity function mapping each element to itself."""
        mapping = {x: x for x in obj.elements}
        morphism = SetMorphism(obj, obj, mapping, f"id_{obj.name}")
        self._add_morphism(morphism)
        return morphism
    
    def compose(self, f: SetMorphism, g: SetMorphism) -> SetMorphism:
        """Compose f ∘ g."""
        return f.compose(g)
    
    @property
    def terminal(self) -> FinSetObject:
        """Return a terminal object (singleton set)."""
        terminal = FinSetObject("1", self, {"*"})
        return terminal
    
    @property
    def initial(self) -> FinSetObject:
        """Return an initial object (empty set)."""
        empty = FinSetObject("∅", self, set())
        return empty
