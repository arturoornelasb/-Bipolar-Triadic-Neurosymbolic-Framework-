"""
generic_inference.py v1.1.0 – 2025-11-19
UPDATE: Refactorización de lógica aditiva (Suma/Resta explícitas) y corrección de contador de pasos.
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
        
        # Regla base: '1' siempre es 1.0
        known['1'] = 1.0
        
        print(f"\n--- INFERENCIA HÍBRIDA PARA {target_var} ---")
        print(f"Datos iniciales: {known}")

        for step in range(1, max_steps + 1):
            # Verificación de éxito al inicio del ciclo
            if target_var in known:
                val = known[target_var]
                display_val = int(val) if val.is_integer() else val
                # Ajuste de UX: Si lo encontramos en el paso 1, decimos "1 PASOS" (no 0)
                print(f"¡ÉXITO EN {step} PASOS! {target_var} = {display_val}")
                return val
            
            changed = False
            
            # --- 1. INFERENCIA MULTIPLICATIVA (Triadas) ---
            for _, _, data in self.net.G.edges(data=True):
                triad = data.get('triad') 
                if not triad: continue
                
                # Aprendizaje de literales al vuelo
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
                    
                    # Algebra de despeje universal (C1, C2, C3 o C4)
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
                        print(f"Paso {step} (Multiplicativo): {missing_lbl} = {val_calculated:.2f}  [Despeje de {triad}]")
                        
                except ZeroDivisionError:
                    continue

            # --- 2. INFERENCIA ADITIVA (Lógica Explícita) ---
            for law in self.additive_laws:
                # Rama A: Calcular el TOTAL (Suma / Integral)
                if law.total not in known:
                    if all(p in known for p in law.parts):
                        total_val = sum(known[p] for p in law.parts)
                        known[law.total] = total_val
                        changed = True
                        print(f"Paso {step} (Aditivo - Suma): {law.total} = {total_val:.2f}")

                # Rama B: Calcular una PARTE (Resta / Diferencial)
                if law.total in known:
                    total_val = known[law.total]
                    missing_parts = [p for p in law.parts if p not in known]
                    
                    if len(missing_parts) == 1:
                        missing_part = missing_parts[0]
                        known_parts_sum = sum(known[p] for p in law.parts if p in known)
                        val_part = total_val - known_parts_sum
                        
                        known[missing_part] = val_part
                        changed = True
                        print(f"Paso {step} (Aditivo - Resta): {missing_part} = {val_part:.2f}")

            if not changed:
                print(f"Inferencia detenida en paso {step}: No se pueden deducir más hechos.")
                break
            
        return known.get(target_var)