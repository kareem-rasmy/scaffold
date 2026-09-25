from scaffold.categories.base import *
from scaffold.fields.set_theory.objects import *
from dataclasses import dataclass
from collections.abc import Callable


@dataclass(frozen=True)
class SetMorphism(Morphism):
    function: Callable

    def map(self, x: SetObject):    
        return self.function(x)
