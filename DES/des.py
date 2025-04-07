# Autor: Rodrigo Gael Guzman Alburo
# Fecha: 07/04/2025

##############################################################
########## F U N C I O N E S    A U X I L I A R E S ##########
##############################################################

def str_to_int(bit_str):
    """Convierte bit string a entero."""
    return int(bit_str, 2)

def int_to_str(num, bit_length):
    """Convierte entero a bit string con longitud fija."""
    return format(num, f'0{bit_length}b')

def pad_to_64bits(bit_string):
    """Ajusta el bit string a 64 bits."""	
    if len(bit_string) < 64:
        return bit_string.ljust(64, '0')  # Pad with zeros
    elif len(bit_string) > 64:
        return bit_string[:64]  # Truncate if longer
    return bit_string

def bits_to_hex(bit_string):
    """Convierte un string de bits a hexadecimal."""
    # Agregar ceros a la izquierda para que la longitud sea un múltiplo de 4 si es necesario
    padding = (4 - len(bit_string) % 4) % 4
    padded_bits = '0' * padding + bit_string
    
    # Convierte cada 4 bits a un caracter hexadecimal
    hex_chars = []
    for i in range(0, len(padded_bits), 4):
        chunk = padded_bits[i:i+4]
        hex_chars.append(f"{int(chunk, 2):x}")
    
    return ''.join(hex_chars)

def print_bits(m_bits, int_space):
    """Imprime un string de bits con espacios."""
    count = 0
    for b in m_bits:
        print(b, end="")
        count += 1
        if count == int_space:
            print(" ", end="")
            count = 0
    print()


def string_to_bits(m):
    """Convierte un string a su representación en bits."""
    bytes_m = m.encode("utf-8")
    bit_string = "".join(format(byte_m, "08b") for byte_m in bytes_m)
    return bit_string


def hex_to_bits(hex_string):
    """Convierte un string hexadecimal a su representación en bits."""	
    # Elimina espacios y "0x" del string hexadecimal
    hex_string = hex_string.strip().replace(" ", "").replace("0x", "")

    # Convierte el string hexadecimal a bytes (requiere longitud par)
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string  # Agrega un cero al inicio si es impar

    byte_data = bytes.fromhex(hex_string)

    # Convierte cada byte a 8 bits y concatena
    bit_string = "".join(format(byte, "08b") for byte in byte_data)
    pad_bits = pad_to_64bits(bit_string)
    return pad_bits

##############################################################
########## T A B L A S    P E R M U T A C I O N E S ##########
##############################################################

