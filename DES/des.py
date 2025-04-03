# Autor: Rodrigo Gael Guzman Alburo

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

# Step 0: Get message and encode it to binary
def print_bits(m_bits, int_space):
    count = 0
    for b in m_bits:
        print(b, end="")
        count += 1
        if count == int_space:
            print(" ", end="")
            count = 0
    print()


def string_to_bits(m):
    bytes_m = m.encode("utf-8")
    print(bytes_m)
    bit_string = "".join(format(byte_m, "08b") for byte_m in bytes_m)
    print(bit_string, 8)
    return bit_string


def hex_to_bits(hex_string):
    # Remove any spaces or '0x' prefix if present
    hex_string = hex_string.strip().replace(" ", "").replace("0x", "")

    # Convert hex string to bytes (requires even-length hex)
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string  # Pad with leading zero if odd length

    byte_data = bytes.fromhex(hex_string)

    # Convert each byte to 8 bits and concatenate
    bit_string = "".join(format(byte, "08b") for byte in byte_data)
    print_bits(bit_string, 4)
    return bit_string


## END STEP 0

# STEP 1: Create 16 subkeys, each of which is 48-bits long.

# Matriz PC1
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

Cn_subkeys = [None] * 17 # Array with 17 elements for the original and 16 subkeys (C0, C1, ..., C17)
Dn_subkeys = [None] * 17

def pc1_permutation(key):
    new_key = "".join(key[pos - 1] for pos in PC1)
    # print("NEW KEY")
    # print_bits(new_key, 7)
    # Split the permutated key:
    C0 = new_key[0:28]
    D0 = new_key[28:]
    # print("C0:")
    # print_bits(C0, 7)
    # print("D0:")
    # print_bits(D0, 7)
    return C0, D0


def left_shift_keys(C, D, number_shifts):
    Cn = C[number_shifts:] + C[:number_shifts]
    Dn = D[number_shifts:] + D[:number_shifts]

    return Cn, Dn

# Step 1.3: Apply permutations on the 16 keys (Kn = Cn+Dn)
PC2 = (
    14, 17, 11, 24,  1,  5,  3, 28,
    15,  6, 21, 10, 23, 19, 12,  4,
    26,  8, 16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55, 30, 40, 
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
)

subkeys = [None] * 16

def pc2_permutation(Cn, Dn):
    pre_key = Cn + Dn
    new_key = "".join(pre_key[pos-1] for pos in PC2)
    return new_key

# END STEP 1

# STEP 2: Encode each 64-bit block of data
# Step 2.1: Get the initial permutation of the message
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

def initial_permutation(m):
    ip = "".join(m[pos-1] for pos in IP)
    return ip[:32], ip[32:] # Returns the Left and Right side of IP

# Step 2.2: 16 iterations of the feistel function

# Expansion permutation
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


def feistel(R, K):
    new_R = "".join(R[pos-1] for pos in E)
    xor_r_k = "".join(str(int(x) ^ int(y)) for x,y in zip(K, new_R))
    count = 0
    #for i in range(8):


def get_n_keys(L, R, K):
    Ln = R
    Rn = L + feistel(R, K)
    return Ln, Rn

if __name__ == "__main__":
    print("Input the message:", end=" ")
    message = input()
    binary_message = hex_to_bits(message)

    print("Input the key:", end=" ")
    key = input()
    binary_key = hex_to_bits(key)

    # Step 1.1: PC1 permutation
    C0, D0 = pc1_permutation(binary_key)
    Cn_subkeys[0] = C0
    Dn_subkeys[0] = D0

    # Step 1.2: Creating 16 Cn and Dn
    for i in range(1, 17):
        if i in (1, 2, 9, 16):
            Cn_subkeys[i], Dn_subkeys[i] = left_shift_keys(
                Cn_subkeys[i - 1], Dn_subkeys[i - 1], 1
            )
        else:
            Cn_subkeys[i], Dn_subkeys[i] = left_shift_keys(
                Cn_subkeys[i - 1], Dn_subkeys[i - 1], 2
            )

    for i in range(len(Cn_subkeys)):
        print(f"Turn C{i}: {Cn_subkeys[i]}")
        print(f"Turn D{i}: {Dn_subkeys[i]}")
        print()

    # Step 1.3: PC2 permutation on the 16 keys
    for i in range(16):
        subkeys[i] = pc2_permutation(Cn_subkeys[i+1], Dn_subkeys[i+1])

    for i in range(len(subkeys)):
        print(f"Key {i+1}: {subkeys[i]}")

    ip_message_l, ip_message_r = initial_permutation(binary_message)
    print("\nL and R permuted message")
    print_bits(ip_message_l, 4)
    print_bits(ip_message_r, 4)


