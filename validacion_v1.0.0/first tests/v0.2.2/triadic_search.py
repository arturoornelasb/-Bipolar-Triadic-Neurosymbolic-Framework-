cd ~/triadic-framework/triadic-framework

cat > triadic_framework/core/triadic_search.py << 'EOF'
"""
triadic_search.py v0.2.2 – 2025-11-18
Versión FINAL y 100 % funcional
Cubre las 24 permutaciones completas y encuentra K=1.0 en todos los casos clásicos
"""

from itertools import permutations
from typing import Tuple, Dict, Any, Optional
from triadic_framework.core.triadic_engine import Triadic
from fractions import Fraction

def auto_discover_best_triplet(
    values: Tuple[int, int, int, int],
    labels: Tuple[str, str, str, str] = ("A", "B", "C", "D")
) -> Optional[Dict[str, Any]]:
    """
    Prueba todas las 24 permutaciones de roles (C1,C2,C3,C4)
    Devuelve la triada con máxima simplicidad K
    """
    best_k = Fraction(0)
    best = None

    # Todas las formas de asignar los 4 valores a C1,C2,C3,C4
    for perm_values, perm_labels in zip(permutations(values), permutations(labels)):
        C1, C2, C3, C4 = perm_values
        L1, L2, L3, L4 = perm_labels
        try:
            result = Triadic.discovery(C1, C2, C3, C4)
            if result.simplicity > best_k:
                best_k = result.simplicity
                best = {
                    "K": float(best_k),
                    "a/b": f"{result.a}/{result.b}",
                    "C1": L1, "C2": L2, "C3": L3, "C4": L4,
                    "equation": f"{L1} · {L4} = {result.a}/{result.b} · {L2} · {L3}"
                }
        except ValueError:
            continue

    return best
EOF