S1 = [
    [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
    [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
    [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
    [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
]

S2 = [
    [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
    [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
    [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
    [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
]

S3 = [
    [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
    [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
    [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
    [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
]

S4 = [
    [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
    [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
    [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
    [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
]

S5 = [
    [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
    [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
    [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
    [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
]

S6 = [
    [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
    [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
    [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
    [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
]

S7 = [
    [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
    [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
    [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
    [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
]

S8 = [
    [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
    [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
    [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
    [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
]

# Permutacion PC1
PC1 = (
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
)

# Permutacion PC2
PC2 = (
    14, 17, 11, 24,  1,  5,  3, 28,
    15,  6, 21, 10, 23, 19, 12,  4,
    26,  8, 16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55, 30, 40, 
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
)

# Permutación inicial del mensaje
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)

# Permutación de expansión
E = (
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
)

# Permutación P
P = (
    16,  7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26,  5, 18, 31, 10,
    2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
)

# Permutación final
FIP = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
)

################################################
########## A L G O R I T M O    D E S ##########
################################################

def pc1_permutation(key):
    """Permutación inicial de la llave (PC1). Retorna C0 y D0"""

    new_key = "".join(key[pos - 1] for pos in PC1)
    C0 = new_key[0:28]
    D0 = new_key[28:]
    return C0, D0

def left_shift_keys(C, D, number_shifts):
    """Realiza un desplazamiento a la izquierda de C y D según el número de desplazamientos.
    Retorna Cn y Dn"""

    Cn = C[number_shifts:] + C[:number_shifts]
    Dn = D[number_shifts:] + D[:number_shifts]

    return Cn, Dn

def pc2_permutation(Cn, Dn):
    """Permutación PC2 de la llave Dn+Cn. Retorna Kn"""

    pre_key = Cn + Dn
    new_key = "".join(pre_key[pos-1] for pos in PC2)
    return new_key

def initial_permutation(m):
    """Aplica la permutación inicial (IP) al mensaje m. Retorna L y R"""

    ip = "".join(m[pos-1] for pos in IP)
    return ip[:32], ip[32:] # Returns the Left and Right side of IP

def feistel(R, K):
    """Aplica la función de Feistel al lado derecho R y la llave K.
    Retorna el resultado de la función de Feistel"""

    new_R = "".join(R[pos-1] for pos in E)

    # Transforma E(Rn) y Kn a enteros para un mejor rendimiento al aplicar XOR
    R_int = str_to_int(new_R)
    K_int = str_to_int(K)
    xor_r_k = R_int ^ K_int 

    # Transforma (Rn XOR Kn) de entero a string
    xor_str = int_to_str(xor_r_k, 48)

    # Aplica 16 S-boxes:
    s_boxes_result = []
    for i in range(8):
        block_6bit = xor_str[i*6 : (i+1)*6]
        row = int(block_6bit[0] + block_6bit[5], 2)
        col = int(block_6bit[1:5], 2)
        s_value = globals()[f"S{i+1}"][row][col] # Gets the rol/col value of specific S-box
        s_boxes_result.append(int_to_str(s_value, 4))

    feistel_result = ''.join(''.join(s_boxes_result)[pos-1] for pos in P)
    return feistel_result

def des_round(L, R, K):
    """Realiza una ronda de DES. Aplica la función de Feistel y retorna R y L"""

    feistel_res = feistel(R, K)
    newR_int = str_to_int(L) ^ str_to_int(feistel_res)
    return R, int_to_str(newR_int, 32)

def get_n_keys(L, R, K):
    """Genera la subllave Kn y retorna L y R"""

    Ln = R
    Rn = L + feistel(R, K)
    return Ln, Rn

def create_subkeys(binary_key):
    """Genera las 16 subllaves de DES a partir de la llave original.
    Retorna una lista con las 16 subllaves"""

    # Arreglo con 17 elements para la subllave original y el resto de las 16 (C0, C1, ..., C17)
    Cn_subkeys = [None] * 17
    Dn_subkeys = [None] * 17

    # 1. Permutacion PC1
    C0, D0 = pc1_permutation(binary_key)
    Cn_subkeys[0] = C0
    Dn_subkeys[0] = D0

    # 2. Creación de 16 Cn y Dn
    for i in range(1, 17):
        if i in (1, 2, 9, 16):
            Cn_subkeys[i], Dn_subkeys[i] = left_shift_keys(
                Cn_subkeys[i - 1], Dn_subkeys[i - 1], 1
            )
        else:
            Cn_subkeys[i], Dn_subkeys[i] = left_shift_keys(
                Cn_subkeys[i - 1], Dn_subkeys[i - 1], 2
            )

    # 3. Permutacion PC2 de las 16 llaves
    subkeys = [None] * 16
    for i in range(16):
        subkeys[i] = pc2_permutation(Cn_subkeys[i+1], Dn_subkeys[i+1])

    return subkeys

def final_permutation(m):
    """Aplica la permutación final (FIP) al mensaje m. Retorna el mensaje final"""

    final = ''.join(m[pos-1] for pos in FIP)
    return final

def encrypt_message():
    """Función principal para cifrar el mensaje utilizando DES."""

    print("Input the message:", end=" ")
    message = input().strip()
    #binary_message = hex_to_bits(message)
    binary_message = string_to_bits(message)

    print("Input the key:", end=" ")
    key = input().strip()
    #binary_key = hex_to_bits(key)
    binary_key = string_to_bits(key)

    # Generar 16 subllaves
    subkeys = create_subkeys(binary_key)

    # Aplica la permutación inicial (igual que encripcion)
    L, R = initial_permutation(binary_message)

    # 16 rondas de Feistel con las subllaves
    for i in range(16):
        L, R = des_round(L, R, subkeys[i])

    # Se aplica la permutaciópn final
    cypher_text = final_permutation(R + L)

    print(f"Encrypted message: {bits_to_hex(cypher_text).upper()}")

def decrypt_message():
    """Función principal para descifrar el mensaje utilizando DES."""

    print("Input the crypted message:", end=" ")
    message = input().strip()
    #binary_message = hex_to_bits(message)
    binary_message = string_to_bits(message)

    print("Input the key:", end=" ")
    key = input().strip()
    #binary_key = hex_to_bits(key)
    binary_key = string_to_bits(key)

    # Crea 16 subllaves
    subkeys = create_subkeys(binary_key)
    
    # Invierte el orden de las subllaves para el descifrado
    reversed_subkeys = subkeys[::-1]  # Llaves K16 a K1

    # Aplica la permutación inicial (igual que encripcion)
    L, R = initial_permutation(binary_message)

    # 16 rondas de Feistel con las subllaves invertidas
    for i in range(16):
        L, R = des_round(L, R, reversed_subkeys[i])

    # Se aplica la permutaciópn final
    plaintext = final_permutation(R + L)

    print(f"Decrypted message: {bits_to_hex(plaintext).upper()}")

if __name__ == "__main__":

    #encrypt_message()

    decrypt_message()