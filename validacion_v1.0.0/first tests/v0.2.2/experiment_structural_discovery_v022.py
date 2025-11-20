poetry run python - << 'PY'
from triadic_framework.core.triadic_search import auto_discover_best_triplet
from math import gcd
def lcm(a,b): return a*b // gcd(a,b) if a*b else 0

print(auto_discover_best_triplet((gcd(24,36), 24, 36, lcm(24,36)), ('GCD','a','b','LCM')))
print(auto_discover_best_triplet((12, 1, 3, 4), ('V','1','I','R')))
print(auto_discover_best_triplet((100, 1, 10, 10), ('2KE','1','m','v²')))
PY