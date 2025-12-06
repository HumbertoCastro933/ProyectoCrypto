import sys
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox"
ESCROW_DIR = BASE_DIR / "escrow"

def validar_ruta_sandbox(ruta_archivo: str) -> Path:
    """Asegura que no salgan de la carpeta sandbox"""
    try:
        ruta_absoluta = (SANDBOX_DIR / ruta_archivo).resolve()
        # Verificamos si la ruta comienza con la ruta de sandbox
        if not str(ruta_absoluta).startswith(str(SANDBOX_DIR.resolve())):
            raise PermissionError
        return ruta_absoluta
    except (PermissionError, FileNotFoundError):
        print(f"[ALERTA DE SEGURIDAD] Acceso denegado fuera de Sandbox: {ruta_archivo}")
        sys.exit(1)

def leer_archivo(ruta: str) -> bytes:
    ruta_segura = validar_ruta_sandbox(ruta)
    if not ruta_segura.exists():
        raise FileNotFoundError(f"El archivo {ruta} no existe en sandbox/.")
    with open(ruta_segura, 'rb') as f:
        return f.read()

def escribir_archivo(ruta: str, datos: bytes):
    ruta_segura = validar_ruta_sandbox(ruta)
    with open(ruta_segura, 'wb') as f:
        f.write(datos)