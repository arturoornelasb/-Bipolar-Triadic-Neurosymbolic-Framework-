from typing import Tuple, Dict
UnitTuple = Tuple[int, int, int, int, int]

class DimensionalUnit:
    def __init__(self, exponents: UnitTuple = (0, 0, 0, 0, 0)):
        self.exponents = exponents
    def __mul__(self, other: 'DimensionalUnit') -> 'DimensionalUnit':
        return DimensionalUnit(tuple(a + b for a, b in zip(self.exponents, other.exponents)))
    def __truediv__(self, other: 'DimensionalUnit') -> 'DimensionalUnit':
        return DimensionalUnit(tuple(a - b for a, b in zip(self.exponents, other.exponents)))
    def __pow__(self, power: int) -> 'DimensionalUnit':
        return DimensionalUnit(tuple(exp * power for exp in self.exponents))
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DimensionalUnit): return False
        return self.exponents == other.exponents
    def __repr__(self) -> str:
        return str(self.exponents)

M = DimensionalUnit((1, 0, 0, 0, 0))
L = DimensionalUnit((0, 1, 0, 0, 0))
T = DimensionalUnit((0, 0, 1, 0, 0))
I = DimensionalUnit((0, 0, 0, 1, 0))
ONE = DimensionalUnit((0, 0, 0, 0, 0))
ACCEL = L / (T**2)
FORCE = M * ACCEL
ENERGY = FORCE * L
UNITS_MAP: Dict[str, DimensionalUnit] = {
    '1': ONE, 'm': M, 'v2': (L/T)**2, '2KE': ENERGY, 'KE': ENERGY, 'PE': ENERGY, 'E_total': ENERGY
}
