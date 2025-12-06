import unittest
from src.cipher import MiAlgoritmoCipher

class TestCifrado(unittest.TestCase):
    def test_reversible(self):
        """Prueba de integridad basica: Dec(Enc(M)) == M"""
        key = b'0000000000000000' # Ejemplo de clave 16 bytes
        cipher = MiAlgoritmoCipher(key)
        mensaje = b"Hola Mundo Crypto"
        
        cifrado = cipher.encrypt_file(mensaje)
        descifrado = cipher.decrypt_file(cifrado)
        
        self.assertEqual(mensaje, descifrado, "El descifrado no recuperó el mensaje original")

if __name__ == '__main__':
    unittest.main()