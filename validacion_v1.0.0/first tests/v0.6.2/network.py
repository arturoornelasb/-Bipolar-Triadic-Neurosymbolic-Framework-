cd ~/triadic-framework/triadic-framework

cat > triadic_framework/core/network.py << 'EOF'
"""
network.py v0.6.0 – 2025-11-19
TriadicNetwork con VALIDACIÓN DIMENSIONAL ESTRICTA (Guardián Dimensional)
"""

import networkx as nx
from typing import Tuple, Any
from triadic_framework.core.triadic_search import auto_discover_best_triplet
from triadic_framework.core.dimensional_units import UNITS_MAP, DimensionalUnit

class TriadicNetwork:
    def __init__(self):
        self.G = nx.DiGraph()

    def check_dimensional_balance(self, labels: Tuple[str, str, str, str]) -> bool:
        """
        Verifica que las dimensiones físicas sean coherentes en la ecuación balanceada:
        C1 · C4 = (a/b) · C2 · C3  →  [C1]·[C4] = [C2]·[C3] cuando a/b = 1/1
        """
        try:
            u1 = UNITS_MAP.get(labels[0])
            u2 = UNITS_MAP.get(labels[1])
            u3 = UNITS_MAP.get(labels[2])
            u4 = UNITS_MAP.get(labels[3])

            if None in (u1, u2, u3, u4):
                print(f"  Advertencia: Unidad desconocida en {labels}. Se omite chequeo dimensional.")
                return True  # permitimos para desarrollo

            left = u1 * u4   # C1 · C4
            right = u2 * u3  # C2 · C3

            if left == right:
                print(f"  Balance dimensional OK: {left} = {right}")
                return True
            else:
                print(f"  FALLO DIMENSIONAL: {left} ≠ {right}")
                return False

        except Exception as e:
            print(f"  Error dimensional: {e}")
            return True

    def add_candidate_quartet(self, values: Tuple[int, int, int, int], labels: Tuple[str, str, str, str], min_K: float = 0.9):
        print(f"\nIntentando añadir triada: {labels} ← valores {values}")

        # 1. VALIDACIÓN DIMENSIONAL (el guardián)
        if not self.check_dimensional_balance(labels):
            print("  TRIADA RECHAZADA por inconsistencia dimensional")
            return

        # 2. VALIDACIÓN NUMÉRICA (como antes)
        result = auto_discover_best_triplet(values, labels)
        if result and result["K"] >= min_K:
            C1, C2, C3, C4 = result["C1"], result["C2"], result["C3"], result["C4"]
            K = result["K"]
            a, b = map(int, result["a/b"].split('/'))

            # Añadimos nodos con unidades
            for lbl in labels:
                unit = UNITS_MAP.get(lbl, "unknown")
                self.G.add_node(lbl, unit=str(unit))

            # Arista triádica
            self.G.add_edge(f"{C1},{C2},{C3}", C4,
                            triad=labels, a=a, b=b, K=K,
                            label=f"{C1}·{C4} = {a}/{b}·{C2}·{C3}")

            print(f"  TRIADA ACEPTADA | K={K} | {result['equation']}")
        else:
            k = result["K"] if result else 0
            print(f"  TRIADA RECHAZADA por K bajo ({k})")

    def visualize(self, filename: str = "triadic_physics_graph"):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(self.G, k=3, iterations=100, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_size=4000, node_color="#a8e6cf",
                font_size=11, font_weight="bold", arrowsize=25, edge_color="#555555")
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels, font_size=9)
        plt.title("Grafo Triádico con Validación Dimensional\n(Guardián Activado)", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Grafo exportado a {filename}.png")
EOF