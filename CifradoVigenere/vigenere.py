def vigenere_encrypt(plaintext, key):
    """Función que encripta un texto usando el cifrado de Vigenère."""

    encrypted_text = ""
    key_index = 0

    # Itera sobre cada caracter del texto plano
    for char in plaintext:
        # Calcula el desplazamiento de la letra actual (usa el modulo para envolver la llave)
        shift = ord(key[key_index % len(key)]) - ord("a")
        # Encripta el caracter y lo agrega al texto cifrado
        encrypted_text += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        # Incrementa el índice de la clave
        key_index += 1
    return encrypted_text


def vigenere_decrypt(ciphertext, key):
    """Función que desencripta un texto usando el cifrado de Vigenère."""

    decrypted_text = ""
    key_index = 0

    # Itera sobre cada caracter del texto cifrado
    for char in ciphertext:
        # Calcula el desplazamiento de la letra actual (usa el modulo para envolver la llave)
        shift = ord(key[key_index % len(key)]) - ord("a")
        # Desencripta el caracter y lo agrega al texto descifrado
        decrypted_text += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
        # Incrementa el índice de la clave
        key_index += 1
    return decrypted_text


def main():
    """Función principal que encripta y desencripta un texto usando el cifrado de Vigenère."""

    # Obtiene el texto plano y la clave del usuario
    plaintext = input("Ingresa el mensaje a cifrar (solo minusculas): ").lower()
    key = input("Ingresa la llave (solo minusculas): ").lower()

    # Convierte el texto plano a minúsculas
    plaintext = plaintext.lower()

    # Encripta mensaje
    encrypted_text = vigenere_encrypt(plaintext, key)
    print("Texto encriptado: ", encrypted_text)

    # Desencripta mensaje
    decrypted_text = vigenere_decrypt(encrypted_text, key)
    print("Texto desencriptado: ", decrypted_text)


if __name__ == "__main__":
    main()
