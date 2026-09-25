from dataclasses import dataclass
from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import combinations
from networkx import DiGraph    

@dataclass(frozen=True)
class Object(ABC):
    name: str

    @abstractmethod
    def __contains__(self, other):
        pass 

    @abstractmethod
    def value(self):
        pass 


@dataclass(frozen=True)
class Morphism(ABC):
    name: str
    domain: Object
    codomain: Object

    def __call__(self, x):
        # validate input in domain
        if x not in self.domain:
            raise ValueError(f"Input {x} not in domain: {self.domain}")
        
        res = self.map(x)

        # validate output in codomain
        if res not in self.codomain:
            raise ValueError(f"Output {res} not in codomain: {self.codomain}")

        return res
    
    def compose(self, other: "Morphism") -> "CompositeMorphism":
        if other.codomain != self.domain:
            raise ValueError(f"Cannot compose morphisms: {other.codomain.name} != {self.domain.name}")

        return CompositeMorphism(
            name=f"{self.name} o {other.name}",
            domain=other.domain,
            codomain=self.codomain,
            morphisms=[other, self]
        )

    @abstractmethod
    def map(self, x):
        pass


class IdentityMorphism(Morphism):
    def map(self, x):
        return x


@dataclass(frozen=True)
class CompositeMorphism(Morphism):
    morphisms: list[Morphism]

    def map(self, x):
        """Compose morphisms on x"""
        for morphism in self.morphisms:
            x = morphism(x)
        return x


class Category(ABC):
    name: str

    @abstractmethod
    def is_object(self, obj) -> bool:
        """Return whether obj is an object of this category."""
        pass

    @abstractmethod
    def is_morphism(self, morphism) -> bool:
        """Return whether morphism belongs to this category."""
        pass

    @abstractmethod
    def hom(self, A, B):
        """Return/represent Hom_C(A, B)."""
        pass

    @abstractmethod
    def identity(self, A):
        """Return the identity morphism id_A."""
        pass

    def compose(self, g, f):
        """Return g ∘ f."""
        if f.codomain != g.domain:
            raise ValueError(
                f"Cannot compose {g.name} ∘ {f.name}: "
                f"{f.codomain} != {g.domain}"
            )

        return g.compose(f)


class ExplicitCategory(Category):

    def __init__(self, name:str):
        self.name = name 
        self.objects = set()
        self._hom = defaultdict(set)

    def __str__(self):
        return f"{type(self).__name__}: {self.name}" 

    def __repr__(self):
        return str(self)

    def add_object(self, obj):
        self.objects.add(obj)

    def add_morphism(self, morphism):
        if morphism.domain not in self.objects:
            raise ValueError(f"Domain {morphism.domain} is not an object of this category.")

        if morphism.codomain not in self.objects:
            raise ValueError(f"Codomain {morphism.codomain} is not an object of this category.")

        self._hom[
            (morphism.domain, morphism.codomain)
        ].add(morphism)

    def is_object(self, obj):
        return obj in self.objects

    def is_morphism(self, morphism):
        return morphism in self._hom.get((morphism.domain, morphism.codomain), set())

    def hom(self, A, B):
        return self._hom.get((A, B), set())

    def identity(self, A):
        return IdentityMorphism(name=f"Id_{A.name}", domain=A, codomain=A)
        

class CategoryAnalyzer:
    def __init__(self, category: Category):
        self.category = category

    def __str__(self):
        return f"Category Analyzer: {str(self.category)}"

    def __repr__(self):
        return str(self)

    @property
    def is_thin(self):
        """Check if category is thin."""
        for object_pair in combinations(self.category.objects, 2):
            if self.category.hom(object_pair[0], object_pair[1]):
                continue 
            elif self.category.hom(object_pair[1], object_pair[0]):
                continue 
            else:
                return False  
        return True


class CategoryGrapher(DiGraph):
    pass 
