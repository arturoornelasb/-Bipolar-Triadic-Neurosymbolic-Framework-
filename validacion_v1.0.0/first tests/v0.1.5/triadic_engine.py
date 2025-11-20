
"""
triadic_engine.py v0.1.5 – 2025-11-18
Author: José Arturo Ornelas Brand
Update: Simplified discovery for multiplicative relations; ready for Euclid's theorem experiment
"""

from __future__ import annotations
import math
from fractions import Fraction
from typing import Dict
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TriadicResult:
    output: int
    simplicity: Fraction
    a: int
    b: int
    steps: Dict[str, any]

class TriadicRelationalFramework:
    @staticmethod
    def discovery(C1: int, C2: int, C3: int, C4: int) -> TriadicResult:
        if not all(isinstance(x, int) and x >= 0 for x in [C1, C2, C3, C4]):
            raise ValueError("Inputs must be non-negative integers")
        
        gcd = math.gcd(C1, C2, C3, C4) or 1
        C1n = C1 // gcd
        C2n = C2 // gcd
        C3n = C3 // gcd
        C4n = C4 // gcd
        
        if C2n == 0 or C3n == 0:
            raise ValueError("C2 or C3 cannot be zero after normalization")

        # Ratio for a/b = (C1 * C4) / (C2 * C3)  -- corrected for standard balancing
        ratio = Fraction(C1n * C4n, C2n * C3n)
        a = ratio.numerator
        b = ratio.denominator
        g = math.gcd(a, b)
        a //= g
        b //= g

        K = Fraction(1, a * b)
        logger.info(f"Φ_D discovered a={a}, b={b} → K={K}")
        return TriadicResult(C4, K, a, b, {"a": a, "b": b, "K": str(K)})

Triadic = TriadicRelationalFramework