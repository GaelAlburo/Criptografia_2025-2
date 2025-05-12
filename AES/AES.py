class AES128:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long")
        self.key = key
        self.round_keys = self.key_expansion(key)

    def encrypt(self, plaintext):
        # Asegura que el texto plano sea de 16 bytes
        if len(plaintext) != 16:
            raise ValueError("Plaintext must be 16 bytes long")

        # Convierte el texto plano a una matriz de bytes
        state = self.bytes_to_matrix(plaintext)

        # Impresión de estado inicial y claves de ronda
        print("Estado inicial:")
        self.print_matrix(state)
        
        print("Round key 0: ", self.round_keys[0])

        # Ronda inicial: AddRoundKey
        state = self.add_round_key(state, self.round_keys[0])

        print("Estado después de add_round_key:")
        self.print_matrix(state)

        # 9 rondas principales
        for i in range(1, 10):
            print(f"Round key {i}: ", self.round_keys[i])
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, self.round_keys[i])
            print(f"Estado después de ronda {i}:")
            self.print_matrix(state)

        # Última ronda (sin MixColumns)
        print("Round key 10: ", self.round_keys[10])
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.round_keys[10])

        # Convierte la matriz de bytes de vuelta a texto cifrado
        return self.matrix_to_bytes(state)
    
    def decrypt(self, ciphertext):
        # Asegura que el texto cifrado sea de 16 bytes
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext must be 16 bytes long")

        # Convierte el texto cifrado a una matriz de bytes
        state = self.bytes_to_matrix(ciphertext)

        # Impresión de estado inicial y claves de ronda
        print("Estado inicial:")
        self.print_matrix(state)
        
        print("Round key 10: ", self.round_keys[10])

        # Ronda inicial: AddRoundKey
        state = self.add_round_key(state, self.round_keys[10])

        print("Estado después de add_round_key:")
        self.print_matrix(state)

        # 9 rondas principales
        for i in range(9, 0, -1):
            print(f"Round key {i}: ", self.round_keys[i])
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, self.round_keys[i])
            state = self.inv_mix_columns(state)
            print(f"Estado después de ronda {i}:")
            self.print_matrix(state)

        # Última ronda (sin InvMixColumns)
        print("Round key 0: ", self.round_keys[0])
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, self.round_keys[0])

        # Convierte la matriz de bytes de vuelta a texto descifrado
        return self.matrix_to_bytes(state)
    
    def print_matrix(self, matrix):
        # Imprime la matriz de bytes en formato hexadecimal
        for row in matrix:
            print(" ".join(f"{byte:02x}" for byte in row))
        print()
    
    def sub_bytes(self, state):
        # Sustituye cada byte en el estado por su correspondiente en la S-box
        return [[self.sbox[state[i][j]] for j in range(4)] for i in range(4)]
    
    def inv_sub_bytes(self, state):
        # Sustituye cada byte en el estado por su correspondiente en la S-box inversa
        return [[self.inv_s_box[state[i][j]] for j in range(4)] for i in range(4)]
    
    def shift_rows(self, state):
        # Crea una nueva matriz para el estado
        new_state = [row[:] for row in state]
        
        # Primera fila (índice 0) no se desplaza
        
        # Segunda fila (índice 1) se desplaza 1 a la izquierda
        new_state[1] = [state[1][1], state[1][2], state[1][3], state[1][0]]
        
        # Tercera fila (índice 2) se desplaza 2 a la izquierda
        new_state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
        
        # Cuarta fila (índice 3) se desplaza 3 a la izquierda
        new_state[3] = [state[3][3], state[3][0], state[3][1], state[3][2]]
        
        return new_state
    
    def inv_shift_rows(self, state):
        # Crea una nueva matriz para el estado
        new_state = [row[:] for row in state]
        
        # Primera fila (índice 0) no se desplaza
        
        # Segunda fila (índice 1) se desplaza 3 a la derecha
        new_state[1] = [state[1][3], state[1][0], state[1][1], state[1][2]]
        
        # Tercera fila (índice 2) se desplaza 2 a la derecha
        new_state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
        
        # Cuarta fila (índice 3) se desplaza 1 a la derecha
        new_state[3] = [state[3][1], state[3][2], state[3][3], state[3][0]]
        
        return new_state
    
    def mix_columns(self, state):
        # Crea una nueva matriz para almacenar el resultado
        new_state = [[0]*4 for _ in range(4)]
        
        for c in range(4):  # Para cada columna
            new_state[0][c] = (self.gmul(0x02, state[0][c]) ^ 
                               self.gmul(0x03, state[1][c]) ^ 
                               state[2][c] ^ 
                               state[3][c])
            new_state[1][c] = (state[0][c] ^ 
                               self.gmul(0x02, state[1][c]) ^ 
                               self.gmul(0x03, state[2][c]) ^ 
                               state[3][c])
            new_state[2][c] = (state[0][c] ^ 
                               state[1][c] ^ 
                               self.gmul(0x02, state[2][c]) ^ 
                               self.gmul(0x03, state[3][c]))
            new_state[3][c] = (self.gmul(0x03, state[0][c]) ^ 
                               state[1][c] ^ 
                               state[2][c] ^ 
                               self.gmul(0x02, state[3][c]))
        
        return new_state
    
    def inv_mix_columns(self, state):
        # Crea una nueva matriz para almacenar el resultado
        new_state = [[0]*4 for _ in range(4)]
        
        for c in range(4):
            new_state[0][c] = (self.gmul(0x0e, state[0][c]) ^ 
                               self.gmul(0x0b, state[1][c]) ^ 
                               self.gmul(0x0d, state[2][c]) ^ 
                               self.gmul(0x09, state[3][c]))
            new_state[1][c] = (self.gmul(0x09, state[0][c]) ^ 
                               self.gmul(0x0e, state[1][c]) ^ 
                               self.gmul(0x0b, state[2][c]) ^ 
                               self.gmul(0x0d, state[3][c]))
            new_state[2][c] = (self.gmul(0x0d, state[0][c]) ^ 
                               self.gmul(0x09, state[1][c]) ^ 
                               self.gmul(0x0e, state[2][c]) ^ 
                               self.gmul(0x0b, state[3][c]))
            new_state[3][c] = (self.gmul(0x0b, state[0][c]) ^ 
                               self.gmul(0x0d, state[1][c]) ^ 
                               self.gmul(0x09, state[2][c]) ^ 
                               self.gmul(0x0e, state[3][c]))
        return new_state
    
    def gmul(self, a, b):
        # Multiplicación en el campo de Galois GF(2^8)
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            if hi_bit_set:
                a ^= 0x1b  # Polinomio irreducible x^8 + x^4 + x^3 + x + 1
            b >>= 1
        return p & 0xFF
    
    def add_round_key(self, state, round_key):
        # Añade la clave de ronda al estado mediante una operación XOR
        return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]
    
    def key_expansion(self, key):
        def rot_word(word):
            return word[1:] + word[:1]
        
        def sub_word(word):
            return [self.sbox[b] for b in word]
        
        # Convierte la clave a una matriz de 4x4 donde cada columna es una palabra
        key_matrix = self.bytes_to_matrix(key)
        
        # Transformamos la matriz en palabras (columnas)
        w = []
        for j in range(4):
            word = [key_matrix[i][j] for i in range(4)]
            w.append(word)
        
        # Expandimos a 44 palabras (11 claves de ronda de 4 palabras cada una)
        for i in range(4, 44):
            temp = w[i-1][:]  # Copia la palabra anterior
            
            if i % 4 == 0:
                # Aplica RotWord, SubWord y XOR con Rcon
                temp = rot_word(temp)
                temp = sub_word(temp)
                temp[0] ^= self.r_con[i//4]
            
            # XOR con palabra 4 posiciones atrás
            w.append([a ^ b for a, b in zip(w[i-4], temp)])
        
        # Reorganiza las palabras en matrices de 4x4 para cada ronda
        round_keys = []
        for round_num in range(11):
            round_key = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(4):
                for i in range(4):
                    round_key[i][j] = w[round_num*4 + j][i]
            round_keys.append(round_key)
        
        return round_keys
    
    def bytes_to_matrix(self, text):
        return [
            [text[0], text[4], text[8], text[12]],
            [text[1], text[5], text[9], text[13]],
            [text[2], text[6], text[10], text[14]],
            [text[3], text[7], text[11], text[15]]
        ]
    
    def matrix_to_bytes(self, matrix):
        return bytes([
            matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0],
            matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1],
            matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2],
            matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3]
        ])
    
    # S-box de AES
    sbox = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]

    # S-box inversa de AES
    inv_s_box = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    )

    # Rcon: constantes de la clave de ronda
    r_con = (
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a,
        0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39
    )

