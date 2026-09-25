from scaffold.categories.base import *
from dataclasses import dataclass
from collections.abc import Set, Callable

"""
Goal: Implement the category of sets. 
Components:
    Objects: Sets
    Morphisms: Functions
"""


class SetObject(Object):
    @abstractmethod
    def contains(self, item) -> bool:
        pass

    def __contains__(self, item) -> bool:
        return self.contains(item)


@dataclass(frozen=True)
class ExplicitSet(SetObject):
    elements: frozenset 

    def contains(self, item):
        return item in self.elements

    @property
    def value(self):
        return self.elements 


class PredicateSet(SetObject):
    predicate: Callable

    def contains(self, item):
        return self.predicate(item)
