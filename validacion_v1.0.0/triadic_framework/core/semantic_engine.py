import math
from fractions import Fraction
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TriadicRelationalFramework:
    """
    Implementation of the Triadic Relational Framework for Semantic Logic.
    Based on 'A Rigorous Triadic Framework for Neurosymbolic Reasoning'.
    """
    def __init__(self):
        pass 

    def compute_triad(self, C1, C2, C3, a, b):
        """
        Compute the triadic relational transformation: C4 = (a * C2 * C3) / (b * C1)
        
        Parameters:
        - C1, C2, C3: Input integer concepts
        - a, b: Positive integer balancing coefficients (minimal, co-prime)

        Returns:
        - C4: The computed output integer
        - K: The simplicity constant (Fraction: 1 / (a * b))
        - steps: Dictionary with intermediate steps for transparency
        """
        if not all(isinstance(x, int) and x > 0 for x in [C1, C2, C3, a, b]):
            raise ValueError("All inputs must be positive integers.")

        steps = {}

        # Step 1: Input Concepts
        steps['inputs'] = {'C1': C1, 'C2': C2, 'C3': C3, 'a': a, 'b': b}

        # Step 2: Normalization
        gcd_in = math.gcd(C1, C2, C3)
        C1_prime = C1 // gcd_in
        C2_prime = C2 // gcd_in
        C3_prime = C3 // gcd_in
        steps['normalization'] = {'gcd_in': gcd_in, 'C1_prime': C1_prime, 'C2_prime': C2_prime, 'C3_prime': C3_prime}

        # Step 3: Relational Transformation (Phi)
        # Formula: a * C2' * C3' = b * C1' * C4'  => C4' = (a * C2' * C3') / (b * C1')
        numerator = a * C2_prime * C3_prime
        denominator = b * C1_prime
        
        if denominator == 0:
             raise ValueError("Denominator is zero.")

        C4_prime = Fraction(numerator, denominator)
        steps['transformation'] = {'C4_prime': str(C4_prime)}

        # Step 4: Denormalization
        C4 = C4_prime * gcd_in
        
        if C4.denominator != 1:
            # This is a crucial check: The logic fails if the result is not an integer concept
            raise ValueError(f"The balancing does not result in an integer C4. Result: {C4}. Adjust inputs or rule (a,b).")
            
        C4 = int(C4) 
        steps['denormalization'] = {'C4': C4}

        # Simplicity K
        K = Fraction(1, a * b)
        steps['K'] = str(K)

        return C4, K, steps

    def analogy_variant(self, C1, C2, C3):
        """
        Variant for analogies like King:Man :: Queen:Woman.
        Logic: "Remove C2 from C1, add C3".
        In Ratio Logic: C4 = (C1 * C3) / C2.
        
        Parameters:
        - C1: Starting concept (e.g., King)
        - C2: To remove (e.g., Man/Male)
        - C3: To add (e.g., Woman/Female)

        Returns:
        - C4: Predicted concept (e.g., Queen)
        - K: Simplicity (always 1.0 for direct analogy)
        - steps: Dictionary with intermediate steps
        """
        if not all(isinstance(x, int) and x > 0 for x in [C1, C2, C3]):
            raise ValueError("All inputs must be positive integers.")

        steps = {}
        steps['inputs'] = {'C1': C1, 'C2': C2, 'C3': C3}

        # Normalization (over inputs)
        gcd_in = math.gcd(C1, C2, C3)
        C1_prime = C1 // gcd_in
        C2_prime = C2 // gcd_in
        C3_prime = C3 // gcd_in
        steps['normalization'] = {'gcd_in': gcd_in, 'C1_prime': C1_prime, 'C2_prime': C2_prime, 'C3_prime': C3_prime}

        # Analogy transformation: C4_prime = (C1_prime * C3_prime) / C2_prime
        numerator = C1_prime * C3_prime
        denominator = C2_prime
        
        C4_prime = Fraction(numerator, denominator)
        steps['transformation'] = {'C4_prime': str(C4_prime)}
        
        # Denormalization
        C4 = C4_prime * gcd_in
        
        if C4.denominator != 1:
            raise ValueError(f"The analogy does not result in an integer output ({C4}). Check attribute mappings.")
            
        C4 = int(C4)
        steps['denormalization'] = {'C4': C4}

        # For analogy, a=1, b=1 implicitly
        K = Fraction(1, 1) 
        steps['K'] = str(K)
        
        return C4, K, steps

    def modular_resonance(self, C1, C2, C3, C4, modulus=10**9 + 7):
        """
        Check resonance using Modular Arithmetic: (C1 * C4) % P == (C2 * C3) % P.
        This allows verifying relationships between huge concepts using fixed-size integers.
        
        Parameters:
        - C1, C2, C3, C4: Input integers (can be huge)
        - modulus: A large prime (default: 10^9 + 7)
        
        Returns:
        - is_resonant: Boolean
        - remainder_diff: 0 if resonant
        """
        # We assume a=1, b=1 for pure semantic analogy
        
        lhs = (C1 * C4) % modulus
        rhs = (C2 * C3) % modulus
        
        return (lhs == rhs), abs(lhs - rhs)


    def check_static_balance(self, C1, C2, C3, C4):
        """
        Check static balance for existing formula (find minimal co-prime a,b such that a C2' C3' = b C1' C4').
        
        Parameters:
        - C1, C2, C3, C4: Positive integers
        
        Returns:
        - a, b: Minimal co-prime balancing coefficients
        - K: Simplicity (1 / (a * b))
        - steps: Dictionary with steps
        """
        if not all(isinstance(x, int) and x > 0 for x in [C1, C2, C3, C4]):
            raise ValueError("All inputs must be positive integers.")

        steps = {'inputs': {'C1': C1, 'C2': C2, 'C3': C3, 'C4': C4}}
        
        gcd_in = math.gcd(C1, C2, C3, C4)
        C1_prime = C1 // gcd_in
        C2_prime = C2 // gcd_in
        C3_prime = C3 // gcd_in
        C4_prime = C4 // gcd_in
        steps['normalization'] = {'gcd_in': gcd_in, 'C1_prime': C1_prime, 'C2_prime': C2_prime,
            'C3_prime': C3_prime, 'C4_prime': C4_prime}

        # Ratio: a/b = (C1' * C4') / (C2' * C3')
        ratio = Fraction(C1_prime * C4_prime, C2_prime * C3_prime)
        a = ratio.numerator
        b = ratio.denominator
        
        # Ensure a,b are minimal (Fraction does this automatically, but explicit check doesn't hurt)
        gcd_ab = math.gcd(a, b)
        a //= gcd_ab
        b //= gcd_ab
        steps['balancing'] = {'a': a, 'b': b}
        
        K = Fraction(1, a * b)
        steps['K'] = str(K)
        
        return a, b, K, steps
