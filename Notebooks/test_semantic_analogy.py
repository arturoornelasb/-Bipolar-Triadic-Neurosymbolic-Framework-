import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from triadic_framework.core.semantic_engine import TriadicRelationalFramework
from triadic_framework.core.concept_mapper import PrimeConceptMapper

def test_king_queen_analogy():
    print("\n--- TEST: King - Man + Woman = Queen (Triadic Logic) ---")
    
    # 1. Initialize Engine and Mapper
    engine = TriadicRelationalFramework()
    mapper = PrimeConceptMapper()
    
    # 2. Get Integer Values for Concepts
    try:
        val_king = mapper.get_concept_value("king")
        val_man = mapper.get_concept_value("man")
        val_woman = mapper.get_concept_value("woman")
        val_queen_expected = mapper.get_concept_value("queen")
        
        print(f"King Value: {val_king} (Factors: {mapper.get_attributes_from_value(val_king)})")
        print(f"Man Value: {val_man} (Factors: {mapper.get_attributes_from_value(val_man)})")
        print(f"Woman Value: {val_woman} (Factors: {mapper.get_attributes_from_value(val_woman)})")
        print(f"Queen (Expected): {val_queen_expected} (Factors: {mapper.get_attributes_from_value(val_queen_expected)})")
        
        # 3. Apply Analogy Logic: C4 = (C1 * C3) / C2
        # "King is to Man as Queen is to Woman" -> King/Man = Queen/Woman -> Queen = (King * Woman) / Man
        # OR "King - Man + Woman" -> (King * Woman) / Man
        
        print("\nApplying Triadic Analogy: (King * Woman) / Man ...")
        C4, K, steps = engine.analogy_variant(val_king, val_man, val_woman)
        
        print(f"Result C4: {C4}")
        print(f"Simplicity K: {K}")
        
        # 4. Verify Result
        result_name = mapper.get_concept_name(C4)
        print(f"Result Concept Name: {result_name}")
        
        if C4 == val_queen_expected:
            print("\n✅ SUCCESS: The engine correctly derived 'Queen' from 'King - Man + Woman'.")
        else:
            print(f"\n❌ FAILURE: Expected {val_queen_expected} ('queen'), got {C4} ('{result_name}').")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_king_queen_analogy()
