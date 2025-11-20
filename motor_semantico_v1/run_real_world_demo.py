"""
run_real_world_demo.py
Prueba de Analogías Complejas (Geografía y Conceptos) con 50 Dimensiones.
"""
import sys
import os
sys.path.append(os.getcwd()) # Parche de ruta

from buss_framework.core.vector_space import VectorSpace
from buss_framework.core.semantic_engine import SemanticResonanceEngine
from buss_framework.core.mini_glove import load_real_vectors

def run():
    # 1. Iniciar Universo 50d
    vs = VectorSpace()
    load_real_vectors(vs) # Cargamos la "Matrix" simulada
    engine = SemanticResonanceEngine(vs)
    
    print("\n=== TEST 1: GEOGRAFÍA (Capitales) ===")
    # Pregunta: Paris es a Francia lo que Roma es a Italia?
    # A: Paris, B: Francia :: C: Roma, D: Italia
    # Vector: Pais - Ciudad
    K = engine.calculate_resonance("paris", "francia", "roma", "italia")
    print(f"Analogía: Paris -> Francia :: Roma -> Italia")
    print(f"Resonancia K: {K:.4f}")
    
    if K > 0.9: print("✅ El sistema entiende Capitales.")
    
    print("\n=== TEST 2: INFERENCIA GEOGRÁFICA ===")
    # Tokio - Japon + Italia = ?
    # (Debería ser Roma, o algo italiano-ciudad)
    # Ecuación: X = Italia + (Tokio - Japon)
    # X = (Pais_I + Ciudad_I) + ((Pais_J + Ciudad_J) - (Pais_J)) ?? No, al revés
    # Analogía: Japon -> Tokio :: Italia -> ???
    
    res = engine.solve_analogy("japon", "tokio", "italia")
    print(f"Si estás en Japón y vas a Tokio...")
    print(f"Si estás en Italia, vas a: {res.upper()}")
    
    print("\n=== TEST 3: DISCRIMINACIÓN DE RUIDO (50 Dimensiones) ===")
    # Paris -> Francia :: Manzana -> ???
    # En 3D esto dio 0.72. En 50D debería ser mucho más bajo.
    K_ruido = engine.calculate_resonance("paris", "francia", "manzana", "mesa")
    print(f"Analogía Absurda: Paris->Francia :: Manzana->Mesa")
    print(f"Resonancia K: {K_ruido:.4f}")
    
    if K_ruido < 0.5:
        print("✅ ÉXITO: En 50D, el ruido se filtra mucho mejor que en 3D.")
    else:
        print("⚠️ Aún hay correlación espuria.")

if __name__ == "__main__":
    run()