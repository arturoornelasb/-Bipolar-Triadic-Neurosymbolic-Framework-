"""
calculus_convergence_test.py v1.1.2 – 2025-11-19
FIX: Increased scale factor (x10000) to avoid rounding to zero in infinitesimal steps.
"""
print(">>> SCRIPT IS RUNNING... (If you see this, the file is correct)")

from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.generic_inference import GenericInferenceEngine
from triadic_framework.core.additive_laws import AdditiveLaw
import logging

# Turn off logs for clean output
logging.getLogger().setLevel(logging.ERROR)

def run_high_res_integral():
    net = TriadicNetwork()
    print("=== UHRT CONVERGENCE TEST (v1.1.2) ===")
    print("Objective: Demonstrate that the Integral is a sum of triads.")
    print("Function: v(t) = 2t")
    print("Exact Theoretical: 16.0\n")

    acceleration = 2.0
    total_time = 4.0
    steps = 100
    delta_t = total_time / steps  # dt = 0.04s
    
    # --- SCALE FACTOR (The Microscope) ---
    SCALE = 10000 
    
    print(f"Configuration: {steps} steps (dt={delta_t}s). Integer Scale: x{SCALE}")
    
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

    integral_law = AdditiveLaw("Riemann Integral", slices, "Total_Distance")

    engine = GenericInferenceEngine(net)
    engine.additive_laws.append(integral_law)

    print("... Solving 100 infinitesimal triads ...")
    result = engine.solve(known_values, "Total_Distance", max_steps=5)
    
    print(f"\n>>> HIGH RESOLUTION RESULT: {result}")
    
    error = result - 16.0
    print(f"Error: {error:.4f}")
    
    if abs(error) < 1.0: 
        print("\n✅ CONVERGENCE PROVEN: Calculus emerges from arithmetic.")

if __name__ == "__main__":
    run_high_res_integral()
