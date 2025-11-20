cd ~/triadic-framework/triadic-framework

cat > triadic_framework/core/network.py << 'EOF'
"""
network.py v0.3.1 – 2025-11-19
TriadicNetwork: grafo dirigido de conceptos conectado por triadas de alto K
FIX: SyntaxError en add_node + uso de node_type en vez de type
"""

import networkx as nx
from typing import Tuple, Any
from triadic_framework.core.triadic_search import auto_discover_best_triplet
from fractions import Fraction

class TriadicNetwork:
    def __init__(self):
        self.G = nx.DiGraph()
    
    def add_candidate_quartet(self, values: Tuple[int, int, int, int], labels: Tuple[str, str, str, str], min_K: float = 0.9):
        result = auto_discover_best_triplet(values, labels)
        if result and result["K"] >= min_K:
            C1, C2, C3, C4 = result["C1"], result["C2"], result["C3"], result["C4"]
            K = result["K"]
            a, b = map(int, result["a/b"].split('/'))
            
            # Añadimos nodos (corregido: type → node_type)
            for label in labels:
                self.G.add_node(label, node_type="concept")
            
            # Arista triádica
            self.G.add_edge(
                f"{C1},{C2},{C3}", C4,
                triad=(C1, C2, C3, C4),
                a=a, b=b, K=K,
                label=f"{C1}·{C4} = {a}/{b}·{C2}·{C3}"
            )
            print(f"✓ Triada añadida | K={K:.1f} | {result['equation']}")
        else:
            k = result["K"] if result else 0
            print(f"✗ Triada rechazada | K={k:.3f}")

    def visualize(self, filename="triadic_physics_graph"):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(14,10))
        pos = nx.spring_layout(self.G, k=3, iterations=100, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_size=4000, node_color="#a8e6cf",
                font_size=11, font_weight="bold", arrowsize=25, edge_color="#555555")
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels, font_size=10, alpha=0.8)
        plt.title("Grafo Triádico de Mecánica Clásica\nRedescubierto Automáticamente (K≥0.9)", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Grafo exportado a {filename}.png")
EOF