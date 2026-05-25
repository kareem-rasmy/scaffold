"""
Core abstract base classes for the categorical framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Set, Tuple, Optional


class CompositionError(Exception):
    """Raised when morphism composition fails."""
    pass


class Object:
    """
    An object in a category. Deliberately minimal - defined by its relationships,
    not its internal structure.
    """
    def __init__(self, name: str, category: 'Category'):
        self.name = name
        self._category = category
        category._add_object(self)
    
    @property
    def category(self) -> 'Category':
        return self._category
    
    def identity(self) -> 'Morphism':
        """Returns the identity morphism for this object."""
        return self._category.identity(self)
    
    def __repr__(self):
        return f"Obj({self.name})"
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self is other


class Morphism(ABC):
    """
    A morphism between two objects. The fundamental building block.
    """
    def __init__(self, domain: Object, codomain: Object, name: Optional[str] = None):
        self._domain = domain
        self._codomain = codomain
        self._name = name or f"mor_{id(self)}"
    
    @property
    def domain(self) -> Object:
        return self._domain
    
    @property
    def codomain(self) -> Object:
        return self._codomain
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def compose(self, other: 'Morphism') -> 'Morphism':
        """
        Compose self @ other. 
        Requires: other.codomain == self.domain
        Returns: morphism from other.domain to self.codomain
        """
        pass
    
    def __matmul__(self, other: 'Morphism') -> 'Morphism':
        """Use @ for composition: f @ g means f @ g (f after g)"""
        if not isinstance(other, Morphism):
            return NotImplemented
        return self.compose(other)
    
    def __repr__(self):
        return f"{self._name}: {self._domain.name} -> {self._codomain.name}"
    
    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self is other


class Category(ABC):
    """
    A category: a collection of objects and morphisms with composition.
    """
    def __init__(self, name: str):
        self._name = name
        self._objects: Set[Object] = set()
        self._hom_sets: Dict[Tuple[Object, Object], Set[Morphism]] = {}
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def objects(self) -> Set[Object]:
        return self._objects.copy()
    
    def _add_object(self, obj: Object):
        """Internal method to register an object."""
        self._objects.add(obj)
    
    def morphisms(self, source: Object, target: Object) -> Set[Morphism]:
        """Return all morphisms from source to target."""
        return self._hom_sets.get((source, target), set()).copy()
    
    def all_morphisms(self) -> Set[Morphism]:
        """Return all morphisms in the category."""
        result = set()
        for morph_set in self._hom_sets.values():
            result.update(morph_set)
        return result
    
    def _add_morphism(self, morphism: Morphism):
        """Register a morphism in the appropriate hom-set."""
        if morphism.domain not in self._objects:
            raise ValueError(f"Domain {morphism.domain} not in category")
        if morphism.codomain not in self._objects:
            raise ValueError(f"Codomain {morphism.codomain} not in category")
        
        key = (morphism.domain, morphism.codomain)
        if key not in self._hom_sets:
            self._hom_sets[key] = set()
        self._hom_sets[key].add(morphism)
    
    @abstractmethod
    def identity(self, obj: Object) -> Morphism:
        """Return the identity morphism for obj."""
        pass
    
    @abstractmethod
    def compose(self, f: Morphism, g: Morphism) -> Morphism:
        """
        Compose f @ g. 
        Requires: g.codomain == f.domain
        Returns: morphism from g.domain to f.codomain
        """
        pass
    
    def __repr__(self):
        return f"Category({self._name})"
