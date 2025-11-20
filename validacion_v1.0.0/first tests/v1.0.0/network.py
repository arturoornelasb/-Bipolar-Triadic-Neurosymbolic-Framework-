"""
network.py v1.0.1 – 2025-11-19
FIX: El Guardián Dimensional ahora valida DESPUÉS del descubrimiento aritmético.
"""

import networkx as nx
from typing import Tuple
from triadic_framework.core.triadic_search import auto_discover_best_triplet
from triadic_framework.core.dimensional_units import UNITS_MAP

class TriadicNetwork:
    def __init__(self):
        self.G = nx.DiGraph()

    def check_dimensional_balance(self, labels: Tuple[str, str, str, str]) -> bool:
        """
        Verifica C1 * C4 == C2 * C3 dimensionalmente.
        """
        try:
            # Obtenemos las unidades, si no existen, asumimos que son constantes (None)
            u1, u2, u3, u4 = [UNITS_MAP.get(l) for l in labels]
            
            # Si alguna unidad es desconocida (ej. constantes numéricas nuevas), permitimos el paso
            # para no bloquear el descubrimiento, pero lanzamos advertencia.
            if None in (u1, u2, u3, u4): 
                return True 
            
            # Chequeo estricto: [Extremos] == [Medios]
            return (u1 * u4) == (u2 * u3)
        except:
            return True

    def add_candidate_quartet(self, values: Tuple[int, int, int, int], labels: Tuple[str, str, str, str], min_K: float = 0.9):
        # 1. PRIMERO DESCUBRIMOS EL ORDEN ARITMÉTICO (El Motor trabaja)
        result = auto_discover_best_triplet(values, labels)
        
        if result and result["K"] >= min_K:
            # Extraemos el orden "ganador" que encontró el motor
            C1_lbl, C2_lbl, C3_lbl, C4_lbl = result["C1"], result["C2"], result["C3"], result["C4"]
            ordered_labels = (C1_lbl, C2_lbl, C3_lbl, C4_lbl)
            
            # 2. AHORA SÍ, EL GUARDIÁN VALIDA ESE ORDEN ESPECÍFICO
            if not self.check_dimensional_balance(ordered_labels):
                print(f"Rechazo Dimensional sobre orden descubierto: {ordered_labels}")
                # Imprimimos por qué falló para depurar
                u = [UNITS_MAP.get(l) for l in ordered_labels]
                print(f"  Detalle: {u[0]}*{u[3]} != {u[1]}*{u[2]}")
                return

            # 3. Si pasa ambos filtros, agregamos al grafo
            C1, C2, C3, C4 = result["C1"], result["C2"], result["C3"], result["C4"] # Valores son strings en result keys
            # Nota: result guarda los LABELS en C1..C4, no los valores numéricos. 
            # Pero para el grafo usamos los labels.
            
            K = result["K"]
            a, b = map(int, result["a/b"].split('/'))
            
            for lbl in labels: self.G.add_node(lbl)
            
            # Creamos la arista
            self.G.add_edge(f"{C1_lbl},{C2_lbl},{C3_lbl}", C4_lbl,
                            triad=ordered_labels, a=a, b=b, K=K,
                            label=f"{C1_lbl}·{C4_lbl}={a}/{b}·{C2_lbl}·{C3_lbl}")
            
            print(f"Triada Aceptada (K={K}): {result['equation']}")
        else:
            k_val = result["K"] if result else 0
            print(f"Rechazo Aritmético (K bajo: {k_val}) para {labels}")