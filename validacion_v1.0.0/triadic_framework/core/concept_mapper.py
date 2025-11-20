import math

class PrimeConceptMapper:
    """
    A mock 'Neural Layer' that maps semantic attributes to Prime Numbers.
    This allows the Triadic Engine to process abstract concepts as integers.
    """
    def __init__(self):
        # 1. Define the 'Basis Vectors' (Attributes) as Primes
        self.attribute_map = {
            # Entity Types
            "ENTITY": 2,
            "HUMAN": 3,
            "ANIMAL": 5,
            "OBJECT": 7,
            
            # Gender
            "MALE": 11,
            "FEMALE": 13,
            "NEUTRAL": 17,
            
            # Status / Role
            "ROYALTY": 19,
            "COMMONER": 23,
            "LEADER": 29,
            "SERVANT": 31,
            
            # Age
            "YOUNG": 37,
            "ADULT": 41,
            "OLD": 43,
            
            # Abstract Qualities (BUSS Axes)
            "POSITIVE": 47,
            "NEGATIVE": 53,
            "POWERFUL": 59,
            "WEAK": 61
        }
        
        # 2. Define 'Concepts' as combinations of attributes
        # In a real system, this would be learned. Here we define them manually.
        self.concept_definitions = {
            "man": ["HUMAN", "MALE", "ADULT"],
            "woman": ["HUMAN", "FEMALE", "ADULT"],
            "king": ["HUMAN", "MALE", "ADULT", "ROYALTY", "LEADER"],
            "queen": ["HUMAN", "FEMALE", "ADULT", "ROYALTY", "LEADER"],
            "prince": ["HUMAN", "MALE", "YOUNG", "ROYALTY"],
            "princess": ["HUMAN", "FEMALE", "YOUNG", "ROYALTY"],
            "boy": ["HUMAN", "MALE", "YOUNG"],
            "girl": ["HUMAN", "FEMALE", "YOUNG"],
            
            # Sentiment Examples
            "hero": ["HUMAN", "POSITIVE", "POWERFUL"],
            "villain": ["HUMAN", "NEGATIVE", "POWERFUL"],
            "victim": ["HUMAN", "NEGATIVE", "WEAK"] # Negative situation
        }

    def get_concept_value(self, word: str) -> int:
        """
        Returns the integer representation of a word by multiplying its attribute primes.
        """
        word = word.lower()
        if word not in self.concept_definitions:
            raise ValueError(f"Concept '{word}' not defined in mapper.")
            
        attributes = self.concept_definitions[word]
        value = 1
        for attr in attributes:
            if attr in self.attribute_map:
                value *= self.attribute_map[attr]
            else:
                raise ValueError(f"Attribute '{attr}' not found in basis.")
        
        return value

    def get_attributes_from_value(self, value: int) -> list:
        """
        Reverse engineering: Factorize the integer to find its attributes.
        """
        attributes = []
        temp_val = value
        
        # Check each prime in our basis
        for attr, prime in self.attribute_map.items():
            while temp_val % prime == 0:
                attributes.append(attr)
                temp_val //= prime
                
        if temp_val != 1:
            # If we have a remainder, it means the number has factors not in our basis
            attributes.append(f"UNKNOWN_FACTOR({temp_val})")
            
        return attributes

    def get_concept_name(self, value: int) -> str:
        """
        Find the word that matches this integer value.
        """
        # 1. Check exact matches
        for word in self.concept_definitions:
            if self.get_concept_value(word) == value:
                return word
                
        # 2. If no exact match, return the factorized description
        attrs = self.get_attributes_from_value(value)
        return f"Composite({', '.join(attrs)})"
