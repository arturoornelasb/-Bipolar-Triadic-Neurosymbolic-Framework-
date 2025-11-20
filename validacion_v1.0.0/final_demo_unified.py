import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from triadic_framework.core.semantic_engine import TriadicRelationalFramework
from triadic_framework.core.concept_mapper import PrimeConceptMapper

def final_unified_demo():
    print("\n===================================================")
    print("   TRIADIC ENGINE v2.0: UNIFIED DEMO (PHYSICS + SEMANTICS)")
    print("===================================================\n")
    
    engine = TriadicRelationalFramework()
    mapper = PrimeConceptMapper()
    
    # --- PART 1: PHYSICS (F = ma) ---
    print("--- PART 1: PHYSICS DOMAIN (F = ma) ---")
    # F = m * a  =>  F/m = a  =>  a = (F * 1) / m
    # Let's use integer values: m=2, a=3 => F=6
    
    val_F = 6
    val_m = 2
    val_a_expected = 3
    
    print(f"Inputs: Force={val_F}, Mass={val_m}")
    print("Applying Triadic Logic: a = (F * 1) / m ...")
    
    # We use analogy_variant for simple ratio: C4 = (C1 * C3) / C2
    # C1=F, C2=m, C3=1 => C4 = F/m
    C4_phys, K_phys, _ = engine.analogy_variant(val_F, val_m, 1)
    
    print(f"Result: Acceleration = {C4_phys}")
    if C4_phys == val_a_expected:
        print("✅ PHYSICS VERIFIED: F=ma holds.")
    else:
        print("❌ PHYSICS FAILED.")

    # --- PART 2: SEMANTICS (King - Man + Woman = Queen) ---
    print("\n--- PART 2: SEMANTIC DOMAIN (Analogy) ---")
    # King : Man :: Queen : Woman
    
    val_king = mapper.get_concept_value("king")
    val_man = mapper.get_concept_value("man")
    val_woman = mapper.get_concept_value("woman")
    
    print(f"Inputs: King={val_king}, Man={val_man}, Woman={val_woman}")
    print("Applying Triadic Logic: Queen = (King * Woman) / Man ...")
    
    C4_sem, K_sem, _ = engine.analogy_variant(val_king, val_man, val_woman)
    result_name = mapper.get_concept_name(C4_sem)
    
    print(f"Result: {result_name} ({C4_sem})")
    if result_name == "queen":
        print("✅ SEMANTICS VERIFIED: Analogy holds.")
    else:
        print("❌ SEMANTICS FAILED.")
        
    # --- PART 3: SCALABILITY (Modular Check) ---
    print("\n--- PART 3: SCALABILITY (Modular Resonance) ---")
    print("Verifying resonance between Physics and Semantics logic...")
    
    # Check if the Semantic result is resonant using Modular Arithmetic
    is_res, _ = engine.modular_resonance(val_king, val_man, val_woman, C4_sem)
    
    if is_res:
        print("✅ MODULAR CHECK PASSED: The engine can verify this without full expansion.")
    
    print("\n===================================================")
    print("   CONCLUSION: ONE ENGINE, TWO WORLDS.")
    print("===================================================")

if __name__ == "__main__":
    final_unified_demo()
