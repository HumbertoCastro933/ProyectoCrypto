import argparse
import sys
# Importaremos nuestros modulos (aun por crear la logica real)
# from src.cipher import MiCifrador
# from src.key_manager import generar_llaves

def cmd_init(args):
    print("[*] Inicializando sistema...")
    print("[*] Generando claves y guardando en escrow/recovery.enc...")
    # Aqui llamaremos a la logica de key_manager
    pass

def cmd_encrypt(args):
    print(f"[*] Cifrando archivo: {args.input} -> {args.output}")
    # 1. Leer archivo usando utils.leer_archivo (valida sandbox)
    # 2. Cargar clave
    # 3. Cifrar datos
    # 4. Guardar usando utils.escribir_archivo
    pass

def cmd_decrypt(args):
    print(f"[*] Descifrando archivo: {args.input} -> {args.output}")
    # Logica inversa a encrypt
    pass

def cmd_test(args):
    print("[*] Ejecutando suite de pruebas automatizadas...")
    # Aqui se puede invocar unittest o pytest programaticamente
    import unittest
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)

def main():
    parser = argparse.ArgumentParser(description="Herramienta de Cifrado Académico")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comando: init
    subparsers.add_parser('init', help='Generar claves y configurar entorno')

    # Comando: encrypt
    parser_enc = subparsers.add_parser('encrypt', help='Cifrar un archivo')
    parser_enc.add_argument('input', type=str, help='Archivo de entrada (en sandbox/)')
    parser_enc.add_argument('output', type=str, help='Archivo de salida (en sandbox/)')

    # Comando: decrypt
    parser_dec = subparsers.add_parser('decrypt', help='Descifrar un archivo')
    parser_dec.add_argument('input', type=str, help='Archivo cifrado (en sandbox/)')
    parser_dec.add_argument('output', type=str, help='Archivo descifrado (en sandbox/)')

    # Comando: test
    subparsers.add_parser('test', help='Correr pruebas automatizadas')

    args = parser.parse_args()

    # Mapeo de funciones
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'encrypt':
        cmd_encrypt(args)
    elif args.command == 'decrypt':
        cmd_decrypt(args)
    elif args.command == 'test':
        cmd_test(args)

if __name__ == "__main__":
    main()