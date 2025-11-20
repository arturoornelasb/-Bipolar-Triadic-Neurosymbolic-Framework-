cd ~/triadic-framework/triadic-framework

cat > triadic_framework/core/dimensional_units.py << 'EOF'
"""
dimensional_units.py v0.6.2 – 2025-11-19
Sistema de unidades dimensionales – CORREGIDO (soporte para potencias)
"""

from typing import Tuple, Dict

UnitTuple = Tuple[int, int, int, int, int]  # M, L, T, I, Θ

class DimensionalUnit:
    def __init__(self, exponents: UnitTuple = (0, 0, 0, 0, 0)):
        self.exponents = exponents

    def __mul__(self, other: 'DimensionalUnit') -> 'DimensionalUnit':
        return DimensionalUnit(tuple(a + b for a, b in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: 'DimensionalUnit') -> 'DimensionalUnit':
        return DimensionalUnit(tuple(a - b for a, b in zip(self.exponents, other.exponents)))

    def __pow__(self, power: int) -> 'DimensionalUnit':
        if not isinstance(power, int):
            raise TypeError("Solo enteros para potencias")
        return DimensionalUnit(tuple(exp * power for exp in self.exponents))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DimensionalUnit):
            return False
        return self.exponents == other.exponents

    def __repr__(self) -> str:
        names = ['M', 'L', 'T', 'I', 'Θ']
        parts = []
        for name, exp in zip(names, self.exponents):
            if exp == 1:
                parts.append(f"[{name}]")
            elif exp > 1:
                parts.append(f"[{name}]^{exp}")
            elif exp == -1:
                parts.append(f"[{name}]^-1")
            elif exp < -1:
                parts.append(f"[{name}]^{exp}")
        return "".join(parts) if parts else "[1]"

# Unidades base
M = DimensionalUnit((1, 0, 0, 0, 0))
L = DimensionalUnit((0, 1, 0, 0, 0))
T = DimensionalUnit((0, 0, 1, 0, 0))
I = DimensionalUnit((0, 0, 0, 1, 0))
Θ = DimensionalUnit((0, 0, 0, 0, 1))
ONE = DimensionalUnit((0, 0, 0, 0, 0))

# Unidades derivadas
ACCEL = L / (T**2)
FORCE = M * ACCEL
ENERGY = FORCE * L
VOLT = ENERGY / (I * T)
OHM = VOLT / I

# Mapeo de variables
UNITS_MAP: Dict[str, DimensionalUnit] = {
    '1': ONE,
    'm': M, 'm1': M, 'm2': M,
    'a': ACCEL,
    'F': FORCE,
    'd': L, 'x': L, 'r': L,
    'W': ENERGY, 'KE': ENERGY, 'PE': ENERGY,
    'V': VOLT,
    'I': I,
    'R': OHM,
    'k': FORCE / L,
    'G': L**3 / (M * T**2),
}
EOF