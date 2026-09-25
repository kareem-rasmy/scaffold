from scaffold.categories.base import *


class SetCategory(ExplicitCategory):
    def __init__(self, name: str, objects=[], morphisms=[]):
        super().__init__(name)

        # add objects
        for obj in objects:
            self.add_object(obj)

        # add morphisms
        for morphism in morphisms:
            self.add_morphism(morphism)
