"""
ingest_physics_db.py v7.0
Objetivo: Ingeniería Inversa de 'final_physics_database.json'.
Mejoras Críticas:
1. DEEP CLEANING: Elimina sufijos basura (_planc, _light, _boltzmann, _charge).
2. UNIFICACIÓN DE CONSTANTES: Detecta c, h, k, G, e automáticamente.
3. PUENTES DE RAMA: Conecta cada ley a su Rama (Branch) para garantizar conectividad total.
"""
import json
import re
from triadic_framework.core.network import TriadicNetwork

# Palabras basura detectadas en tu JSON específico
GARBAGE_SUFFIXES = [
    "_planc_lightk_boltzmann", 
    "_planc", "_light", "_boltzmann", "_charge", "_grav", "_gas",
    "_elec", "_mag", "constant", "number"
]

# Mapa de Unificación Semántica (Diccionario Maestro)
UNIFY_MAP = {
    # Espacio-Tiempo
    't': 't', 'dt': 't', 'tau': 't', 'T_period': 't', 'time': 't',
    'd': 'L', 'x': 'L', 'y': 'L', 'z': 'L', 'r': 'L', 'h': 'L', 'l': 'L', 
    'L': 'L', 's': 'L', 'wavelength': 'L', 'lambda': 'L', 'lamda': 'L', 'radius': 'L',
    'A': 'Area', 'Area': 'Area', 'S': 'Area',
    'V': 'Volume', 'Vol': 'Volume', 'Volume': 'Volume', # Cuidado con Voltaje
    
    # Dinámica
    'v': 'v', 'c': 'v', 'velocity': 'v', 'speed': 'v',
    'a': 'a', 'g': 'a', 'acceleration': 'a',
    'p': 'Momentum',
    'F': 'Force', 'force': 'Force', 'Weight': 'Force', 'Tension': 'Force',
    'm': 'Mass', 'M': 'Mass', 'mu': 'Mass', # mu a veces es masa reducida
    
    # Energía y Trabajo
    'E': 'Energy', 'E_k': 'Energy', 'KE': 'Energy', 'PE': 'Energy', 'U': 'Energy', 
    'W': 'Energy', 'Work': 'Energy', 'H': 'Energy', 'Q': 'Energy', 'Hamiltonian': 'Energy',
    'P': 'Power', 'Power': 'Power',
    
    # Electromagnetismo (Aquí V es Voltaje)
    'V_voltage': 'Voltage', 'EMF': 'Voltage', 'potential': 'Voltage',
    'I': 'Current', 'J': 'Current_Density',
    'R': 'Resistance', 'Z': 'Resistance', 'X': 'Resistance',
    'q': 'Charge', 'e': 'Charge', 'Q_charge': 'Charge',
    'B': 'B_Field',
    'E_field': 'E_Field',
    
    # Termodinámica (Aquí P es Presión)
    'T': 'Temperature', 'temp': 'Temperature',
    'P_pressure': 'Pressure', 'pressure': 'Pressure',
    'S': 'Entropy',
    'n': 'Moles', 'N': 'Particles',
    
    # Constantes (Nodos Puente)
    'c_light': 'CONST_c',
    'h_Planck': 'CONST_h', 'hbar': 'CONST_h',
    'k_Boltzmann': 'CONST_k',
    'G_Newton': 'CONST_G',
    'e_charge': 'CONST_e',
    'mu_0': 'CONST_mu0', 'epsilon_0': 'CONST_eps0',
    'pi': 'CONST_pi'
}

def deep_clean(sym):
    """Cirugía para limpiar nombres de variables sucios."""
    if not sym: return None
    
    # 1. Eliminación de sufijos basura conocidos
    original = sym
    for garbage in GARBAGE_SUFFIXES:
        sym = sym.replace(garbage, "")
    
    # 2. Correcciones específicas del dataset
    if sym.startswith("_0"): sym = "mu_0" # Error común de OCR
    if sym == "e": sym = "e_charge"
    if sym == "c": sym = "c_light"
    
    # 3. Limpieza de caracteres
    sym = re.sub(r"\*\*?\d+", "", sym) # Quitar potencias (v^2 -> v)
    sym = sym.strip("_")
    
    # 4. Mapeo Semántico
    # Primero intento directo
    if sym in UNIFY_MAP: return UNIFY_MAP[sym]
    
    # Intento parcial (si contiene la clave)
    # Ej: 'V_rms' contiene 'V_voltage' en tu mente, pero aqui mapeamos keys
    for key, master in UNIFY_MAP.items():
        if key == sym: return master
        
    return sym

def extract_variables_from_sympy(expr_str):
    """Extrae variables usando regex sobre la cadena sympy."""
    # Busca palabras que empiecen con letra
    raw = re.findall(r"[a-zA-Z][a-zA-Z0-9_]*", expr_str)
    
    clean_vars = set()
    blacklist = {"Eq", "sqrt", "sin", "cos", "tan", "exp", "log", "ln", "diff", "const"}
    
    for r in raw:
        if r in blacklist: continue
        cleaned = deep_clean(r)
        if cleaned:
            clean_vars.add(cleaned)
            
    return list(clean_vars)

def run_ingestion():
    print("=== INGENIERÍA INVERSA V7.0 (DEEP CLEANING) ===")
    
    try:
        with open('final_physics_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("❌ Error: No encuentro 'final_physics_database.json'.")
        return

    net = TriadicNetwork()
    laws = data.get("laws", [])
    constants = data.get("constants", [])
    
    print(f"Procesando {len(laws)} leyes y {len(constants)} constantes...")
    
    # 1. INYECTAR CONSTANTES (Nodos Puente)
    for const in constants:
        sym = deep_clean(const.get("symbol"))
        if sym:
            net.G.add_node(sym, type="constant", label=const.get("name"))
            
    # 2. PROCESAR LEYES
    connections = 0
    
    for law in laws:
        name = law.get("name", "Unknown")
        branch = law.get("branch", "General Physics") # Rama (Mecánica, Termo...)
        eq_str = law.get("sympy_repr", "")
        
        if not eq_str: continue
        
        # Extraer variables limpias
        vars_in_law = extract_variables_from_sympy(eq_str)
        
        if len(vars_in_law) < 2: continue
        
        # ESTRATEGIA DE CONEXIÓN TOTAL
        
        # A. Conexión Interna (La Fórmula)
        # Conectamos todas las variables entre sí (forman un 'clique' de conocimiento)
        hub_var = vars_in_law[0]
        for var in vars_in_law[1:]:
            if var != hub_var:
                net.G.add_edge(var, hub_var, relation="formula")
                connections += 1
        
        # B. Conexión Jerárquica (La Rama)
        # Conectamos las variables principales a su Rama (Ej: Temperature -> Thermodynamics)
        # Esto garantiza que no haya islas.
        branch_node = f"BRANCH_{branch.upper()}"
        net.G.add_node(branch_node, type="branch")
        
        for var in vars_in_law:
            # Solo conectamos si no existe ya, para no saturar
            if not net.G.has_edge(var, branch_node):
                net.G.add_edge(var, branch_node, relation="belongs_to")
                connections += 1

    print("\n" + "="*40)
    print(f"RESULTADO V7.0:")
    print(f"  Nodos Totales: {net.G.number_of_nodes()}")
    print(f"  Conexiones:    {net.G.number_of_edges()}")
    print("="*40)

    if net.G.number_of_edges() > 0:
        net.visualize("physics_universe_v7")

if __name__ == "__main__":
    run_ingestion()