"""
validate_romiti_discovery.py (v2.2 - Multi-Path)
Objective: Find MULTIPLE paths between Plasma and Dirac.
This validates the robustness and redundancy of knowledge in the graph.
"""
import networkx as nx
import json
from ingest_physics_db import deep_clean, extract_variables_from_sympy, UNIFY_MAP

def find_node_by_keyword(G, keywords):
    """Find nodes by keyword."""
    candidates = []
    for node in G.nodes():
        node_str = str(node).lower()
        for kw in keywords:
            if kw.lower() in node_str:
                candidates.append(node)
    return list(set(candidates))

def find_romiti_path():
    print(">>> Reconstructing Graph for Multi-Path Test (UHRT v7.0)...")
    
    try:
        with open('final_physics_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'final_physics_database.json' is missing.")
        return
        
    net = nx.Graph()
    laws = data.get("laws", [])
    constants = data.get("constants", [])

    for const in constants:
        sym = deep_clean(const.get("symbol"))
        if sym: net.add_node(sym, type="constant")
            
    for law in laws:
        eq_str = law.get("sympy_repr", "")
        if not eq_str: continue
        vars_in_law = extract_variables_from_sympy(eq_str)
        if len(vars_in_law) < 2: continue
        
        hub = vars_in_law[0]
        for var in vars_in_law[1:]:
            if var != hub:
                net.add_edge(var, hub, label="formula")
        
        branch = law.get("branch", "General")
        branch_node = f"BRANCH_{branch.upper()}"
        for var in vars_in_law:
            net.add_edge(var, branch_node, label="branch")

    print(f"Graph reconstructed: {net.number_of_nodes()} nodes.")

    # --- TEST CONFIGURATION ---
    # Plasma (Drag Coefficient / Temperature / Debye) -> Quantum (Planck)
    
    # We will test with C_d (which worked before) and Temperature (more fundamental)
    start_nodes = ["C_d", "Temperature", "lambda_D"]
    # Check which of these actually exist
    valid_starts = [n for n in start_nodes if n in net]
    
    if not valid_starts:
        print("⚠️ Exact start nodes not found. Searching for approximations...")
        valid_starts = find_node_by_keyword(net, ["Debye", "Plasma", "drag"])
    
    start_node = valid_starts[0]
    end_node = "CONST_h" # Planck
    
    print(f"\n>>> ORIGIN: {start_node} (Plasma/Fluids)")
    print(f">>> DESTINATION: {end_node} (Quantum/Dirac)")

    # 1. ALL SHORTEST PATHS
    print(f"\n--- [1] OPTIMAL PATHS (Shortest Paths) ---")
    try:
        paths = list(nx.all_shortest_paths(net, source=start_node, target=end_node))
        print(f"Found {len(paths)} minimal length paths ({len(paths[0])-1} hops):")
        
        for i, path in enumerate(paths[:5]): # Show max 5
            print(f"  Route {i+1}: {' -> '.join(path)}")
            
    except nx.NetworkXNoPath:
        print("❌ No path found.")

    # 2. ALTERNATIVE PATHS (Without passing through Branches)
    # Sometimes paths via BRANCH_... are "cheating" (too easy).
    # Let's see if there are purely physical paths (variables and constants).
    print(f"\n--- [2] PURELY PHYSICAL PATHS (Avoiding 'BRANCH' Nodes) ---")
    
    # Create a view of the graph without Branch nodes
    physical_nodes = [n for n in net.nodes() if "BRANCH" not in n]
    G_physical = net.subgraph(physical_nodes)
    
    try:
        if start_node in G_physical and end_node in G_physical:
            phy_paths = list(nx.all_shortest_paths(G_physical, source=start_node, target=end_node))
            print(f"Found {len(phy_paths)} strict physical paths (Length {len(phy_paths[0])-1}):")
            for i, path in enumerate(phy_paths[:3]):
                print(f"  Physics {i+1}: {' -> '.join(path)}")
        else:
            print("⚠️ Start/End nodes are Branches or do not exist in the physical subgraph.")
            
    except nx.NetworkXNoPath:
        print("❌ No direct physical connection (requires passing through a theoretical Branch).")

if __name__ == "__main__":
    find_romiti_path()