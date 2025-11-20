import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from triadic_framework.core.semantic_engine import TriadicRelationalFramework
from triadic_framework.core.concept_mapper import PrimeConceptMapper

def test_modular_scaling():
    print("\n--- TEST: Modular Resonance (Scaling Test) ---")
    
    engine = TriadicRelationalFramework()
    mapper = PrimeConceptMapper()
    
    # 1. Create a "Complex" Concept (Simulated)
    # Let's imagine a concept with 50 attributes (which we know explodes)
    # We simulate this by multiplying many primes manually
    
    print("Generating huge concepts (50+ primes)...")
    
    # Concept A: Huge Number
    huge_primes_A = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71] * 3
    val_A = 1
    for p in huge_primes_A: val_A *= p
    
    # Concept B: Another Huge Number (A * 2)
    val_B = val_A * 2
    
    # Concept C: Small Number (3)
    val_C = 3
    
    # Concept D: Expected Result (B * C / A) = (A * 2 * 3) / A = 6
    val_D_expected = 6
    
    print(f"Value A (approx): {float(val_A):.2e} (Bits: {val_A.bit_length()})")
    
    # 2. Test Standard Logic (Might be slow, but Python handles it)
    print("\nTesting Standard Logic...")
    try:
        # Analogy: A : B :: C : D  => A/B = C/D => D = (B*C)/A
        # We use our analogy_variant: C4 = (C1 * C3) / C2
        # Here: C1=B, C2=A, C3=C => D = (B*C)/A
        C4, K, _ = engine.analogy_variant(val_B, val_A, val_C)
        print(f"Standard Result: {C4}")
    except Exception as e:
        print(f"Standard Logic Failed: {e}")
        
    # 3. Test Modular Logic
    print("\nTesting Modular Logic (Modulus = 10^9 + 7)...")
    is_resonant, diff = engine.modular_resonance(val_A, val_B, val_C, val_D_expected)
    # Note: modular_resonance checks (C1 * C4) == (C2 * C3)
    # Here: (A * D) == (B * C) ?
    # (A * 6) == (A*2 * 3) == (A * 6). YES.
    
    if is_resonant:
        print(f"✅ MODULAR SUCCESS: Resonance verified without full expansion.")
    else:
        print(f"❌ MODULAR FAILURE: Diff {diff}")

if __name__ == "__main__":
    test_modular_scaling()
