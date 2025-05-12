class AES128:

    def __init__(self, key):
        self.key = key
        self.round_keys = self.key_expansion(key) # Genera las 10 llaves por ronda

    def print_matrix(self, matrix):
        # Imprime la matriz de bytes en formato hexadecimal
        for row in matrix:
            print(" ".join(f"{byte:02x}" for byte in row))
        print()


    def encrypt(self, plaintext):

        # Se aplica el relleno PKCS7 para que el texto plano sea un múltiplo de 16 bytes
        ##plaintext = self.pad(plaintext)

        # Convierte el texto plano a una matriz de bytes
        # AES utiliza una matriz de 4x4 bytes para representar el estado
        # El texto plano debe ser un múltiplo de 16 bytes
        # de lo contrario, se debe rellenar 
        state = self.bytes_to_matrix(plaintext)

        # Imprime el estado inicial
        print("Estado inicial:")
        self.print_matrix(state)

        print("Round key 0: ", self.round_keys[0])
        print("Round key 1: ", self.round_keys[1])

        # Ronda inicial
        # Añadir la clave de ronda inicial
        state = self.add_round_key(state, self.round_keys[0])

        # Imprime el estado después de la ronda inicial
        print("Estado después de add_round_key:")
        self.print_matrix(state)

        # 9 rondas principales
        for i in range(1, 10):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, self.round_keys[i])

        # Última ronda
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.round_keys[10])

        # Convierte la matriz de bytes de vuelta a texto cifrado
        return self.matrix_to_bytes(state)
    
    def sub_bytes(self, state):
        # Sustituye cada byte en el estado por su correspondiente en la S-box
        for i in range(4):
            for j in range(4):
                state[i][j] = self.sbox[state[i][j]]
        return state
    
    def shift_rows(self, state):
        # Desplaza las filas de la matriz de estado cíclicamente:
        # Fila 0 no se desplaza
        # Fila 1 se desplaza 1 a la izquierda
        # Fila 2 se desplaza 2 a la izquierda
        # Fila 3 se desplaza 3 a la izquierda

        state[1] = state[1][1:] + state[1][:1] # Rota 1 byte a la izquierda
        state[2] = state[2][2:] + state[2][:2] # Rota 2 bytes a la izquierda
        state[3] = state[3][3:] + state[3][:3] # Rota 3 bytes a la izquierda
        return state
    
    def mix_columns(self, state):
        # Mezcla las columnas del estado
        # Cada columna se trata como un polinomio en GF(2^8) y se multiplica por una matriz fija
        
        for i in range(4): # Para cada columna
            # Multiplica la columna por la matriz de mezcla
            s0 = self.gmul(0x02, state[0][i]) ^ self.gmul(0x03, state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ self.gmul(0x02, state[1][i]) ^ self.gmul(0x03, state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ self.gmul(0x02, state[2][i]) ^ self.gmul(0x03, state[3][i])
            s3 = self.gmul(0x03, state[0][i]) ^ state[1][i] ^ state[2][i] ^ self.gmul(0x02, state[3][i])
            
            state[0][i] = s0 & 0xFF  # Asegurar que es 1 byte
            state[1][i] = s1 & 0xFF
            state[2][i] = s2 & 0xFF
            state[3][i] = s3 & 0xFF
        return state
    
    def add_round_key(self, state, round_key):
        # Añade la clave de ronda al estado mediante una operación XOR
        # Estado XOR Clave de ronda
        # Proporciona confusión y difusión
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i][j] % 256 # Asegura que el resultado esté en el rango de 0-255
        return state
    
    def key_expansion(self, key):
        
        key_columns = self.bytes_to_matrix(key) # Convierte la clave a una matriz de bytes
        # Expande la clave para generar las claves de ronda
        expanded_key = [column for column in key_columns]

        # Genera las claves de ronda
        for i in range(4, 4*11): # 11 rondas * 4 palabras por ronda
            temp = expanded_key[i-1] # Última palabra de la clave expandida
            if i % 4 == 0:
                # RotWord: rota la palabra 1 byte a la izquierda
                temp = temp
                # SubWord: sustituye cada byte por su correspondiente en la S-box
                temp = [self.sbox[b] for b in temp]
                # XOR con Rcon
                temp[0] ^= self.r_con[i//4]

            # Genera la nueva palabra
            # XOR con la palabra 4 posiciones atrás
            expanded_key.append([a ^ b for a,b in zip(expanded_key[i-4], temp)])

        # Agrega las claves de ronda a la lista
        return [expanded_key[i*4 : (i+1)*4] for i in range(len(expanded_key)//4)]
    
    ## FUNCIONES AUXILIARES ##
    def gmul(self, a, b):
        # Multiplicación en el campo de Galois GF(2^8)
        # con poliniomio irreducible x^8 + x^4 + x^3 + x + 1
        p = 0
        for _ in range(8): # Se usa _ para ignorar el valor de la variable
            if b & 1:
                p ^= a
            a <<= 1
            if a & 0x80:
                a ^= 0x1b # Polinomio irreducible
            b >>= 1
        return p & 0xFF # Asegura que el resultado esté en el rango de 0-255
    
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

    # Rcon: constantes de la clave de ronda
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

# Ejemplo de uso
if __name__ == "__main__":
    key_plain = b"Thats my Kung Fu"
    plaintext = b"Two One Nine Two"

    aes = AES128(key_plain)
    ciphertext = aes.encrypt(plaintext)
    print("Texto plano:", plaintext)
    print("Texto plano (hex):", plaintext.hex())
    print("Clave:", key_plain)
    print("Clave (hex):", key_plain.hex())
    print("Texto cifrado:", ciphertext.hex())