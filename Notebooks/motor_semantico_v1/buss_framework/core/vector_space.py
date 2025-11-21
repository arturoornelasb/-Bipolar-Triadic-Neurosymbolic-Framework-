"""
vector_space.py v0.1
Gestiona el 'Significado' como coordenadas en un espacio n-dimensional.
Para esta demo, usamos vectores sintéticos 'perfectos' para validar la lógica.
"""
import numpy as np
from typing import Dict, List, Optional

class VectorSpace:
    def __init__(self):
        self.vocab: Dict[str, np.ndarray] = {}
        self.dims = 0

    def add_word(self, word: str, vector: List[float]):
        """Añade un concepto al espacio."""
        v = np.array(vector, dtype=float)
        if self.dims == 0:
            self.dims = len(v)
        elif len(v) != self.dims:
            raise ValueError(f"Dimensión incorrecta para '{word}'. Se espera {self.dims}.")
        self.vocab[word] = v

    def get_vector(self, word: str) -> Optional[np.ndarray]:
        return self.vocab.get(word)

    def load_synthetic_data(self):
        """
        Loads a 'Toy Universe' to test analogies.
        Conceptual Axes:
        [0]: Gender (-1.0 = Man, +1.0 = Woman)
        [1]: Royalty (0.0 = Commoner, 1.0 = Noble)
        [2]: Age    (0.0 = Baby, 1.0 = Adult)
        """
        print("--- Loading Pure Synthetic Data ---")
        #                        [Gender, Royalty, Age]
        self.add_word("hombre",  [-1.0,   0.0,    1.0]) # man
        self.add_word("mujer",   [ 1.0,   0.0,    1.0]) # woman
        self.add_word("rey",     [-1.0,   1.0,    1.0]) # king
        self.add_word("reina",   [ 1.0,   1.0,    1.0]) # queen
        
        self.add_word("niño",    [-1.0,   0.0,    0.2]) # boy
        self.add_word("niña",    [ 1.0,   0.0,    0.2]) # girl
        self.add_word("prncipe", [-1.0,   1.0,    0.2]) # prince
        self.add_word("prncesa", [ 1.0,   1.0,    0.2]) # princess
        
        # Garbage concepts to test failure
        self.add_word("manzana", [ 0.0,  -0.5,    0.0]) # apple 
