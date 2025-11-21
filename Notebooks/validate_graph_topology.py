"""
validate_graph_topology.py (v2.0 - Robust)
Objective: Scientifically validate the structure of the UHRT Graph v7.0.
FIX: Error handling in log-log fit and improved visualization.
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os

def simple_pagerank(G, alpha=0.85, max_iter=100, tol=1.0e-6):
    """
    A simple PageRank implementation using numpy to avoid scipy dependency.
    """
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0: return {}
    
    node_map = {node: i for i, node in enumerate(nodes)}
    
    # Create transition matrix M
    # M[i, j] is probability of moving from j to i
    M = np.zeros((n, n))
    
    for node in nodes:
        neighbors = list(G.neighbors(node))
        if not neighbors:
            # Dangling node: distribute probability equally to all nodes
            M[:, node_map[node]] = 1.0 / n
        else:
            prob = 1.0 / len(neighbors)
            for neighbor in neighbors:
                M[node_map[neighbor], node_map[node]] = prob
                
    # Power iteration
    v = np.ones(n) / n
    for _ in range(max_iter):
        v_next = alpha * np.dot(M, v) + (1 - alpha) / n
        if np.linalg.norm(v_next - v, 1) < tol:
            v = v_next
            break
        v = v_next
        
    return {nodes[i]: v[i] for i in range(n)}

def build_graph_for_analysis():
    print(">>> Loading UHRT Graph v7.0 from 'physics_knowledge_graph.graphml'...")
    try:
        if os.path.exists('physics_knowledge_graph.graphml'):
            G = nx.read_graphml('physics_knowledge_graph.graphml')
            # Convert to undirected for topological analysis (connected components, etc.)
            G = G.to_undirected()
            print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
            return G
        else:
            print("❌ Error: 'physics_knowledge_graph.graphml' not found. Please run ingest_physics_db.py first.")
            return None
    except Exception as e:
        print(f"❌ Error loading graph: {e}")
        return None

def analyze_topology(G):
    print("\n=== TOPOLOGICAL ANALYSIS (Academic Validation) ===")
    
    degrees = [d for n, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees)
    print(f"1. Average Degree: {avg_degree:.2f}")
    
    density = nx.density(G)
    print(f"2. Density: {density:.4f}")
    
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    giant = G.subgraph(components[0])
    print(f"3. Giant Component: {giant.number_of_nodes()} nodes ({giant.number_of_nodes()/G.number_of_nodes():.1%})")
    
    if giant.number_of_nodes() > 1:
        try:
            # Use a sample if it is very large to speed up, but here there are few nodes
            avg_path = nx.average_shortest_path_length(giant)
            print(f"4. Average Path Length (L): {avg_path:.2f}")
        except: pass

    clustering = nx.average_clustering(G)
    print(f"6. Clustering Coefficient (C): {clustering:.4f}")
    
    try:
        # PageRank is better for knowledge graphs than Eigenvector
        # Try nx.pagerank first, fallback to simple_pagerank
        try:
            pagerank = nx.pagerank(G)
        except ImportError:
            print("Scipy not found, using numpy-based simple_pagerank...")
            pagerank = simple_pagerank(G)
            
        top_20 = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:20]
        
        print("\n=== TOP 5 HUBS (PageRank) ===")
        for i, (node, score) in enumerate(top_20[:5], 1):
            print(f"   {i}. {node} ({score:.4f})")
            
        # Generate PageRank Plot
        nodes = [n for n, s in top_20]
        scores = [s for n, s in top_20]
        
        plt.figure(figsize=(12, 8))
        plt.barh(nodes[::-1], scores[::-1], color='skyblue')
        plt.xlabel('PageRank Score')
        plt.title('Top 20 Physics Concepts by Centrality (PageRank)')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("pagerank_top20_physics.png")
        print("Plot saved: 'pagerank_top20_physics.png'")
    except Exception as e:
        print(f"Error calculating PageRank: {e}")

    # --- 7. POWER LAW (Robust) ---
    print("\nGenerating Degree Distribution plot...")
    
    # Count frequencies
    degree_counts = {}
    for d in degrees:
        if d > 0: # Ignore isolated nodes to avoid log(0)
            degree_counts[d] = degree_counts.get(d, 0) + 1
    
    # Sort for plotting
    x = sorted(degree_counts.keys())
    y = [degree_counts[d] for d in x]
    
    # Convert to numpy arrays for math
    x_arr = np.array(x)
    y_arr = np.array(y)
    
    # Logarithms (filtering zeros for safety)
    log_x = np.log10(x_arr)
    log_y = np.log10(y_arr)
    
    # Linear Fit (Gamma)
    # Only use the "tail" of the distribution (degrees > 1) to avoid noise at the start
    try:
        coeffs = np.polyfit(log_x, log_y, 1)
        gamma = -coeffs[0]
        r_squared = 1 - (sum((log_y - (coeffs[0]*log_x + coeffs[1]))**2) / ((len(log_y)-1) * np.var(log_y, ddof=1)))
    except:
        gamma = 0
        r_squared = 0

    print(f"\n>>> GAMMA EXPONENT (γ): {gamma:.2f} (R²={r_squared:.2f})")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(x, y, 'bo', markersize=6, alpha=0.6, label='Real Data')
    
    if gamma > 0:
        # Draw the fit line
        fit_y = 10**(coeffs[0]*log_x + coeffs[1])
        plt.loglog(x, fit_y, 'r--', linewidth=2, label=f'Power Law Fit (γ={gamma:.2f})')

    plt.title("Scale-Free Topology of Physics Graph", fontsize=14)
    plt.xlabel("Degree (k) - Connections", fontsize=12)
    plt.ylabel("Frequency P(k)", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig("graph_validation_plot.png")
    print("Plot saved: 'graph_validation_plot.png'")

if __name__ == "__main__":
    G = build_graph_for_analysis()
    if G:
        analyze_topology(G)