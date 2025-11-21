"""
network.py v5.1 – 2025-11-19
UPDATE: Visualization with community detection (Louvain/Greedy) to see physics branches.
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
            
            print(f"Triad Accepted (K={K}): {result['equation']}")
        else:
            pass

    def save_graph(self, filename: str):
        """Saves the current graph to a GraphML file."""
        try:
            # Ensure filename ends with .graphml
            if not filename.endswith(".graphml"):
                filename += ".graphml"
            nx.write_graphml(self.G, filename)
            print(f"Graph successfully saved to: {filename}")
        except Exception as e:
            print(f"Error saving graph: {e}")

    def visualize(self, filename: str = "triadic_physics_graph"):
        if self.G.number_of_nodes() == 0:
            print("The graph is empty.")
            return

        plt.figure(figsize=(24, 18)) # 4K Canvas to see details
        
        # 1. Semantic Coloring (Priority: Type > Community)
        # We try to use the 'type' attribute if available (constant, branch, etc.)
        node_colors = []
        # Define a semantic color map
        semantic_colors = {
            "constant": "#FFD700",  # Gold for Constants
            "branch": "#FF69B4",    # HotPink for Branches
            "variable": "#87CEFA",  # LightSkyBlue for Variables (default)
            "default": "#CCCCCC"    # Grey for others
        }
        
        # Fallback: Community Detection
        G_undirected = self.G.to_undirected()
        try:
            communities = nx.community.greedy_modularity_communities(G_undirected)
        except:
            communities = [self.G.nodes()]

        comm_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#DDA0DD']
        comm_map = {}
        for i, comm in enumerate(communities):
            for node in comm:
                comm_map[node] = comm_colors[i % len(comm_colors)]

        for node in self.G.nodes():
            # Check for explicit type first
            node_type = self.G.nodes[node].get("type")
            if node_type in semantic_colors:
                node_colors.append(semantic_colors[node_type])
            elif node.startswith("BRANCH_"): # Fallback if type not set but name implies branch
                 node_colors.append(semantic_colors["branch"])
            elif node.startswith("CONST_"): # Fallback for constants
                 node_colors.append(semantic_colors["constant"])
            else:
                # Use community color if no specific type
                node_colors.append(comm_map.get(node, semantic_colors["default"]))

        # 2. Layout - Spring Layout with more spacing (k) is often cleaner than Kamada-Kawai for this
        # k = optimal distance between nodes. Increase to spread out.
        try:
            # k=0.15 is default. We use a dynamic k based on node count to ensure spacing.
            k_val = 2.0 / (self.G.number_of_nodes() ** 0.5) 
            pos = nx.spring_layout(self.G, k=k_val, iterations=50, seed=42)
        except:
            pos = nx.random_layout(self.G)
        
        # 3. Draw
        # Larger central nodes (Degree Centrality)
        degrees = dict(self.G.degree())
        # Cap node size to avoid obscuring the graph
        node_sizes = [min(degrees[n] * 100 + 300, 3000) for n in self.G.nodes()]

        nx.draw_networkx_nodes(self.G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, edgecolors="black", linewidths=1.5)
        nx.draw_networkx_edges(self.G, pos, alpha=0.3, edge_color="#555555", arrowsize=15, width=1.0)
        
        # Labels: Show all branches and constants, and high degree nodes
        labels_to_draw = {}
        for n, d in degrees.items():
            is_special = n.startswith("BRANCH_") or n.startswith("CONST_") or self.G.nodes[n].get("type") in ["branch", "constant"]
            if d > 2 or is_special:
                labels_to_draw[n] = n
                
        nx.draw_networkx_labels(self.G, pos, labels=labels_to_draw, font_size=10, font_weight="bold", font_color="#222222")

        # Graph Statistics
        info = (f"Nodes: {self.G.number_of_nodes()} | Edges: {self.G.number_of_edges()}\n"
                f"Communities Detected: {len(communities)}")
        plt.text(0.02, 0.98, info, transform=plt.gca().transAxes, fontsize=14, 
                 verticalalignment='top', bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

        # Legend for Semantic Colors
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Constant', markerfacecolor=semantic_colors['constant'], markersize=15, markeredgecolor='k'),
            Line2D([0], [0], marker='o', color='w', label='Branch', markerfacecolor=semantic_colors['branch'], markersize=15, markeredgecolor='k'),
            Line2D([0], [0], marker='o', color='w', label='Variable/Cluster', markerfacecolor=semantic_colors['variable'], markersize=15, markeredgecolor='k')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=12, title="Node Types")

        plt.title("Unified Physics Graph (UHRT v7.0)\nSemantic Topology Visualization", fontsize=22)
        plt.axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        print(f"Topological Graph exported to: {filename}.png")