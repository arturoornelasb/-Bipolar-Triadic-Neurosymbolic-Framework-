import sys
import os
import random
from fractions import Fraction

# Add project root to path
sys.path.append(os.path.abspath('.'))

from triadic_framework.core.concept_mapper import PrimeConceptMapper

def calculate_fuzzy_resonance(val_A, val_B, val_C, val_D):
    """
    Calculates the resonance ratio R = (A * D) / (B * C).
    Ideally R = 1.0 for perfect analogy.
    Returns deviation from 1.0.
    """
    numerator = val_A * val_D
    denominator = val_B * val_C
    
    ratio = numerator / denominator
    deviation = abs(1.0 - ratio)
    
    return ratio, deviation

def run_fuzzy_test():
    print("==========================================")
    print("   EXPERIMENTAL: FUZZY LOGIC & NOISE")
    print("==========================================\n")
    
    mapper = PrimeConceptMapper()
    
    # 1. Setup Perfect Analogy
    # King : Man :: Queen : Woman
    k = mapper.get_concept_value("king")
    m = mapper.get_concept_value("man")
    w = mapper.get_concept_value("woman")
    q = mapper.get_concept_value("queen")
    
    print("1. BASELINE (Perfect Data)")
    # Analogy: King : Man :: Queen : Woman
    # We want (King * Woman) / (Man * Queen) == 1
    # Function computes (A * D) / (B * C)
    # So A=King, B=Man, C=Queen, D=Woman
    
    ratio, dev = calculate_fuzzy_resonance(k, m, q, w)
    print(f"   Ratio: {ratio:.10f}")
    print(f"   Deviation: {dev:.10f}")
    if dev < 1e-9:
        print("   ✅ Perfect Resonance.")
    else:
        print("   ❌ Baseline Error.")
        
    # 2. Introduce Noise
    print("\n2. NOISE INJECTION")
    # Simulate "fuzzy" meaning by multiplying 'Man' by a small noise factor
    
    noise_factor = 1.0000001 # Simulated floating point noise (Measurement Error)
    m_noisy = m * noise_factor
    
    print(f"   Injecting 0.00001% noise into 'Man'...")
    # Pass m_noisy as B
    ratio_n, dev_n = calculate_fuzzy_resonance(k, m_noisy, q, w)
    
    print(f"   Noisy Ratio: {ratio_n:.10f}")
    print(f"   Deviation: {dev_n:.10f}")
    
    if dev_n < 1e-5:
        print("   ✅ SYSTEM ROBUSTNESS: Resonance detected despite noise.")
    else:
        print("   ❌ SYSTEM FRAGILE: Noise broke resonance.")

    # 3. Semantic Drift (Wrong Factor)
    print("\n3. SEMANTIC DRIFT (Wrong Prime)")
    # Multiply 'Man' by prime 2 (e.g., 'Physical') again -> Man^2
    m_drift = m * 2
    
    print(f"   Adding structural drift (Factor * 2)...")
    ratio_d, dev_d = calculate_fuzzy_resonance(k, m_drift, q, w)
    print(f"   Drift Ratio: {ratio_d:.5f}")
    
    if ratio_d == 0.5:
        print("   ✅ DRIFT IDENTIFIED: Exact 0.5 ratio implies missing factor of 2.")
    else:
        print(f"   Unknown Drift.")

if __name__ == "__main__":
    run_fuzzy_test()
