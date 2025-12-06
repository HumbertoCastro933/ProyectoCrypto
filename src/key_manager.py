import os
import secrets
from src.cipher import SingularityCipher
from src.utils import ESCROW_DIR

# Clave maestra simulada de la institucion
RECOVERY_MASTER_KEY = b'MASTER_KEY_ADMIN' 

class KeyManager:
    def __init__(self):
        self.escrow_path = ESCROW_DIR / "recovery.enc"
        self.cipher = SingularityCipher(RECOVERY_MASTER_KEY)

    def generate_and_save_key(self) -> bytes:
        new_key = secrets.token_bytes(16)
        encrypted_key = self.cipher.encrypt(new_key)
        
        if not ESCROW_DIR.exists():
            os.makedirs(ESCROW_DIR)
            
        with open(self.escrow_path, 'wb') as f:
            f.write(encrypted_key)
        
        print(f"[KeyManager] Llave generada y guardada en escrow.")
        return new_key

    def load_key(self) -> bytes:
        if not self.escrow_path.exists():
            raise FileNotFoundError("No hay llaves. Ejecuta 'init' primero.")
            
        with open(self.escrow_path, 'rb') as f:
            encrypted_key = f.read()
            
        return self.cipher.decrypt(encrypted_key)