import math
import sys

def estimate_concept_size(num_attributes):
    """
    Estimates the magnitude of a concept's integer value based on the number of attributes.
    Assumes attributes are mapped to the first N primes.
    """
    # 1. Generate first N primes
    primes = []
    candidate = 2
    while len(primes) < num_attributes:
        is_prime = True
        for p in primes:
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
        
    # 2. Calculate Product (Worst Case: A concept has ALL first N attributes)
    # In reality, a concept has a subset, but we want to see the magnitude of the "Basis".
    
    # Let's assume a concept has 'k' attributes.
    # We'll test for a concept having the *average* prime value, or just the first k primes.
    
    # Scenario A: Concept has the first k primes (Dense concept)
    product = 1
    for p in primes:
        product *= p
        
    return product, primes[-1]

def run_analysis():
    print("--- SCALABILITY ANALYSIS: Integer Explosion Risk ---\n")
    print(f"{'Attributes':<15} | {'Max Prime':<10} | {'Concept Value (Approx)':<30} | {'Bits Needed':<15}")
    print("-" * 80)
    
    scenarios = [5, 10, 20, 50, 100]
    
    for k in scenarios:
        val, max_p = estimate_concept_size(k)
        bits = val.bit_length()
        
        # Format value for readability
        val_str = f"{val:.2e}" if val > 1e15 else str(val)
        
        print(f"{k:<15} | {max_p:<10} | {val_str:<30} | {bits:<15}")

    print("\n--- CONCLUSION ---")
    print("Standard 64-bit integers can hold up to ~1.8e19 (approx 64 bits).")
    print("Python handles arbitrarily large integers, but computation speed (multiplication/division)")
    print("and storage will degrade as concepts become more complex.")
    
if __name__ == "__main__":
    run_analysis()
