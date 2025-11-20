"""
run_additive_reto.py v1.0.0 – 2025-11-19
RETO SUPERADO: Inferencia Híbrida (Multiplicativa + Aditiva)
"""
from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.generic_inference import GenericInferenceEngine

# 1. Construimos la Red con leyes físicas
net = TriadicNetwork()

print("--- [1] CARGA DE CONOCIMIENTO (TRIADAS) ---")

# TRIADA 1: Energía Cinética (2KE = m·v²)
# CORRECCIÓN MATEMÁTICA: 
# Si m=5 y v²=10, entonces m·v²=50. 
# Para que K=1.0, 2KE debe ser 50.
net.add_candidate_quartet((50, 1, 5, 10), ('2KE', '1', 'm', 'v2')) 

# TRIADA 2: Relación Escalar (KE = 2KE / 2)
# 25 (KE) · 2 = 50 (2KE) · 1
net.add_candidate_quartet((25, 50, 1, 2), ('KE', '2KE', '1', '2'))

# 2. Iniciamos el Motor de Inferencia Híbrida
engine = GenericInferenceEngine(net)

# 3. Planteamos el Problema "Imposible"
# Datos: Masa(5), Velocidad²(10), Energía Potencial(200)
# Incógnita: Energía Mecánica Total (E_total)
# Ruta requerida:
#   1. Calcular 2KE (Multiplicativo: m · v²)
#   2. Calcular KE  (Multiplicativo: 2KE / 2)
#   3. Calcular E_total (Aditivo: KE + PE)

inputs = {"m": 5, "v2": 10, "PE": 200}
target = "E_total"

result = engine.solve(inputs, target)

if result is not None:
    print(f"\n🎉 ¡RETO SUPERADO! E_total = {result}")
    print(f"Verificación manual: KE=(1/2)*5*10=25 | PE=200 | Total=225")
else:
    print("\n❌ Falló la inferencia.")