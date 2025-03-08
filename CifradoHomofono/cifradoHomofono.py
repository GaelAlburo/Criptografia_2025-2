import random

tabla_homofona = {
    "A": ["00101010", "11010101", "10101010"],
    "B": ["01010101", "10110101", "11001100"],
    "C": ["00110011", "11001101", "10110001"],
    "D": ["01100110", "10011001", "11011011"],
    "E": ["00111100", "11000011", "10111101", "11110000"],
    "F": ["01001111", "10100101", "11000110"],
    "G": ["01111000", "10000111", "11101010"],
    "H": ["00101101", "11010010", "10101100"],
    "I": ["01011010", "10101001", "11001011"],
    "J": ["01101001", "10010110", "11100101"],
    "K": ["00110101", "11001010", "10110110"],
    "L": ["01001011", "10111000", "11011101"],
    "M": ["01110110", "10001001", "11101100"],
    "N": ["00111011", "11000100", "10111010"],
    "Ñ": ["01011100", "10100011", "11011110"],
    "O": ["01100010", "10011101", "11100001", "11010111"],
    "P": ["00101111", "11011000", "10101111"],
    "Q": ["01010011", "10110000", "11010011"],
    "R": ["01101101", "10010010", "11101111"],
    "S": ["00111111", "11000001", "10111110"],
    "T": ["01000101", "10111111", "11000111"],
    "U": ["01110001", "10001110", "11110011"],
    "V": ["00101001", "11010110", "10101011"],
    "W": ["01011001", "10100110", "11011001"],
    "X": ["01100101", "10011010", "11100110"],
    "Y": ["00110110", "11001001", "10110111"],
    "Z": ["01001101", "10110011", "11001110"],
}


def cifrar_homofono(palabra, tabla):
    """Cifra una palabra usando un cifrado homófono"""

    palabra_cifrada = []
    for letra in palabra.upper():
        if letra in tabla:
            homofono = random.choice(tabla[letra])  # Selecciona un homófono al azar
            palabra_cifrada.append(homofono)
        else:
            palabra_cifrada.append(
                letra
            )  # Si la letra no está en la tabla, se deja igual
    return " ".join(palabra_cifrada)


# Crear la tabla inversa de decodificación
tabla_inversa = {}
for letra, codigos in tabla_homofona.items():
    for codigo in codigos:
        tabla_inversa[codigo] = letra


def descifrar_homofono(mensaje_cifrado, tabla):
    """Descifra un mensaje cifrado con cifrado homófono"""

    palabra_descifrada = []
    for codigo in mensaje_cifrado.split():
        if codigo in tabla:
            palabra_descifrada.append(tabla[codigo])  # Se recupera la letra original
        else:
            palabra_descifrada.append("?")  # Si no se encuentra, se usa un marcador
    return "".join(palabra_descifrada)


def main():
    """Programa principal"""

    palabra = input("Ingrese la palabra a cifrar: ")
    cifrado = cifrar_homofono(palabra, tabla_homofona)
    print("Palabra: ", palabra)
    print("Palabra cifrada:", cifrado)
    descifrado = descifrar_homofono(cifrado, tabla_inversa)
    print("Mensaje descifrado:", descifrado)

    print("EJEMPLO DESCIFRADO, si la palabra descifrada es 'HOLA'")
    print("Mensaje cifrado: 00101101 01100010 01001011 00101010")
    descifrado = descifrar_homofono(
        "00101101 01100010 01001011 00101010", tabla_inversa
    )
    print("Mensaje descifrado:", descifrado)


if __name__ == "__main__":
    main()
