"""
calculus_convergence_test.py v1.1.2 – 2025-11-19
FIX: Aumento de factor de escala (x10000) para evitar redondeo a cero en pasos infinitesimales.
"""
print(">>> EL SCRIPT SE ESTÁ EJECUTANDO... (Si ves esto, el archivo es correcto)")

from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.generic_inference import GenericInferenceEngine
from triadic_framework.core.additive_laws import AdditiveLaw
import logging

# Apagamos logs para que la salida sea limpia
logging.getLogger().setLevel(logging.ERROR)

def run_high_res_integral():
    net = TriadicNetwork()
    print("=== PRUEBA DE CONVERGENCIA UHRT (v1.1.2) ===")
    print("Objetivo: Demostrar que la Integral es una suma de triadas.")
    print("Función: v(t) = 2t")
    print("Teórico Exacto: 16.0\n")

    acceleration = 2.0
    total_time = 4.0
    steps = 100
    delta_t = total_time / steps  # dt = 0.04s
    
    # --- FACTOR DE ESCALA (El Microscopio) ---
    SCALE = 10000 
    
    print(f"Configuración: {steps} pasos (dt={delta_t}s). Escala Entera: x{SCALE}")
    
    slices = []
    known_values = {'1': 1.0} 

    for i in range(1, steps + 1):
        t_instant = i * delta_t
        v_instant = acceleration * t_instant
        
        var_v = f"v_{i}"
        var_d = f"d_{i}"
        var_dt = f"dt_{i}"
        
        known_values[var_v] = v_instant
        known_values[var_dt] = delta_t
        
        v_int = int(v_instant * SCALE)
        dt_int = int(delta_t * SCALE)
        d_expected_int = v_int * dt_int 
        
        net.add_candidate_quartet(
            (d_expected_int, 1, v_int, dt_int), 
            (var_d, '1', var_v, var_dt)
        )
        slices.append(var_d)

    integral_law = AdditiveLaw("Integral Riemann", slices, "Distancia_Total")

    engine = GenericInferenceEngine(net)
    engine.additive_laws.append(integral_law)

    print("... Resolviendo 100 triadas infinitesimales ...")
    result = engine.solve(known_values, "Distancia_Total", max_steps=5)
    
    print(f"\n>>> RESULTADO ALTA RESOLUCIÓN: {result}")
    
    error = result - 16.0
    print(f"Error: {error:.4f}")
    
    if abs(error) < 1.0: 
        print("\n✅ CONVERGENCIA DEMOSTRADA: El cálculo emerge de la aritmética.")

if __name__ == "__main__":
    run_high_res_integral()
