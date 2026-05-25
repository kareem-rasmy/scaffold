"""
Examples demonstrating the category FinSet.
"""

from scaffold import FinSet

def example_product_construction():
    """Demonstrate the product (Cartesian product) in FinSet."""
    print("=" * 50)
    print("Example 1: Product in FinSet")
    print("=" * 50)
    
    C = FinSet()
    
    # Create two sets
    A = C.create_object("A", {"a1", "a2"})
    B = C.create_object("B", {"b1", "b2", "b3"})
    
    # Create their Cartesian product
    A_x_B_elements = {(a, b) for a in A.elements for b in B.elements}
    A_x_B = C.create_object("A×B", A_x_B_elements)
    
    # Create projections
    pi1 = C.create_morphism(A_x_B, A, 
                           {(a, b): a for (a, b) in A_x_B_elements},
                           "π₁")
    pi2 = C.create_morphism(A_x_B, B,
                           {(a, b): b for (a, b) in A_x_B_elements},
                           "π₂")
    
    # Now demonstrate the universal property
    # Create a test object X with maps to A and B
    X = C.create_object("X", {"x1", "x2"})
    f = C.create_morphism(X, A, {"x1": "a1", "x2": "a2"}, "f")
    g = C.create_morphism(X, B, {"x1": "b1", "x2": "b2"}, "g")
    
    # The unique mediating morphism ⟨f, g⟩
    mediating = C.create_morphism(X, A_x_B, 
                                  {"x1": ("a1", "b1"), "x2": ("a2", "b2")},
                                  "⟨f,g⟩")
    
    # Verify: π₁ ∘ ⟨f,g⟩ = f and π₂ ∘ ⟨f,g⟩ = g
    left = pi1 @ mediating  # π₁ ∘ ⟨f,g⟩
    right = pi2 @ mediating  # π₂ ∘ ⟨f,g⟩
    
    print(f"A = {A.elements}")
    print(f"B = {B.elements}")
    print(f"A×B = {A_x_B.elements}")
    print(f"\nπ₁ = {pi1}")
    print(f"π₂ = {pi2}")
    print(f"\nTest object X = {X.elements}")
    print(f"f: X→A = {f.mapping}")
    print(f"g: X→B = {g.mapping}")
    print(f"⟨f,g⟩: X→A×B = {mediating.mapping}")
    print(f"\nVerification:")
    print(f"  π₁ ∘ ⟨f,g⟩ = {left.mapping} == f = {f.mapping} ? {left.mapping == f.mapping}")
    print(f"  π₂ ∘ ⟨f,g⟩ = {right.mapping} == g = {g.mapping} ? {right.mapping == g.mapping}")


def example_initial_terminal():
    """Demonstrate initial and terminal objects."""
    print("\n" + "=" * 50)
    print("Example 2: Initial and Terminal Objects")
    print("=" * 50)
    
    C = FinSet()
    
    terminal = C.terminal
    initial = C.initial
    
    print(f"Terminal object: {terminal}")
    print(f"Initial object: {initial}")
    
    # Create another set
    A = C.create_object("A", {"x", "y", "z"})
    
    # There is exactly one function from A to terminal
    unique_to_terminal = C.create_morphism(
        A, terminal,
        {a: "*" for a in A.elements},
        f"!_{A.name}"
    )
    print(f"\nUnique morphism from {A.name} to terminal: {unique_to_terminal}")
    
    # There is exactly one function from initial to A (the empty function)
    unique_from_initial = C.create_morphism(
        initial, A,
        {},  # empty mapping
        f"!^{A.name}"
    )
    print(f"Unique morphism from initial to {A.name}: {unique_from_initial}")


def example_composition():
    """Demonstrate morphism composition."""
    print("\n" + "=" * 50)
    print("Example 3: Composition")
    print("=" * 50)
    
    C = FinSet()
    
    A = C.create_object("A", {1, 2, 3})
    B = C.create_object("B", {"x", "y"})
    C_obj = C.create_object("C", {True, False})
    
    f = C.create_morphism(A, B, {1: "x", 2: "y", 3: "x"}, "f")
    g = C.create_morphism(B, C_obj, {"x": True, "y": False}, "g")
    
    # Compose g ∘ f
    h = g @ f
    print(f"f: {f.mapping}")
    print(f"g: {g.mapping}")
    print(f"g ∘ f: {h.mapping}")
    print(f"  h(1) = {h(1)} == g(f(1)) = g('x') = {g('x')}")
    print(f"  h(2) = {h(2)} == g(f(2)) = g('y') = {g('y')}")
    print(f"  h(3) = {h(3)} == g(f(3)) = g('x') = {g('x')}")


if __name__ == "__main__":
    example_product_construction()
    example_initial_terminal()
    example_composition()
