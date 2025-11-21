import os
import json
import requests

class LLMConnector:
    """
    Interface for connecting to LLMs.
    Supports:
    1. Mock (Default): Returns pre-defined responses for testing.
    2. Google Gemini (Free Tier): Uses API Key if provided.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # Reverting to generic alias
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def extract_physics_data(self, text):
        """
        Extracts physics variables and hypothesis from text.
        """
        if self.api_key:
            return self._call_gemini(text)
        else:
            return self._call_mock(text)
            
    def _call_mock(self, text):
        print("   [LLM Connector] Using MOCK (No API Key found).")
        if "Newton" in text:
            return {
                "candidates": [
                    {"symbol": "F", "unit": "N", "name": "Force"},
                    {"symbol": "m", "unit": "kg", "name": "Mass"},
                    {"symbol": "a", "unit": "m/s^2", "name": "Acceleration"}
                ],
                "hypothesis": "F = m * a"
            }
        elif "Kinetic Energy" in text:
             return {
                "candidates": [
                    {"symbol": "KE", "unit": "J", "name": "Kinetic Energy"},
                    {"symbol": "m", "unit": "kg", "name": "Mass"},
                    {"symbol": "v", "unit": "m/s", "name": "Velocity"}
                ],
                "hypothesis": "KE = 0.5 * m * v^2"
            }
        return None

    def _call_gemini(self, text):
        print("   [LLM Connector] Calling GEMINI API...")
        
        prompt = f"""
        You are a Physics Mining Assistant. Extract variables and the formula hypothesis from the following text.
        Return ONLY valid JSON in this format:
        {{
            "candidates": [
                {{"symbol": "var_symbol", "unit": "SI_unit", "name": "var_name"}}
            ],
            "hypothesis": "formula_string"
        }}
        
        Text: "{text}"
        """
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(
                f"{self.url}?key={self.api_key}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            text_resp = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean markdown code blocks if present
            text_resp = text_resp.replace("```json", "").replace("```", "").strip()
            
            return json.loads(text_resp)
            
        except Exception as e:
            print(f"   [LLM Connector] API Error: {e}")
            return self._call_mock(text) # Fallback to mock on error

if __name__ == "__main__":
    # Test the connector
    connector = LLMConnector()
    data = connector.extract_physics_data("Newton's second law: Force equals mass times acceleration.")
    print(json.dumps(data, indent=2))
