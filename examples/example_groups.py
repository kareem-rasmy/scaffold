"""
Examples demonstrating the category of groups.
"""

from scaffold import Grp


def example_cyclic_groups():
    """Demonstrate homomorphisms between cyclic groups."""
    print("=" * 50)
    print("Example: Cyclic Groups and Homomorphisms")
    print("=" * 50)
    
    C = Grp()
    
    # Z_2: {0, 1} with addition mod 2
    Z2 = C.create_object("Z₂", {0, 1}, lambda a, b: (a + b) % 2, 0)
    
    # Z_4: {0, 1, 2, 3} with addition mod 4
    Z4 = C.create_object("Z₄", {0, 1, 2, 3}, lambda a, b: (a + b) % 4, 0)
    
    # Homomorphism Z₄ → Z₂: reduction mod 2
    def mod2_reduction(x):
        return x % 2
    
    phi = C.create_morphism(Z4, Z2, mod2_reduction, "mod2")
    
    # Verify homomorphism properties
    print(f"Z₂ = {Z2}")
    print(f"Z₄ = {Z4}")
    print(f"\nφ: Z₄ → Z₂")
    for x in Z4.elements:
        print(f"  φ({x}) = {phi(x)}")
    
    # Check that φ(x + y) = φ(x) + φ(y) for a few examples
    print("\nHomomorphism property check:")
    for a, b in [(1, 2), (3, 1), (2, 3)]:
        lhs = phi(Z4.operate(a, b))
        rhs = Z2.operate(phi(a), phi(b))
        print(f"  φ({a} + {b} mod 4) = φ({Z4.operate(a, b)}) = {lhs}")
        print(f"  φ({a}) + φ({b}) mod 2 = {phi(a)} + {phi(b)} mod 2 = {rhs}")
        print(f"  Equal? {lhs == rhs}")


if __name__ == "__main__":
    example_cyclic_groups()
