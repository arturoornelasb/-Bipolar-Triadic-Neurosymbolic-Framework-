from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.generic_inference import GenericInferenceEngine

# 1. Configurar Red
net = TriadicNetwork()
print("Construyendo Grafo Físico...")

# Triada 1: 2KE = m * v^2
# Valores: 50 (2KE), 1, 5 (m), 10 (v^2) -> 50*1 = 1/1 * 5 * 10 -> OK
net.add_candidate_quartet((50, 1, 5, 10), ('2KE', '1', 'm', 'v2'))

# Triada 2: Relación escalar KE = 2KE / 2
# Valores: 25 (KE), 50 (2KE), 1, 2 -> 25*2 = 1/1 * 50 * 1 -> OK
net.add_candidate_quartet((25, 50, 1, 2), ('KE', '2KE', '1', '2'))

# 2. Inferencia
engine = GenericInferenceEngine(net)
inputs = {"m": 5, "v2": 10, "PE": 200} # Nota: No damos KE, debe deducirlo
target = "E_total"

result = engine.solve(inputs, target)

print(f"\nRESULTADO FINAL: E_total = {result}")
if result == 225.0:
    print("✅ PRUEBA DE INTEGRIDAD v1.0.0 SUPERADA")
else:
    print("❌ FALLO EN PRUEBA")
