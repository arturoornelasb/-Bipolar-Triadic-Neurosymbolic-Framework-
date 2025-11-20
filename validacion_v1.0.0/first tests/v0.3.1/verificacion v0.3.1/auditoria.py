poetry run python - << 'PY'
from triadic_framework.core.network import TriadicNetwork
net = TriadicNetwork()  # recreamos rápidamente el grafo

# Añadimos las mismas triadas del notebook (copia-pega esto)
quartets = [
    ((12,24,36,72), ('GCD','a','b','LCM')),
    ((12,1,3,4), ('V','1','I','R')),
    ((100,1,10,10), ('2KE','1','m','v²')),
    ((50,50,1,1), ('W','ΔKE','1','1')),
    ((10,5,50,1), ('F','d','W','1')),
    ((20,10,2,1), ('F','m','a','1')),
    ((30,1,10,3), ('F','1','k','x')),
    ((1,4,4,1), ('F','r²','G·m1·m2','1')),
]
for values, labels in quartets:
    net.add_candidate_quartet(values, labels)

# === VERIFICACIÓN FINAL ===
print(f"Nodos totales: {net.G.number_of_nodes()}")
print(f"Aristas (triadas válidas): {net.G.number_of_edges()}\n")
print("Lista completa de triadas aceptadas (K ≥ 0.9):")
for u, v, data in net.G.edges(data=True):
    print(f"{u} → {v} | K = {data['K']:.1f} | {data['label']}")
PY