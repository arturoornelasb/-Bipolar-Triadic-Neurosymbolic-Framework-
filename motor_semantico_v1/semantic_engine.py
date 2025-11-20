"""
semantic_engine.py v0.1
Calcula la Resonancia Triádica (K) en el espacio semántico.
Lógica: Paralelismo Vectorial.
"""
import numpy as np
from scipy.spatial.distance import cosine
from typing import Tuple

class SemanticResonanceEngine:
    def __init__(self, space):
        self.space = space

    def calculate_resonance(self, A: str, B: str, C: str, D: str) -> float:
        """
        Verifica la analogía: A es a B como C es a D.
        Matemáticamente: vec(B) - vec(A) ≈ vec(D) - vec(C)
        """
        va = self.space.get_vector(A)
        vb = self.space.get_vector(B)
        vc = self.space.get_vector(C)
        vd = self.space.get_vector(D)

        if any(v is None for v in [va, vb, vc, vd]):
            print(f"Error: Alguna palabra no existe en el vocabulario.")
            return 0.0

        # 1. Calcular Vectores de Transformación (El "Significado" del cambio)
        # T1: El viaje de A a B (ej: de Hombre a Rey, gana Realeza)
        T1 = vb - va
        
        # T2: El viaje de C a D (ej: de Mujer a Reina, gana Realeza)
        T2 = vd - vc

        # 2. Calcular Similitud Coseno entre las transformaciones
        # (1 - distancia coseno) nos da similitud entre -1 y 1
        # Si los vectores son idénticos (paralelos), K = 1.0
        
        # Protección contra vectores cero (si A=B)
        if np.all(T1 == 0) or np.all(T2 == 0):
            return 0.0 # No hay transformación para comparar
            
        similarity = 1 - cosine(T1, T2)
        return similarity

    def solve_analogy(self, A: str, B: str, C: str) -> str:
        """
        Resuelve: A es a B como C es a... ¿X?
        X = C + (B - A)
        """
        va, vb, vc = [self.space.get_vector(x) for x in [A, B, C]]
        
        # Vector Objetivo Ideal
        target_vec = vc + (vb - va)
        
        # Buscar el vecino más cercano en el vocabulario
        best_word = None
        best_dist = float('inf')
        
        for word, vec in self.space.vocab.items():
            if word in [A, B, C]: continue # No queremos repetir la pregunta
            
            dist = cosine(target_vec, vec)
            if dist < best_dist:
                best_dist = dist
                best_word = word
                
        return best_word