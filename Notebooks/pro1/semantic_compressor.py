import sys
import os
import zlib
import struct
import argparse

# Add parent directory to path to import motor_semantico_v1
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor_semantico_v1.vector_space import VectorSpace

class SemanticCompressor:
    def __init__(self):
        self.vs = VectorSpace()
        self.vs.load_synthetic_data()
        self.marker_byte = 0xFF 
        self.vocab_list = list(self.vs.vocab.keys())
        self.word_to_id = {word: i for i, word in enumerate(self.vocab_list)}
        self.id_to_word = {i: word for i, word in enumerate(self.vocab_list)}

    def compress(self, input_path, output_path):
        print(f"Compressing {input_path}...")
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        compressed_stream = bytearray()
        i = 0
        n = len(text)
        while i < n:
            match_found = False
            for word in self.vocab_list:
                if text.startswith(word, i):
                    end_pos = i + len(word)
                    if end_pos == n or not text[end_pos].isalpha():
                        compressed_stream.append(self.marker_byte)
                        compressed_stream.append(self.word_to_id[word])
                        i += len(word)
                        match_found = True
                        break
            if not match_found:
                char_bytes = text[i].encode('utf-8')
                compressed_stream.extend(char_bytes)
                i += 1
        
        final_data = zlib.compress(compressed_stream)
        with open(output_path, 'wb') as f:
            f.write(final_data)
        print(f"Done. Original: {os.path.getsize(input_path)}B, Compressed: {len(final_data)}B")

    def decompress(self, input_path, output_path):
        print(f"Decompressing {input_path}...")
        with open(input_path, 'rb') as f:
            compressed_data = f.read()
        try:
            stream = zlib.decompress(compressed_data)
        except zlib.error as e:
            print(f"Error: {e}")
            return

        decoded_text = []
        i = 0
        n = len(stream)
        while i < n:
            byte = stream[i]
            if byte == self.marker_byte:
                if i + 1 < n:
                    word_id = stream[i+1]
                    if word_id in self.id_to_word:
                        decoded_text.append(self.id_to_word[word_id])
                        i += 2
                    else:
                        decoded_text.append(chr(byte))
                        i += 1
                else:
                    break
            else:
                literal_bytes = bytearray()
                while i < n and stream[i] != self.marker_byte:
                    literal_bytes.append(stream[i])
                    i += 1
                decoded_text.append(literal_bytes.decode('utf-8'))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("".join(decoded_text))
        print(f"Restored to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['compress', 'decompress'])
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    c = SemanticCompressor()
    if args.action == 'compress': c.compress(args.input, args.output)
    else: c.decompress(args.input, args.output)
