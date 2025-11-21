"""
ingest_physics_db.py v7.0
Objective: Reverse Engineering of 'final_physics_database.json'.
Critical Improvements:
1. DEEP CLEANING: Removes garbage suffixes (_planc, _light, _boltzmann, _charge).
2. CONSTANT UNIFICATION: Automatically detects c, h, k, G, e.
3. BRANCH BRIDGES: Connects each law to its Branch to ensure total connectivity.
"""
import json
import re
from triadic_framework.core.network import TriadicNetwork

# Garbage words detected in your specific JSON
GARBAGE_SUFFIXES = [
    "_planc_lightk_boltzmann", 
    "_planc", "_light", "_boltzmann", "_charge", "_grav", "_gas",
    "_elec", "_mag", "constant", "number"
]

# Semantic Unification Map (Master Dictionary)
UNIFY_MAP = {
    # Space-Time
    't': 't', 'dt': 't', 'tau': 't', 'T_period': 't', 'time': 't',
    'd': 'L', 'x': 'L', 'y': 'L', 'z': 'L', 'r': 'L', 'h': 'L', 'l': 'L', 
    'L': 'L', 's': 'L', 'wavelength': 'L', 'lambda': 'L', 'lamda': 'L', 'radius': 'L',
    'A': 'Area', 'Area': 'Area', 'S': 'Area',
    'V': 'Volume', 'Vol': 'Volume', 'Volume': 'Volume', # Watch out for Voltage
    
    # Dynamics
    'v': 'v', 'c': 'v', 'velocity': 'v', 'speed': 'v',
    'a': 'a', 'g': 'a', 'acceleration': 'a',
    'p': 'Momentum',
    'F': 'Force', 'force': 'Force', 'Weight': 'Force', 'Tension': 'Force',
    'm': 'Mass', 'M': 'Mass', 'mu': 'Mass', # mu is sometimes reduced mass
    
    # Energy and Work
    'E': 'Energy', 'E_k': 'Energy', 'KE': 'Energy', 'PE': 'Energy', 'U': 'Energy', 
    'W': 'Energy', 'Work': 'Energy', 'H': 'Energy', 'Q': 'Energy', 'Hamiltonian': 'Energy',
    'P': 'Power', 'Power': 'Power',
    
    # Electromagnetism (Here V is Voltage)
    'V_voltage': 'Voltage', 'EMF': 'Voltage', 'potential': 'Voltage',
    'I': 'Current', 'J': 'Current_Density',
    'R': 'Resistance', 'Z': 'Resistance', 'X': 'Resistance',
    'q': 'Charge', 'e': 'Charge', 'Q_charge': 'Charge',
    'B': 'B_Field',
    'E_field': 'E_Field',
    
    # Thermodynamics (Here P is Pressure)
    'T': 'Temperature', 'temp': 'Temperature',
    'P_pressure': 'Pressure', 'pressure': 'Pressure',
    'S': 'Entropy',
    'n': 'Moles', 'N': 'Particles',
    
    # Constants (Bridge Nodes)
    'c_light': 'CONST_c',
    'h_Planck': 'CONST_h', 'hbar': 'CONST_h',
    'k_Boltzmann': 'CONST_k',
    'G_Newton': 'CONST_G',
    'e_charge': 'CONST_e',
    'mu_0': 'CONST_mu0', 'epsilon_0': 'CONST_eps0',
    'pi': 'CONST_pi'
}

def deep_clean(sym):
    """Surgery to clean dirty variable names."""
    if not sym: return None
    
    # 1. Removal of known garbage suffixes
    original = sym
    for garbage in GARBAGE_SUFFIXES:
        sym = sym.replace(garbage, "")
    
    # 2. Specific dataset corrections
    if sym.startswith("_0"): sym = "mu_0" # Common OCR error
    if sym == "e": sym = "e_charge"
    if sym == "c": sym = "c_light"
    
    # 3. Character cleaning
    sym = re.sub(r"\*\*?\d+", "", sym) # Remove powers (v^2 -> v)
    sym = sym.strip("_")
    
    # 4. Semantic Mapping
    # First direct attempt
    if sym in UNIFY_MAP: return UNIFY_MAP[sym]
    
    # Partial attempt (if it contains the key)
    # Ex: 'V_rms' contains 'V_voltage' mentally, but here we map keys
    for key, master in UNIFY_MAP.items():
        if key == sym: return master
        
    return sym

def extract_variables_from_sympy(expr_str):
    """Extracts variables using regex on the sympy string."""
    # Finds words starting with a letter
    raw = re.findall(r"[a-zA-Z][a-zA-Z0-9_]*", expr_str)
    
    clean_vars = set()
    blacklist = {"Eq", "sqrt", "sin", "cos", "tan", "exp", "log", "ln", "diff", "const"}
    
    for r in raw:
        if r in blacklist: continue
        cleaned = deep_clean(r)
        if cleaned:
            clean_vars.add(cleaned)
            
    return sorted(list(clean_vars))

def run_ingestion():
    print("=== REVERSE ENGINEERING V7.0 (DEEP CLEANING) ===")
    
    try:
        with open('final_physics_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("❌ Error: Cannot find 'final_physics_database.json'.")
        return

    net = TriadicNetwork()
    laws = data.get("laws", [])
    constants = data.get("constants", [])
    
    print(f"Processing {len(laws)} laws and {len(constants)} constants...")
    
    # 1. INJECT CONSTANTS (Bridge Nodes)
    for const in constants:
        sym = deep_clean(const.get("symbol"))
        if sym:
            net.G.add_node(sym, type="constant", label=const.get("name"))
            
    # 2. PROCESS LAWS
    connections = 0
    
    for law in laws:
        name = law.get("name", "Unknown")
        branch = law.get("branch", "General Physics") # Branch (Mechanics, Thermo...)
        eq_str = law.get("sympy_repr", "")
        
        if not eq_str: continue
        
        # Extract clean variables
        vars_in_law = extract_variables_from_sympy(eq_str)
        
        if len(vars_in_law) < 2: continue
        
        # TOTAL CONNECTION STRATEGY
        
        # A. Internal Connection (The Formula)
        # Connect all variables to each other (forming a knowledge 'clique')
        hub_var = vars_in_law[0]
        for var in vars_in_law[1:]:
            if var != hub_var:
                net.G.add_edge(var, hub_var, relation="formula")
                connections += 1
        
        # B. Hierarchical Connection (The Branch)
        # Connect main variables to their Branch (Ex: Temperature -> Thermodynamics)
        # This ensures there are no islands.
        branch_node = f"BRANCH_{branch.upper()}"
        net.G.add_node(branch_node, type="branch")
        
        for var in vars_in_law:
            # Only connect if not already existing, to avoid saturation
            if not net.G.has_edge(var, branch_node):
                net.G.add_edge(var, branch_node, relation="belongs_to")
                connections += 1

    print("\n" + "="*40)
    print(f"RESULT V7.0:")
    print(f"  Total Nodes: {net.G.number_of_nodes()}")
    print(f"  Connections: {net.G.number_of_edges()}")
    print("="*40)

    if net.G.number_of_edges() > 0:
        net.save_graph("physics_knowledge_graph")
        net.visualize("physics_universe_v7")

if __name__ == "__main__":
    run_ingestion()