import struct
import hashlib

class SingularityCipher:
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("La clave debe ser de 128 bits (16 bytes).")
        self.key = key
        self.rounds = 16
        self.subkeys = self._generate_subkeys(key)

    def _generate_subkeys(self, main_key: bytes) -> list:
        subkeys = []
        for i in range(self.rounds):
            digest = hashlib.sha256(main_key + struct.pack('>I', i)).digest()
            subkey_int = struct.unpack('>I', digest[:4])[0]
            subkeys.append(subkey_int)
        return subkeys

    def _rotate_left(self, val: int, r_bits: int, max_bits=32) -> int:
        return ((val << r_bits) & (2**max_bits - 1)) | (val >> (max_bits - r_bits))

    def _f_function(self, right_half: int, subkey: int) -> int:
        # 1. Inyeccion de Energia
        state = right_half ^ subkey
        bytes_list = list(state.to_bytes(4, 'big'))
        
        # 2. Singularidad (Posicion del 'agujero negro')
        singularity_idx = subkey % 4
        singularity_mass = bytes_list[singularity_idx]
        
        # 3. Colapso Gravitacional
        for i in range(4):
            if i != singularity_idx:
                bytes_list[i] = (bytes_list[i] + singularity_mass) % 256
        
        # 4. Dilatacion Temporal (Rotacion basada en masa)
        total_mass = sum(bytes_list)
        collapsed_int = int.from_bytes(bytes_list, 'big')
        shift_amount = total_mass % 32
        
        return self._rotate_left(collapsed_int, shift_amount)

    def _process_block(self, block: bytes, mode='encrypt') -> bytes:
        L, R = struct.unpack('>II', block)
        keys = self.subkeys if mode == 'encrypt' else self.subkeys[::-1]

        for subkey in keys:
            temp = R
            f_out = self._f_function(R, subkey)
            R = L ^ f_out
            L = temp

        return struct.pack('>II', R, L) # Swap final

    def _pad(self, data: bytes) -> bytes:
        block_size = 8
        padding_len = block_size - (len(data) % block_size)
        padding = bytes([padding_len] * padding_len)
        return data + padding

    def _unpad(self, data: bytes) -> bytes:
        padding_len = data[-1]
        if padding_len > 8 or padding_len == 0:
            raise ValueError("Padding inválido.")
        return data[:-padding_len]

    def encrypt(self, plaintext: bytes) -> bytes:
        padded_data = self._pad(plaintext)
        encrypted_blocks = []
        for i in range(0, len(padded_data), 8):
            block = padded_data[i : i+8]
            encrypted_blocks.append(self._process_block(block, 'encrypt'))
        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) % 8 != 0:
            raise ValueError("Tamaño de archivo corrupto.")
        decrypted_blocks = []
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i : i+8]
            decrypted_blocks.append(self._process_block(block, 'decrypt'))
        return self._unpad(b''.join(decrypted_blocks))