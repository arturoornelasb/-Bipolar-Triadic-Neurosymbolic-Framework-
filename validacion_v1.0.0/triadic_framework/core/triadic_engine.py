"""
triadic_engine.py v1.1.1 – 2025-11-19
UPDATE: Fix ZeroDivisionError cuando los inputs son cero (manejo de K).
"""

from __future__ import annotations
import math
from fractions import Fraction
from typing import Dict
from dataclasses import dataclass
import logging

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

        ratio = Fraction(C1n * C4n, C2n * C3n)
        a = ratio.numerator
        b = ratio.denominator
        
        if a == 0:
            return TriadicResult(C4, Fraction(0, 1), 0, b, {"a": 0, "b": b, "K": "0"})

        g = math.gcd(a, b)
        a //= g
        b //= g

        K = Fraction(1, a * b)
        return TriadicResult(C4, K, a, b, {"a": a, "b": b, "K": str(K)})
    
    def generative(self, C1: int, C2: int, C3: int, a: int, b: int) -> TriadicResult:
        if b == 0 or C1 == 0:
             raise ValueError("Division by zero in generative mode")
             
        num = a * C2 * C3
        den = b * C1
        
        if num % den != 0: 
            raise ValueError("Result is not an integer")
            
        C4 = num // den
        K = Fraction(1, a * b) if a != 0 else Fraction(0, 1)
        return TriadicResult(C4, K, a, b, {"generative": True})

Triadic = TriadicRelationalFramework
