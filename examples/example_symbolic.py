"""
Examples demonstrating the symbolic enhancements with SymPy.
"""

from scaffold.symbolic import (
    SymbolicFinSet, SymbolicSetObject, SymbolicSetMorphism,
    SymbolicPropLogic, SymbolicProposition, SymbolicProof,
    UniversalPropertyVerifier, CategoryPrinter,
    enable_notebook_display
)
from sympy import (
    symbols, Lambda, FiniteSet, Interval, oo, 
    sin, cos, exp, log, And, Or, Not, Implies
)


def example_infinite_sets():
    """Demonstrate working with infinite sets symbolically."""
    print("=" * 60)
    print("EXAMPLE: Symbolic Infinite Sets")
    print("=" * 60)
    
    C = SymbolicFinSet()
    
    # Create the real numbers as an object
    x = symbols('x')
    R = C.create_symbolic_set("R", condition=x >= -oo)
    
    # Create the interval [0, 1]
    unit_interval = C.create_symbolic_set("[0,1]", expr=Interval(0, 1))
    
    # Create a morphism f: R -> [0,1] using sigmoid
    sigmoid = Lambda(x, 1 / (1 + exp(-x)))
    f = C.create_symbolic_morphism(R, unit_interval, sigmoid, "sigma")
    
    print(f"Category: {C.name}")
    print(f"Object R: {R}")
    print(f"Object [0,1]: {unit_interval}")
    print(f"\nMorphism: {f}")
    print(f"\nComposing with identity:")
    print(f"  sigma @ id = {f @ R.identity()}")
    
    # Create another function
    square = Lambda(x, x**2)
    g = C.create_symbolic_morphism(unit_interval, unit_interval, square, "sq")
    
    # Compose
    h = g @ f  # square after sigmoid
    print(f"\nComposition sq @ sigma: {h}")
    print(f"  This represents: x ↦ (1/(1+e^(-x)))²")


def example_automatic_proof_verification():
    """Use SymPy to automatically verify logical proofs."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Automatic Theorem Proving with SymPy")
    print("=" * 60)
    
    L = SymbolicPropLogic()
    
    # Create atomic propositions
    P = L.atomic("P")
    Q = L.atomic("Q")
    
    # Build: (P ^ Q) => P
    P_and_Q = L.conjunction(P, Q)
    theorem = L.implication(P_and_Q, P)
    
    print(f"Proposition: {theorem}")
    print(f"SymPy form: {theorem.sympy_expression}")
    
    # Check if it's a tautology (classical logic theorem)
    is_tautology = L.is_theorem(theorem)
    print(f"\nIs it a classical tautology? {is_tautology}")
    
    # Build a non-theorem: (P ^ Q) => (~P)
    not_P = L.negation(P)
    non_theorem = L.implication(P_and_Q, not_P)
    
    print(f"\nProposition: {non_theorem}")
    print(f"SymPy form: {non_theorem.sympy_expression}")
    
    is_tautology = L.is_theorem(non_theorem)
    print(f"Is it a classical tautology? {is_tautology}")
    
    # Build Modus Ponens: (P ^ (P => Q)) => Q
    P_implies_Q = L.implication(P, Q)
    premise = L.conjunction(P, P_implies_Q)
    modus_ponens = L.implication(premise, Q)
    
    print(f"\nModus Ponens: {modus_ponens}")
    print(f"SymPy form: {modus_ponens.sympy_expression}")
    print(f"Is it a tautology? {L.is_theorem(modus_ponens)}")


def example_universal_property_verification():
    """Use SymPy to verify universal properties automatically."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Symbolic Universal Property Verification")
    print("=" * 60)
    
    C = SymbolicFinSet()
    verifier = UniversalPropertyVerifier()
    
    # Create sets
    x = symbols('x')
    A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
    B = C.create_symbolic_set("B", expr=FiniteSet(4, 5))
    
    # Create product set
    product_elements = set()
    for a in A.elements:
        for b in B.elements:
            product_elements.add((a, b))
    P = C.create_symbolic_set("AxB", expr=FiniteSet(*product_elements))
    
    # Create projections symbolically
    pi1_func = Lambda((symbols('a'), symbols('b')), symbols('a'))
    pi2_func = Lambda((symbols('a'), symbols('b')), symbols('b'))
    
    # Simplified: use concrete mapping for this example
    pi1 = C.create_morphism(P, A, {(a,b): a for (a,b) in product_elements}, "pi1")
    pi2 = C.create_morphism(P, B, {(a,b): b for (a,b) in product_elements}, "pi2")
    
    # Verify product
    result = verifier.verify_product(C, A, B, P, pi1, pi2)
    print(f"\nFinal result: {'✓ VERIFIED' if result else '✗ FAILED'}")
    
    # Verify terminal object
    terminal = C.terminal
    result = verifier.verify_terminal(C, terminal)
    print(f"\nFinal result: {'✓ VERIFIED' if result else '✗ FAILED'}")


