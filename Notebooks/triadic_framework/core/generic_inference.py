"""
generic_inference.py v1.1.0 – 2025-11-19
UPDATE: Refactoring of additive logic (Explicit Sum/Subtraction) and step counter correction.
"""

from typing import Dict, Optional
from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.triadic_engine import TriadicRelationalFramework as Triadic
from triadic_framework.core.additive_laws import AdditiveLaw, ENERGY_CONSERVATION

class GenericInferenceEngine:
    def __init__(self, network: TriadicNetwork):
        self.net = network
        self.triadic = Triadic()
        self.additive_laws = [ENERGY_CONSERVATION]

    def solve(self, inputs: Dict[str, float], target_var: str, max_steps: int = 10) -> Optional[float]:
        known = {k: float(v) for k, v in inputs.items()}
        
        # Base rule: '1' is always 1.0
        known['1'] = 1.0
        
        print(f"\n--- HYBRID INFERENCE FOR {target_var} ---")
        print(f"Initial data: {known}")

        for step in range(1, max_steps + 1):
            # Success verification at start of cycle
            if target_var in known:
                val = known[target_var]
                display_val = int(val) if val.is_integer() else val
                # UX Adjustment: If found in step 1, say "1 STEPS" (not 0)
                print(f"SUCCESS IN {step} STEPS! {target_var} = {display_val}")
                return val
            
            changed = False
            
            # --- 1. MULTIPLICATIVE INFERENCE (Triads) ---
            for _, _, data in self.net.G.edges(data=True):
                triad = data.get('triad') 
                if not triad: continue
                
                # On-the-fly literal learning
                for lbl in triad:
                    if lbl not in known:
                        try:
                            known[lbl] = float(lbl)
                        except ValueError:
                            pass 

                missing_list = [lbl for lbl in triad if lbl not in known]
                
                if len(missing_list) != 1:
                    continue
                
                missing_lbl = missing_list[0]
                vals = {lbl: known[lbl] for lbl in triad if lbl in known}
                
                try:
                    a, b = data['a'], data['b']
                    C1, C2, C3, C4 = triad
                    val_calculated = None
                    
                    # Universal solving algebra (C1, C2, C3 or C4)
                    if missing_lbl == C1:
                        val_calculated = (a * vals[C2] * vals[C3]) / (b * vals[C4])
                    elif missing_lbl == C4:
                        val_calculated = (a * vals[C2] * vals[C3]) / (b * vals[C1])
                    elif missing_lbl == C2:
                        val_calculated = (b * vals[C1] * vals[C4]) / (a * vals[C3])
                    elif missing_lbl == C3:
                        val_calculated = (b * vals[C1] * vals[C4]) / (a * vals[C2])

                    if val_calculated is not None:
                        known[missing_lbl] = val_calculated
                        changed = True
                        print(f"Step {step} (Multiplicative): {missing_lbl} = {val_calculated:.2f}  [Solving for {triad}]")
                        
                except ZeroDivisionError:
                    continue

            # --- 2. ADDITIVE INFERENCE (Explicit Logic) ---
            for law in self.additive_laws:
                # Branch A: Calculate TOTAL (Sum / Integral)
                if law.total not in known:
                    if all(p in known for p in law.parts):
                        total_val = sum(known[p] for p in law.parts)
                        known[law.total] = total_val
                        changed = True
                        print(f"Step {step} (Additive - Sum): {law.total} = {total_val:.2f}")

                # Branch B: Calculate a PART (Subtraction / Differential)
                if law.total in known:
                    total_val = known[law.total]
                    missing_parts = [p for p in law.parts if p not in known]
                    
                    if len(missing_parts) == 1:
                        missing_part = missing_parts[0]
                        known_parts_sum = sum(known[p] for p in law.parts if p in known)
                        val_part = total_val - known_parts_sum
                        
                        known[missing_part] = val_part
                        changed = True
                        print(f"Step {step} (Additive - Subtraction): {missing_part} = {val_part:.2f}")

            if not changed:
                print(f"Inference stopped at step {step}: No more facts can be deduced.")
                break
            
        return known.get(target_var)