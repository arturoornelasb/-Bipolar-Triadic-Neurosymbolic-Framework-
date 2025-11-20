from typing import List, Dict, Optional

class AdditiveLaw:
    def __init__(self, name: str, parts: List[str], total: str):
        self.name = name
        self.parts = parts
        self.total = total

    def solve_missing(self, known_values: Dict[str, float]) -> Optional[float]:
        if self.total not in known_values:
            if all(p in known_values for p in self.parts):
                return sum(known_values[p] for p in self.parts)
        return None

ENERGY_CONSERVATION = AdditiveLaw("Conservación Energía", ["KE", "PE"], "E_total")
