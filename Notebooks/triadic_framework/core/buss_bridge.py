from triadic_framework.core.concept_mapper import PrimeConceptMapper

class BussBridge:
    """
    Bridges the Bipolar Universal Semantic Scale (BUSS) with the Triadic Engine.
    Maps continuous axes (e.g., Sentiment) to discrete Prime Factors.
    """
    def __init__(self):
        self.mapper = PrimeConceptMapper()
        
        # Define BUSS Axes as Prime Pairs (Poles)
        self.axes = {
            "SENTIMENT": {"POSITIVE": 47, "NEGATIVE": 53},
            "POWER": {"POWERFUL": 59, "WEAK": 61}
        }

    def get_axis_primes(self, axis_name: str):
        axis_name = axis_name.upper()
        if axis_name in self.axes:
            return self.axes[axis_name]
        else:
            raise ValueError(f"Axis {axis_name} not found.")

    def project_concept(self, concept_val: int, axis_name: str) -> str:
        """
        Determines where a concept falls on a BUSS axis based on its prime factors.
        """
        axis = self.get_axis_primes(axis_name)
        
        is_pole_a = (concept_val % axis[list(axis.keys())[0]] == 0)
        is_pole_b = (concept_val % axis[list(axis.keys())[1]] == 0)
        
        if is_pole_a and not is_pole_b:
            return list(axis.keys())[0] # e.g., "POSITIVE"
        elif is_pole_b and not is_pole_a:
            return list(axis.keys())[1] # e.g., "NEGATIVE"
        elif is_pole_a and is_pole_b:
            return "AMBIVALENT" # Has both primes
        else:
            return "NEUTRAL" # Has neither
