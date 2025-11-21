import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from triadic_framework.core.buss_bridge import BussBridge
from triadic_framework.core.concept_mapper import PrimeConceptMapper

def test_buss_sentiment():
    print("\n--- TEST: BUSS Sentiment Logic (Prime Factors) ---")
    
    bridge = BussBridge()
    mapper = PrimeConceptMapper()
    
    # Test Concepts
    concepts = ["hero", "villain", "victim", "man"]
    
    for word in concepts:
        val = mapper.get_concept_value(word)
        sentiment = bridge.project_concept(val, "SENTIMENT")
        power = bridge.project_concept(val, "POWER")
        
        print(f"Concept: '{word}'")
        print(f"  - Value: {val}")
        print(f"  - Sentiment: {sentiment}")
        print(f"  - Power: {power}")
        
        # Verification Logic
        if word == "hero":
            if sentiment == "POSITIVE" and power == "POWERFUL":
                print("  ✅ Correctly identified as Positive/Powerful.")
            else:
                print("  ❌ Failed identification.")
        elif word == "villain":
             if sentiment == "NEGATIVE" and power == "POWERFUL":
                print("  ✅ Correctly identified as Negative/Powerful.")
        elif word == "victim":
             if sentiment == "NEGATIVE" and power == "WEAK":
                print("  ✅ Correctly identified as Negative/Weak.")
        elif word == "man":
             if sentiment == "NEUTRAL":
                print("  ✅ Correctly identified as Neutral.")

if __name__ == "__main__":
    test_buss_sentiment()
