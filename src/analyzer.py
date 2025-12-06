import math
import os
from collections import Counter
from src.cipher import SingularityCipher

class CryptoAnalyzer:
    @staticmethod
    def calcular_entropia(data: bytes) -> float:
        if not data: return 0.0
        frecuencias = Counter(data)
        total = len(data)
        return -sum((c/total) * math.log2(c/total) for c in frecuencias.values())

    @staticmethod
    def test_avalancha(key: bytes, data: bytes) -> float:
        cipher = SingularityCipher(key)
        c1 = cipher.encrypt(data)
        
        data_mut = bytearray(data)
        if len(data_mut) > 0:
            data_mut[0] ^= 1 # Cambiar 1 bit
        
        c2 = cipher.encrypt(bytes(data_mut))
        
        diffs = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(c1, c2))
        total_bits = len(c1) * 8
        return (diffs / total_bits) * 100.0 if total_bits > 0 else 0.0

    @staticmethod
    def generar_reporte(filepath: str, key: bytes):
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Validar que no este vacio
        if not data:
            print("El archivo está vacío. No se puede analizar.")
            return

        cipher = SingularityCipher(key)
        encrypted = cipher.encrypt(data)
        
        print(f"\n--- ANALISIS SINGULARITY ---")
        print(f"Archivo: {os.path.basename(filepath)}")
        print(f"Entropia Original: {CryptoAnalyzer.calcular_entropia(data):.4f}")
        print(f"Entropia Cifrado:  {CryptoAnalyzer.calcular_entropia(encrypted):.4f}")
        print(f"Avalancha:         {CryptoAnalyzer.test_avalancha(key, data):.2f}%")
        print("----------------------------\n")