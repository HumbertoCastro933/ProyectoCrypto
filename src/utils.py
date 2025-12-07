import os
import sys
from pathlib import Path
from datetime import datetime

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox"
ESCROW_DIR = BASE_DIR / "escrow"
LOG_FILE = BASE_DIR / "execution.log"

def validar_ruta_sandbox(ruta_archivo: str) -> Path:
    """Asegura que no salgan de la carpeta sandbox"""
    try:
        # Resolve path to ensure absolute comparison
        ruta_absoluta = (SANDBOX_DIR / ruta_archivo).resolve()
        
        # Check if the absolute path starts with the absolute SANDBOX path
        if not str(ruta_absoluta).startswith(str(SANDBOX_DIR.resolve())):
            raise PermissionError
        return ruta_absoluta
    except (PermissionError, FileNotFoundError):
        log_action(f"Intento de acceso fuera de Sandbox detectado: {ruta_archivo}", "SECURITY_VIOLATION")
        print(f"[ALERTA DE SEGURIDAD] Acceso denegado fuera de Sandbox: {ruta_archivo}")
        sys.exit(1)

def leer_archivo(ruta: str) -> bytes:
    ruta_segura = validar_ruta_sandbox(ruta)
    if not ruta_segura.exists():
        log_action(f"FALLO: Archivo no encontrado en Sandbox: {ruta}", "ERROR")
        raise FileNotFoundError(f"El archivo {ruta} no existe en sandbox.")
    with open(ruta_segura, 'rb') as f:
        return f.read()

def escribir_archivo(ruta: str, datos: bytes):
    ruta_segura = validar_ruta_sandbox(ruta)
    with open(ruta_segura, 'wb') as f:
        f.write(datos)

def log_action(mensaje: str, nivel: str = "INFO"):
    """Escribe un mensaje en el archivo execution.log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Aseguramos que el directorio exista (debería ser la raíz del proyecto)
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)
        
    linea_log = f"[{timestamp}] [{nivel}] {mensaje}\n"
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(linea_log)
    except Exception as e:
        # En caso de que falle el log, al menos lo imprime
        print(f"[FATAL LOG ERROR] No se pudo escribir en el log: {e}")