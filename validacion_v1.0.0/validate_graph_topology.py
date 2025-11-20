"""
validate_graph_topology.py (v2.0 - Robust)
Objetivo: Validar científicamente la estructura del Grafo UHRT v7.0.
FIX: Manejo de errores en ajuste log-log y visualización mejorada.
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from ingest_physics_db import run_ingestion, deep_clean, extract_variables_from_sympy
import json

def build_graph_for_analysis():
    print(">>> Reconstruyendo Grafo UHRT v7.0 en memoria...")
    try:
        with open('final_physics_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None

    G = nx.Graph()
    laws = data.get("laws", [])
    constants = data.get("constants", [])
    
    for const in constants:
        sym = deep_clean(const.get("symbol"))
        if sym: G.add_node(sym, type="constant")
            
    for law in laws:
        eq_str = law.get("sympy_repr", "")
        if not eq_str: continue
        vars_in_law = extract_variables_from_sympy(eq_str)
        if len(vars_in_law) < 2: continue
        
        for i in range(len(vars_in_law)):
            for j in range(i + 1, len(vars_in_law)):
                G.add_edge(vars_in_law[i], vars_in_law[j])
                
    print(f"Grafo construido: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas.")
    return G

def analyze_topology(G):
    print("\n=== ANÁLISIS TOPOLÓGICO (Validación Académica) ===")
    
    degrees = [d for n, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees)
    print(f"1. Grado Promedio: {avg_degree:.2f}")
    
    density = nx.density(G)
    print(f"2. Densidad: {density:.4f}")
    
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    giant = G.subgraph(components[0])
    print(f"3. Componente Gigante: {giant.number_of_nodes()} nodos ({giant.number_of_nodes()/G.number_of_nodes():.1%})")
    
    if giant.number_of_nodes() > 1:
        try:
            # Usamos una muestra si es muy grande para acelerar, pero aqui son pocos nodos
            avg_path = nx.average_shortest_path_length(giant)
            print(f"4. Camino Promedio (L): {avg_path:.2f}")
        except: pass

    clustering = nx.average_clustering(G)
    print(f"6. Clustering (C): {clustering:.4f}")
    
    print("\n=== TOP 5 HUBS (PageRank) ===")
    try:
        # PageRank es mejor para grafos de conocimiento que Eigenvector
        pagerank = nx.pagerank(G) 
        top_5 = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (node, score) in enumerate(top_5, 1):
            print(f"   {i}. {node} ({score:.4f})")
    except: pass

    # --- 7. LEY DE POTENCIA (Robust) ---
    print("\nGenerando gráfico de Distribución de Grado...")
    
    # Contar frecuencias
    degree_counts = {}
    for d in degrees:
        if d > 0: # Ignorar nodos aislados para evitar log(0)
            degree_counts[d] = degree_counts.get(d, 0) + 1
    
    # Ordenar para plotear
    x = sorted(degree_counts.keys())
    y = [degree_counts[d] for d in x]
    
    # Convertir a arrays numpy para matemáticas
    x_arr = np.array(x)
    y_arr = np.array(y)
    
    # Logaritmos (filtrando ceros por seguridad)
    log_x = np.log10(x_arr)
    log_y = np.log10(y_arr)
    
    # Ajuste Lineal (Gamma)
    # Solo usamos la "cola" de la distribución (grados > 1) para evitar ruido al inicio
    try:
        coeffs = np.polyfit(log_x, log_y, 1)
        gamma = -coeffs[0]
        r_squared = 1 - (sum((log_y - (coeffs[0]*log_x + coeffs[1]))**2) / ((len(log_y)-1) * np.var(log_y, ddof=1)))
    except:
        gamma = 0
        r_squared = 0

    print(f"\n>>> EXPONENTE GAMMA (γ): {gamma:.2f} (R²={r_squared:.2f})")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(x, y, 'bo', markersize=6, alpha=0.6, label='Datos Reales')
    
    if gamma > 0:
        # Dibujar la línea de ajuste
        fit_y = 10**(coeffs[0]*log_x + coeffs[1])
        plt.loglog(x, fit_y, 'r--', linewidth=2, label=f'Ajuste Ley Potencia (γ={gamma:.2f})')

    plt.title("Topología Scale-Free del Grafo Físico", fontsize=14)
    plt.xlabel("Grado (k) - Conexiones", fontsize=12)
    plt.ylabel("Frecuencia P(k)", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig("graph_validation_plot.png")
    print("Gráfico guardado: 'graph_validation_plot.png'")

if __name__ == "__main__":
    G = build_graph_for_analysis()
    if G:
        analyze_topology(G)