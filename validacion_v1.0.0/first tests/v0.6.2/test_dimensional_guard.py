cat > test_dimensional_guard.py << 'EOF'
from triadic_framework.core.network import TriadicNetwork

net = TriadicNetwork()

print("=== PRUEBA DEL GUARDIÁN DIMENSIONAL ===\n")

# 1. Ley correcta: F = m·a
net.add_candidate_quartet((20, 10, 2, 1), ('F', 'm', 'a', '1'))

# 2. Ley correcta: W = F·d
net.add_candidate_quartet((50, 5, 10, 1), ('W', 'F', 'd', '1'))

# 3. LEY FALSA: F = m·m / a (numéricamente posible pero físicamente absurda)
net.add_candidate_quartet((100, 10, 10, 1), ('F', 'm', 'm', 'a'))

# 4. LEY FALSA: W = m·R (energía = masa × resistencia)
net.add_candidate_quartet((500, 5, 100, 1), ('W', 'm', 'R', '1'))

print(f"\nGrafo final: {net.G.number_of_edges()} triadas válidas (debe ser 2)")
net.visualize("grafo_con_guardian")
EOF

poetry run python test_dimensional_guard.py