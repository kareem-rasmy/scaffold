"""
A category representing propositional logic (Curry-Howard).
Objects are propositions, morphisms are proofs.
"""

from ..core import Category, Object, Morphism, CompositionError
from enum import Enum, auto


class Connective(Enum):
    """Logical connectives as categorical constructs."""
    AND = auto()      # Product
    OR = auto()       # Coproduct
    IMPLIES = auto()  # Exponential
    TRUE = auto()     # Terminal
    FALSE = auto()    # Initial


class Proposition(Object):
    """
    A proposition in a logical system.
    """
    def __init__(self, name: str, category: 'PropLogic', 
                 is_atomic: bool = True, 
                 connective: Connective = None,
                 left: 'Proposition' = None,
                 right: 'Proposition' = None):
        self._is_atomic = is_atomic
        self._connective = connective
        self._left = left
        self._right = right
        super().__init__(name, category)
    
    @property
    def is_atomic(self) -> bool:
        return self._is_atomic
    
    @property
    def connective(self):
        return self._connective
    
    def __repr__(self):
        if self._is_atomic:
            return self.name
        elif self._connective == Connective.AND:
            return f"({self._left} ^ {self._right})"
        elif self._connective == Connective.IMPLIES:
            return f"({self._left} => {self._right})"
        elif self._connective == Connective.TRUE:
            return "Top"
        return self.name


class Proof(Morphism):
    """
    A proof that proposition A entails proposition B.
    Represents a morphism in the logical category.
    """
    def __init__(self, domain: Proposition, codomain: Proposition,
                 rule_name: str, premises: list = None):
        self._rule_name = rule_name
        self._premises = premises or []
        super().__init__(domain, codomain, rule_name)
    
    @property
    def rule_name(self) -> str:
        return self._rule_name
    
    @property
    def premises(self) -> list:
        return self._premises
    
    def compose(self, other: 'Proof') -> 'Proof':
        """
        Composing proofs is cut-elimination: 
        if other proves A |- B and self proves B |- C,
        the composite proves A |- C.
        """
        if not isinstance(other, Proof):
            raise CompositionError("Can only compose Proofs")
        if other.codomain != self.domain:
            raise CompositionError(
                f"Cannot compose proofs: {other.codomain} != {self.domain}"
            )
        
        new_name = f"cut({self._rule_name}, {other._rule_name})"
        return Proof(other.domain, self.codomain, new_name, 
                     premises=[self, other])
    
    def __repr__(self):
        return f"({self.domain} |- {self.codomain} [{self._rule_name}])"


class PropLogic(Category):
    """
    Category of propositions with proofs as morphisms.
    This is a Cartesian Closed Category.
    """
    def __init__(self):
        super().__init__("PropLogic")
        self._truth = None
        self._falsehood = None
    
    @property
    def truth(self) -> Proposition:
        """Terminal object: logical truth Top."""
        if self._truth is None:
            self._truth = Proposition("Top", self, is_atomic=True)
            self._truth._connective = Connective.TRUE
        return self._truth
    
    @property
    def falsehood(self) -> Proposition:
        """Initial object: logical falsehood Bot."""
        if self._falsehood is None:
            self._falsehood = Proposition("Bot", self, is_atomic=True)
            self._falsehood._connective = Connective.FALSE
        return self._falsehood
    
    def atomic(self, name: str) -> Proposition:
        """Create an atomic proposition."""
        return Proposition(name, self, is_atomic=True)
    
    def conjunction(self, A: Proposition, B: Proposition) -> Proposition:
        """Create the product A ^ B."""
        name = f"({A.name}^{B.name})"
        prop = Proposition(name, self, is_atomic=False, 
                          connective=Connective.AND, left=A, right=B)
        # Add product structure: projections
        fst = Proof(prop, A, "pi1")
        snd = Proof(prop, B, "pi2")
        self._add_morphism(fst)
        self._add_morphism(snd)
        return prop
    
    def implication(self, A: Proposition, B: Proposition) -> Proposition:
        """Create the exponential A => B."""
        name = f"({A.name}=>{B.name})"
        return Proposition(name, self, is_atomic=False,
                          connective=Connective.IMPLIES, left=A, right=B)
    
    def axiom(self, A: Proposition) -> Proof:
        """Identity proof: A |- A."""
        proof = Proof(A, A, f"ax_{A.name}")
        self._add_morphism(proof)
        return proof
    
    def prove_implication_intro(self, A: Proposition, B: Proposition,
                                proof_of_b_from_a: Proof) -> Proof:
        """
        =>-Introduction: Given a proof that A |- B, 
        construct a proof that Top |- (A => B).
        """
        impl = self.implication(A, B)
        # This is currying: Hom(A, B) ~= Hom(Top, A=>B)
        global_proof = Proof(self.truth, impl, f"=>I({proof_of_b_from_a.rule_name})")
        self._add_morphism(global_proof)
        return global_proof
    
    def identity(self, obj: Proposition) -> Proof:
        """Identity is the axiom rule."""
        return self.axiom(obj)
    
    def compose(self, f: Proof, g: Proof) -> Proof:
        """Composition is cut elimination."""
        return f.compose(g)
