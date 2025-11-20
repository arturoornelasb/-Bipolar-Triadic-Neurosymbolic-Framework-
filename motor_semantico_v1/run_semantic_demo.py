"""
run_semantic_demo.py
Prueba de Concepto: Validación de Analogías con Vectores Sintéticos.
"""
import sys
import os

# --- PARCHE DE RUTA ---
# Añadimos el directorio actual al path de Python para que encuentre 'buss_framework'
sys.path.append(os.getcwd())
# ----------------------

from buss_framework.core.vector_space import VectorSpace
from buss_framework.core.semantic_engine import SemanticResonanceEngine

def run_demo():
    # 1. Iniciar el Universo
    vs = VectorSpace()
    vs.load_synthetic_data()
    
    engine = SemanticResonanceEngine(vs)
    
    print("\n=== TEST 1: VERIFICACIÓN DE ANALOGÍA (Cálculo de K) ===")
    # Pregunta: ¿Hombre -> Rey es similar a Mujer -> Reina?
    # Debería ser K=1.0 porque ambos "ganan" el mismo atributo de realeza (+1.0)
    
    A, B = "hombre", "rey"
    C, D = "mujer", "reina"
    
    K = engine.calculate_resonance(A, B, C, D)
    print(f"Analogía: {A} -> {B} :: {C} -> {D}")
    print(f"Resonancia Semántica (K): {K:.4f}")
    
    if K > 0.99:
        print("✅ LÓGICA CONFIRMADA: La estructura se mantiene.")
    else:
        print("❌ FALLO DE LÓGICA.")

    print("\n=== TEST 2: SOLUCIÓN DE INCÓGNITAS (Inferencia) ===")
    # Pregunta: Niño -> Príncipe :: Niña -> ???
    A, B, C = "niño", "prncipe", "niña"
    
    result = engine.solve_analogy(A, B, C)
    # Manejo de error si no encuentra respuesta
    if result:
        print(f"Pregunta: {A} es a {B} como {C} es a... ?")
        print(f"Respuesta de la IA: {result.upper()}")
    else:
        print("No se encontró una respuesta clara.")
    
    # Prueba de Falsedad (Control)
    print("\n=== TEST 3: DETECCIÓN DE ABSURDOS ===")
    # Hombre -> Rey :: Manzana -> ???
    # Esto debería dar una resonancia baja o una respuesta sin sentido si lo forzamos
    K_fake = engine.calculate_resonance("hombre", "rey", "manzana", "reina")
    print(f"Analogía Falsa: hombre -> rey :: manzana -> reina")
    print(f"Resonancia K: {K_fake:.4f}")
    print("(Nota: Un K bajo o negativo indica que la analogía no tiene sentido lógico)")

if __name__ == "__main__":
    run_demo()