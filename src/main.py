import argparse
import time
import unittest
import sys
import os

# Ajuste necesario para imports si ejecutas desde raíz
# Esto ayuda a que el unittest encuentre los tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cipher import SingularityCipher
from src.utils import leer_archivo, escribir_archivo, validar_ruta_sandbox, log_action
from src.key_manager import KeyManager
from src.analyzer import CryptoAnalyzer

def cmd_init(args):
    log_action("Comando INIT ejecutado.", "INFO")
    try:
        km = KeyManager()
        km.generate_and_save_key()
        log_action("Sistema inicializado. Nueva clave generada y guardada en escrow.", "SUCCESS")
        print("[OK] Sistema inicializado.")
    except Exception as e:
        log_action(f"FALLO al inicializar el sistema: {e}", "FATAL")
        print(f"[ERROR] {e}")

def cmd_encrypt(args):
    log_action(f"Comando ENCRYPT ejecutado. Input: {args.input}", "INFO")
    try:
        km = KeyManager()
        key = km.load_key()
        cipher = SingularityCipher(key)
        
        print(f"[*] Leyendo: {args.input}")
        data = leer_archivo(args.input)
        
        t0 = time.time()
        print("[*] Aplicando Singularity (Colapso Gravitacional)...")
        encrypted_data = cipher.encrypt(data)
        tf = time.time()
        duration = tf - t0
        
        escribir_archivo(args.output, encrypted_data)
        
        size_kb = len(data) / 1024
        log_action(f"Cifrado exitoso. Salida: {args.output}. Tiempo: {duration:.4f}s. Velocidad: {size_kb/duration:.2f} KB/s", "SUCCESS")
        print(f"[OK] Cifrado en {duration:.4f}s. Velocidad: {size_kb/duration:.2f} KB/s. Salida: {args.output}")
        
    except Exception as e:
        log_action(f"ERROR al cifrar {args.input}: {e}", "ERROR")
        print(f"[ERROR] {e}")

def cmd_decrypt(args):
    log_action(f"Comando DECRYPT ejecutado. Input: {args.input}", "INFO")
    try:
        km = KeyManager()
        key = km.load_key()
        cipher = SingularityCipher(key)
        
        print(f"[*] Descifrando: {args.input}")
        ciphertext = leer_archivo(args.input)
        
        t0 = time.time()
        decrypted_data = cipher.decrypt(ciphertext)
        tf = time.time()
        duration = tf - t0
        
        escribir_archivo(args.output, decrypted_data)
        
        log_action(f"Descifrado exitoso. Salida: {args.output}. Tiempo: {duration:.4f}s.", "SUCCESS")
        print(f"[OK] Descifrado en {duration:.4f}s. Salida: {args.output}")
        
    except Exception as e:
        log_action(f"ERROR al descifrar {args.input}: {e}", "ERROR")
        print(f"[ERROR] {e}")

def cmd_test(args):
    log_action("Comando TEST ejecutado. Corriendo suite de pruebas automatizadas.", "INFO")
    print("\n[*] EJECUTANDO SUITE DE PRUEBAS AUTOMATIZADAS...\n")
    try:
        loader = unittest.TestLoader()
        suite = loader.discover('tests')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            log_action("Pruebas unitarias completadas satisfactoriamente (SUCCESS).", "SUCCESS")
            print("\n[SUCCESS] El sistema Singularity es operativo y seguro.")
        else:
            log_action("Fallos detectados en las pruebas unitarias.", "ALERT")
            print("\n[FAIL] Se encontraron fallos en la integridad del sistema.")
            
    except Exception as e:
        log_action(f"ERROR Fatal al ejecutar los tests: {e}", "FATAL")
        print(f"[ERROR] Error fatal al ejecutar tests: {e}")

def cmd_analyze(args):
    log_action(f"Comando ANALYZE ejecutado. Input: {args.input}", "INFO")
    try:
        km = KeyManager()
        key = km.load_key()
        # Validamos ruta para asegurar que el path sea correcto para el Analyzer
        path = validar_ruta_sandbox(args.input)
        
        CryptoAnalyzer.generar_reporte(str(path), key)
        log_action("Reporte de análisis generado exitosamente.", "SUCCESS")
        
    except Exception as e:
        log_action(f"ERROR al analizar {args.input}: {e}", "ERROR")
        print(f"[ERROR] {e}")

def main():
    parser = argparse.ArgumentParser(description="Singularity Cipher CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comandos CLI
    subparsers.add_parser('init', help='Generar claves nuevas y escrow')
    subparsers.add_parser('test', help='Correr pruebas automatizadas')
    
    p_enc = subparsers.add_parser('encrypt', help='Cifrar archivo')
    p_enc.add_argument('input', help='Archivo de entrada (en sandbox/)')
    p_enc.add_argument('output', help='Archivo de salida (en sandbox/)')

    p_dec = subparsers.add_parser('decrypt', help='Descifrar archivo')
    p_dec.add_argument('input', help='Archivo cifrado')
    p_dec.add_argument('output', help='Archivo salida')
    
    p_an = subparsers.add_parser('analyze', help='Ver métricas de seguridad (Entropía/Avalancha)')
    p_an.add_argument('input', help='Archivo original para analizar')

    args = parser.parse_args()

    # Ejecución de comandos
    if args.command == 'init': cmd_init(args)
    elif args.command == 'encrypt': cmd_encrypt(args)
    elif args.command == 'decrypt': cmd_decrypt(args)
    elif args.command == 'test': cmd_test(args)
    elif args.command == 'analyze': cmd_analyze(args)

if __name__ == "__main__":
    main()