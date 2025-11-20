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
        Carga un 'Universo de Juguete' perfecto para probar analogías.
        Ejes conceptuales:
        [0]: Género (-1.0 = Hombre, +1.0 = Mujer)
        [1]: Realeza (0.0 = Plebeyo, 1.0 = Noble)
        [2]: Edad    (0.0 = Bebé, 1.0 = Adulto)
        """
        print("--- Cargando Datos Sintéticos Puros ---")
        #                        [Género, Realeza, Edad]
        self.add_word("hombre",  [-1.0,   0.0,    1.0])
        self.add_word("mujer",   [ 1.0,   0.0,    1.0])
        self.add_word("rey",     [-1.0,   1.0,    1.0])
        self.add_word("reina",   [ 1.0,   1.0,    1.0])
        
        self.add_word("niño",    [-1.0,   0.0,    0.2])
        self.add_word("niña",    [ 1.0,   0.0,    0.2])
        self.add_word("prncipe", [-1.0,   1.0,    0.2]) # Principe
        self.add_word("prncesa", [ 1.0,   1.0,    0.2]) # Princesa
        
        # Conceptos basura para probar fallos
        self.add_word("manzana", [ 0.0,  -0.5,    0.0]) 
