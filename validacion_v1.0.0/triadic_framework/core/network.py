"""
network.py v5.1 – 2025-11-19
UPDATE: Visualización con detección de comunidades (Louvain/Greedy) para ver las ramas de la física.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple
from triadic_framework.core.triadic_search import auto_discover_best_triplet
from triadic_framework.core.dimensional_units import UNITS_MAP

class TriadicNetwork:
    def __init__(self):
        self.G = nx.DiGraph()

    def check_dimensional_balance(self, labels: Tuple[str, str, str, str]) -> bool:
        try:
            u1, u2, u3, u4 = [UNITS_MAP.get(l) for l in labels]
            if None in (u1, u2, u3, u4): 
                return True 
            return (u1 * u4) == (u2 * u3)
        except:
            return True

    def add_candidate_quartet(self, values: Tuple[int, int, int, int], labels: Tuple[str, str, str, str], min_K: float = 0.9):
        result = auto_discover_best_triplet(values, labels)
        
        if result and result["K"] >= min_K:
            C1_lbl, C2_lbl, C3_lbl, C4_lbl = result["C1"], result["C2"], result["C3"], result["C4"]
            ordered_labels = (C1_lbl, C2_lbl, C3_lbl, C4_lbl)
            
            if not self.check_dimensional_balance(ordered_labels):
                return

            K = result["K"]
            a, b = map(int, result["a/b"].split('/'))
            
            for lbl in labels: self.G.add_node(lbl)
            
            self.G.add_edge(f"{C1_lbl},{C2_lbl},{C3_lbl}", C4_lbl,
                            triad=ordered_labels, a=a, b=b, K=K,
                            label=f"{C1_lbl}·{C4_lbl}={a}/{b}·{C2_lbl}·{C3_lbl}")
            
            print(f"Triada Aceptada (K={K}): {result['equation']}")
        else:
            pass

    def visualize(self, filename: str = "triadic_physics_graph"):
        if self.G.number_of_nodes() == 0:
            print("El grafo está vacío.")
            return

        plt.figure(figsize=(24, 18)) # Lienzo 4K para ver detalles
        
        # 1. Detectar Comunidades (Ramas de la Física)
        # Convertimos a no-dirigido para el algoritmo de comunidades
        G_undirected = self.G.to_undirected()
        try:
            communities = nx.community.greedy_modularity_communities(G_undirected)
        except:
            communities = [self.G.nodes()] # Fallback si falla

        # Asignar colores por comunidad
        color_map = {}
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#DDA0DD', '#FF69B4']
        
        node_colors = []
        for node in self.G.nodes():
            for i, comm in enumerate(communities):
                if node in comm:
                    color_map[node] = colors[i % len(colors)]
                    break
            node_colors.append(color_map.get(node, '#CCCCCC'))

        # 2. Layout (Kamada-Kawai es mejor para separar clusters)
        try:
            pos = nx.kamada_kawai_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, k=0.3, iterations=100)
        
        # 3. Dibujar
        # Nodos centrales más grandes (Degree Centrality)
        degrees = dict(self.G.degree())
        node_sizes = [degrees[n] * 50 + 500 for n in self.G.nodes()]

        nx.draw_networkx_nodes(self.G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, edgecolors="black")
        nx.draw_networkx_edges(self.G, pos, alpha=0.2, edge_color="#555555", arrowsize=10)
        
        # Etiquetas solo para nodos importantes (grado > 2) para no saturar
        labels_to_draw = {n: n for n, d in degrees.items() if d > 2}
        nx.draw_networkx_labels(self.G, pos, labels=labels_to_draw, font_size=10, font_weight="bold", font_color="#333333")

        # Estadísticas en el gráfico
        info = (f"Nodos: {self.G.number_of_nodes()} | Aristas: {self.G.number_of_edges()}\n"
                f"Comunidades Detectadas: {len(communities)}")
        plt.text(0.05, 0.95, info, transform=plt.gca().transAxes, fontsize=14, 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

        plt.title("Grafo Unificado de la Física (UHRT v5.0)\nClasificación Automática por Comunidades", fontsize=22)
        plt.axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        print(f"Grafo Topológico exportado a: {filename}.png")