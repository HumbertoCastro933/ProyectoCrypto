import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cipher import SingularityCipher

class TestSingularity(unittest.TestCase):
    def setUp(self):
        self.key = b'0123456789ABCDEF'

    def test_reversibilidad(self):
        cipher = SingularityCipher(self.key)
        msg = b"PruebaDeSingularity"
        enc = cipher.encrypt(msg)
        dec = cipher.decrypt(enc)
        self.assertEqual(msg, dec)

    def test_padding(self):
        cipher = SingularityCipher(self.key)
        msg = b"123" 
        enc = cipher.encrypt(msg)
        self.assertEqual(len(enc) % 8, 0)
        self.assertEqual(cipher.decrypt(enc), msg)

if __name__ == '__main__':
    unittest.main()