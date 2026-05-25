"""
The category Grp: objects are groups, morphisms are group homomorphisms.
"""

from ..core import Category, Object, Morphism, CompositionError
from typing import Callable, Set, Any


class GroupObject(Object):
    """
    A group as an object in the category of groups.
    """
    def __init__(self, name: str, category: 'Grp', elements: Set[Any],
                 operation: Callable[[Any, Any], Any], identity_elem: Any):
        self._elements = frozenset(elements)
        self._op = operation
        self._identity = identity_elem
        # We could verify group axioms here
        super().__init__(name, category)
    
    @property
    def elements(self) -> frozenset:
        return self._elements
    
    @property
    def identity(self) -> Any:
        return self._identity
    
    def operate(self, a, b) -> Any:
        """Apply the group operation."""
        return self._op(a, b)
    
    def __repr__(self):
        return f"Group({self.name})"


class GroupHomomorphism(Morphism):
    """
    A group homomorphism between two groups.
    """
    def __init__(self, domain: GroupObject, codomain: GroupObject,
                 mapping: Callable[[Any], Any], name: str = None):
        self._mapping = mapping
        super().__init__(domain, codomain, name)
        self._verify_homomorphism()
    
    def _verify_homomorphism(self):
        """Check that mapping preserves group structure."""
        dom = self.domain
        # Check identity preservation
        id_img = self._mapping(dom.identity)
        if id_img != self.codomain.identity:
            raise ValueError("Homomorphism must preserve identity")
        
        # Check operation preservation for a sample (full check is expensive)
        # For finite groups, we could check all pairs
        for a in dom.elements:
            for b in dom.elements:
                if self._mapping(dom.operate(a, b)) != \
                   self.codomain.operate(self._mapping(a), self._mapping(b)):
                    raise ValueError("Homomorphism must preserve group operation")
    
    def __call__(self, x):
        return self._mapping(x)
    
    def compose(self, other: 'GroupHomomorphism') -> 'GroupHomomorphism':
        """Compose self @ other."""
        if not isinstance(other, GroupHomomorphism):
            raise CompositionError("Can only compose GroupHomomorphisms")
        if other.codomain != self.domain:
            raise CompositionError(
                f"Cannot compose: {other.codomain} != {self.domain}"
            )
        
        def composed(x):
            return self._mapping(other._mapping(x))
        
        new_name = f"({self._name} @ {other._name})"
        return GroupHomomorphism(other.domain, self.codomain, composed, new_name)


class Grp(Category):
    """
    The category of groups and group homomorphisms.
    """
    def __init__(self):
        super().__init__("Grp")
    
    def create_object(self, name: str, elements: Set[Any],
                      operation: Callable[[Any, Any], Any], 
                      identity_elem: Any) -> GroupObject:
        """Create a group object."""
        return GroupObject(name, self, elements, operation, identity_elem)
    
    def create_morphism(self, domain: GroupObject, codomain: GroupObject,
                        mapping: Callable[[Any], Any], 
                        name: str = None) -> GroupHomomorphism:
        """Create and register a group homomorphism."""
        morphism = GroupHomomorphism(domain, codomain, mapping, name)
        self._add_morphism(morphism)
        return morphism
    
    def identity(self, obj: GroupObject) -> GroupHomomorphism:
        """Identity homomorphism."""
        morphism = GroupHomomorphism(obj, obj, lambda x: x, f"id_{obj.name}")
        self._add_morphism(morphism)
        return morphism
    
    def compose(self, f: GroupHomomorphism, g: GroupHomomorphism) -> GroupHomomorphism:
        """Compose f @ g."""
        return f.compose(g)
