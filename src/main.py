import argparse
import time
import unittest
import sys
import os

# Ajuste necesario para imports si ejecutas desde raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cipher import SingularityCipher
from src.utils import leer_archivo, escribir_archivo, validar_ruta_sandbox
from src.key_manager import KeyManager
from src.analyzer import CryptoAnalyzer

def cmd_init(args):
    try:
        km = KeyManager()
        km.generate_and_save_key()
        print("[OK] Sistema inicializado.")
    except Exception as e:
        print(f"[ERROR] {e}")

def cmd_encrypt(args):
    try:
        km = KeyManager()
        key = km.load_key()
        cipher = SingularityCipher(key)
        
        print(f"[*] Leyendo: {args.input}")
        data = leer_archivo(args.input)
        
        t0 = time.time()
        enc_data = cipher.encrypt(data)
        tf = time.time()
        
        escribir_archivo(args.output, enc_data)
        print(f"[OK] Cifrado en {tf-t0:.4f}s. Salida: {args.output}")
    except Exception as e:
        print(f"[ERROR] {e}")

def cmd_decrypt(args):
    try:
        km = KeyManager()
        key = km.load_key()
        cipher = SingularityCipher(key)
        
        print(f"[*] Descifrando: {args.input}")
        data = leer_archivo(args.input)
        
        t0 = time.time()
        dec_data = cipher.decrypt(data)
        tf = time.time()
        
        escribir_archivo(args.output, dec_data)
        print(f"[OK] Descifrado en {tf-t0:.4f}s. Salida: {args.output}")
    except Exception as e:
        print(f"[ERROR] {e}")

def cmd_test(args):
    print("[*] Ejecutando Tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def cmd_analyze(args):
    try:
        km = KeyManager()
        key = km.load_key()
        # Hack para resolver ruta absoluta para analyzer
        path = validar_ruta_sandbox(args.input)
        CryptoAnalyzer.generar_reporte(str(path), key)
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    parser = argparse.ArgumentParser(description="Singularity Cipher")
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('init')
    subparsers.add_parser('test')
    
    p_enc = subparsers.add_parser('encrypt')
    p_enc.add_argument('input')
    p_enc.add_argument('output')

    p_dec = subparsers.add_parser('decrypt')
    p_dec.add_argument('input')
    p_dec.add_argument('output')
    
    p_an = subparsers.add_parser('analyze')
    p_an.add_argument('input')

    args = parser.parse_args()

    if args.command == 'init': cmd_init(args)
    elif args.command == 'encrypt': cmd_encrypt(args)
    elif args.command == 'decrypt': cmd_decrypt(args)
    elif args.command == 'test': cmd_test(args)
    elif args.command == 'analyze': cmd_analyze(args)

if __name__ == "__main__":
    main()