def example_pretty_printing():
    """Demonstrate enhanced pretty printing."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Pretty Printing with SymPy")
    print("=" * 60)
    
    printer = CategoryPrinter()
    
    # Propositional logic example
    L = SymbolicPropLogic()
    P = L.atomic("P")
    Q = L.atomic("Q")
    R = L.atomic("R")
    
    complex_prop = L.implication(
        L.conjunction(P, Q),
        L.disjunction(R, L.negation(P))
    )
    
    printer.print_object(complex_prop)
    
    # Set category example
    C = SymbolicFinSet()
    A = C.create_symbolic_set("A", expr=FiniteSet(1, 2, 3))
    B = C.create_symbolic_set("B", expr=FiniteSet(1, 2, 3))
    
    # Create identity and some morphisms
    id_A = A.identity()
    x = symbols('x')
    double = C.create_symbolic_morphism(A, B, Lambda(x, x*2), "double")
    
    printer.print_morphism(double)
    printer.print_category(C)


def example_curry_howard_with_verification():
    """
    The Curry-Howard correspondence with automatic verification:
    Prove A => A and verify it's a theorem.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Curry-Howard with Auto-Verification")
    print("=" * 60)
    
    L = SymbolicPropLogic()
    
    A = L.atomic("A")
    A_implies_A = L.implication(A, A)
    
    # Create the proof (identity morphism)
    id_A = L.axiom(A)
    
    # Convert to global element: 1 -> (A => A)
    proof = L.prove_implication_intro(A, A, id_A)
    
    print(f"Theorem: |- {A_implies_A}")
    print(f"Proof: {proof}")
    
    # Verify syntactically (the proof was constructed correctly)
    print(f"\nSyntactic verification: proof constructed by =>-introduction rule")
    
    # Verify semantically using SymPy (is it a tautology?)
    is_theorem = L.is_theorem(A_implies_A)
    print(f"Semantic verification (tautology check): {is_theorem}")
    
    # Now prove something that's NOT constructively valid
    # but IS classically valid: ~~A => A (double negation elimination)
    not_not_A = L.negation(L.negation(A))
    dne = L.implication(not_not_A, A)
    
    print(f"\nDouble Negation Elimination: {dne}")
    print(f"Classical tautology? {L.is_theorem(dne)}")
    print(f"Constructively valid? This requires excluded middle,")
    print(f"which is not available in intuitionistic logic (CCC).")
    print(f"This demonstrates the distinction between classical and")
    print(f"intuitionistic logic in categorical semantics!")


if __name__ == "__main__":
    # example_infinite_sets()
    example_automatic_proof_verification()
    example_universal_property_verification()
    example_pretty_printing()
    example_curry_howard_with_verification()
    
    print("\n" + "=" * 60)
    print("SYMPY ENHANCEMENTS SUMMARY")
    print("=" * 60)
    print("""
SymPy adds the following capabilities:

1. INFINITE OBJECTS: Represent R, intervals, and other
   infinite sets as categorical objects.

2. SYMBOLIC MORPHISMS: Define functions using SymPy Lambdas
   instead of exhaustive mappings.

3. AUTOMATIC VERIFICATION: Use SAT solvers to check if a
   proposition is a theorem (tautology).

4. PRETTY PRINTING: LaTeX output for Jupyter notebooks and
   mathematical notation in terminals.

5. COMPOSITION: Automatic function composition with symbolic
   simplification (e.g., (f @ g)(x) = f(g(x))).

6. UNIVERSAL PROPERTY CHECKING: Instead of exhaustive iteration,
   use equation solving to verify universal constructions.

7. CLASSICAL vs INTUITIONISTIC: The SAT solver checks classical
   validity, while categorical constructions give intuitionistic
   proofs - showing the distinction clearly.
    """)
