import math

def calculate_super_metric(num_nodes, num_edges, gamma, scale_factor=1.0):
    """
    Calculates the UHRT Super Metric (UBS_UHM).
    Formula: UBS_UHM = Entropy_Term + Dimensional_Term
    
    Args:
        num_nodes (int): Number of nodes in the graph.
        num_edges (int): Number of edges in the graph.
        gamma (float): Power law exponent (Gamma) from topological analysis.
        scale_factor (float): Scaling factor for dimensional term.
    """
    # Shannon Entropy (approximated by connection density)
    # Density = E / (N * (N - 1))
    if num_nodes <= 1:
        return 0.0
        
    density = num_edges / (num_nodes * (num_nodes - 1))
    
    # Entropy Term = -Density * log2(Density)
    # Represents the information content or "disorder" in the connections.
    entropy_term = -1 * density * math.log2(density) if density > 0 else 0
    
    # Dimensional Dilution (based on Gamma - topology)
    # A low gamma (e.g., 1.19) implies high concentration (low dilution/high hub dominance).
    # We use Gamma as a proxy for the dimensional spread.
    # Dimensional Term = Gamma * log2(Scale)
    # If scale_factor is 1.0, log2(1) is 0, so this term vanishes unless we define a scale.
    # For this experiment, we assume a scale relative to the "Universal Binary Scale" base, say 2.
    # Or we just use Gamma directly as the factor if scale is implicit.
    # User's code: dimensional_term = gamma * math.log2(scale_factor)
    # If scale_factor defaults to 1.0, this term is 0. 
    # Let's check if the user intended a specific scale. 
    # "scale_factor=1.0" in args. 
    # If I run it as is, it returns just the entropy term.
    # But the user might want to see the impact of Gamma.
    # Let's keep the user's code exactly as provided, but maybe add a comment or set a default scale if needed.
    # User provided: `dimensional_term = gamma * math.log2(scale_factor)`
    # And called it with default.
    # Wait, if scale_factor is 1, log2(1) is 0. So Gamma doesn't affect the result?
    # Maybe the user meant scale_factor to be N? or something else?
    # "Composite Dimensional Evolution Framework" might suggest Scale = Dimensions.
    # But I will stick to the user's snippet.
    
    dimensional_term = gamma * math.log2(scale_factor)
    
    ubs_uhm = entropy_term + dimensional_term
    return ubs_uhm

def run_metric_calculation():
    # Data from Section 10 (Graph Topology Analysis)
    # [cite: 316, 349] -> These likely refer to the node/edge counts in the user's context or previous runs.
    # In my previous run (Step 554):
    # Graph built: 378 nodes, 1348 edges.
    # Gamma: 1.19
    
    nodes = 378
    edges = 1348
    gamma = 1.19
    
    # We might want to use a scale factor > 1 to make Gamma relevant.
    # But I will follow the user's snippet which uses default 1.0 (implied).
    # Wait, `metric = calculate_super_metric(nodes, edges, gamma)` uses default scale_factor=1.0.
    # So result = entropy_term.
    
    metric = calculate_super_metric(nodes, edges, gamma)
    
    print(f"=== UHRT SUPER METRIC (UBS_UHM) ===")
    print(f"Inputs: Nodes={nodes}, Edges={edges}, Gamma={gamma}")
    print(f"Calculated Value for Physics Graph: {metric:.4f}")
    print("Interpretation: Lower value confirms high-efficiency ordering (Low Entropy).")
    print("Note: This metric quantifies the 'Semantic Cost' of the knowledge structure.")

if __name__ == "__main__":
    run_metric_calculation()
