from triadic_framework.core.triadic_engine import Triadic
import random; random.seed(42)
from math import gcd

def lcm(x, y):
    return x * y // gcd(x, y)

results = []
for _ in range(2000):
    a = random.randint(1, 1000)
    b = random.randint(1, 1000)
    g = gcd(a, b)
    l = lcm(a, b)
    r = Triadic.discovery(g, a, b, l)  # C1=g, C2=a, C3=b, C4=l
    results.append((r.a, r.b, float(r.simplicity)))

print(f"Unique rules (a,b): {set((a,b) for a,b,k in results)}")
print(f"Max K = {max(k for a,b,k in results)}")
PY