# Ejemplo de uso
if __name__ == "__main__":
    #key_plain = b"Thats my Kung Fu"
    #plaintext = b"Two One Nine Two"

    print("\n------------------------------------------------------------\n")
    print("C I F R A D O  AES-128\n")
    key_plain = input("Ingrese la clave de 16 bytes: ").encode()
    plaintext = input("Ingrese el texto plano de 16 bytes: ").encode()

    aes = AES128(key_plain)
    ciphertext = aes.encrypt(plaintext)
    print("Texto plano:", plaintext)
    print("Texto plano (hex):", plaintext.hex())
    print("Clave:", key_plain)
    print("Clave (hex):", key_plain.hex())
    print("Texto cifrado:", ciphertext.hex())

    print("\n------------------------------------------------------------\n")
    print("D E S C I F R A D O  AES-128\n")

    # Desencriptar el texto cifrado
    cipher_text = bytes.fromhex("29c3505f571420f6402299b31a02d73a")
    aes_decrypt = AES128(key_plain)
    decrypted_text = aes_decrypt.decrypt(cipher_text)
    print("Texto cifrado:", cipher_text.hex())
    print("Texto cifrado (hex):", cipher_text.hex())
    print("Texto descifrado:", decrypted_text)
    print("Texto descifrado (hex):", decrypted_text.hex())
    print("Texto descifrado (ascii):", decrypted_text.decode())