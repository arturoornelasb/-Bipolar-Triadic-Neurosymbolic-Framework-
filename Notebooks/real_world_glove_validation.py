import os
import sys
import urllib.request
import zipfile
import numpy as np

# Add parent directory to path to import legacy engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Add motor_semantico_v1 specifically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../motor_semantico_v1')))

try:
    from motor_semantico_v1.vector_space import VectorSpace
    from motor_semantico_v1.semantic_engine import SemanticResonanceEngine
except ImportError:
    # Fallback if structure is different
    from buss_framework.core.vector_space import VectorSpace
    from buss_framework.core.semantic_engine import SemanticResonanceEngine

GLOVE_URL = "http://nlp.stanford.edu/data/glove.6B.zip"
GLOVE_ZIP = "glove.6B.zip"
GLOVE_FILE = "glove.6B.50d.txt"

def download_glove():
    if os.path.exists(GLOVE_FILE):
        print(f"✅ Found {GLOVE_FILE}, skipping download.")
        return

    if not os.path.exists(GLOVE_ZIP):
        print(f"⬇️ Downloading GloVe embeddings from {GLOVE_URL}...")
        print("   (This may take a while, file size ~822MB)")
        try:
            # Use a User-Agent to avoid 403 Forbidden
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(GLOVE_URL, GLOVE_ZIP)
            print("✅ Download complete.")
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("   Try downloading manually: wget http://nlp.stanford.edu/data/glove.6B.zip")
            return

    print(f"📦 Extracting {GLOVE_FILE} from zip...")
    try:
        with zipfile.ZipFile(GLOVE_ZIP, 'r') as zip_ref:
            zip_ref.extract(GLOVE_FILE)
        print("✅ Extraction complete.")
    except zipfile.BadZipFile:
        print("❌ Error: The downloaded zip file is corrupted.")

def load_glove_vectors(vector_space, file_path):
    print(f"📖 Loading vectors from {file_path}...")
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype='float32')
            vector_space.add_word(word, vector)
            count += 1
            if count % 50000 == 0:
                print(f"   Loaded {count} words...")
    print(f"✅ Loaded {count} words into VectorSpace.")

def run_real_world_test():
    print("\n===================================================")
    print("   REAL WORLD VALIDATION: GloVe-50d Integration")
    print("===================================================")
    print("ℹ️  Dataset Info: http://nlp.stanford.edu/data/glove.6B.zip")
    print("ℹ️  See README_DATASETS.md for more details.\n")

    # 1. Ensure Data Exists
    download_glove()
    
    if not os.path.exists(GLOVE_FILE):
        print("❌ Could not find GloVe file. Aborting test.")
        return

    # 2. Initialize Engine
    vs = VectorSpace()
    load_glove_vectors(vs, GLOVE_FILE)
    engine = SemanticResonanceEngine(vs)

    # 3. Test Analogy: Man : King :: Woman : ? (Expected: Queen)
    print("\n--- Test 1: Classic Analogy (Man : King :: Woman : ?) ---")
    # Logic: King - Man + Woman = Queen
    # Solve: A=Man, B=King, C=Woman -> X = Woman + (King - Man)
    
    # Let's check if the words exist
    required_words = ["king", "man", "woman", "queen"]
    missing = [w for w in required_words if w not in vs.vocab]
    if missing:
        print(f"❌ Missing words in vocabulary: {missing}")
        return

    prediction = engine.solve_analogy("man", "king", "woman")
    print(f"Analogy: Man : King :: Woman : ?")
    print(f"Prediction: {prediction}")
    
    if prediction == "queen":
        print("✅ SUCCESS: The engine correctly identified 'queen' using real GloVe data.")
    else:
        print(f"⚠️ Result: '{prediction}' (Expected 'queen'). Real data can be noisy.")

    # 4. Test 2: Capital Cities
    # France : Paris :: Italy : ? (Expected: Rome)
    print("\n--- Test 2: Geography (France : Paris :: Italy : ?) ---")
    prediction_geo = engine.solve_analogy("france", "paris", "italy") 
    print(f"Analogy: France : Paris :: Italy : ?")
    print(f"Prediction: {prediction_geo}")
    
    if prediction_geo == "rome":
        print("✅ SUCCESS: The engine correctly identified 'rome'.")
    else:
         print(f"⚠️ Result: '{prediction_geo}' (Expected 'rome').")

if __name__ == "__main__":
    run_real_world_test()
