def caesar_cipher_encrypt(message, key, alphabet):
    encrypted_message = ""
    alphabet_length = len(alphabet)
    
    for char in message:
        if char in alphabet:
            # Find the position of the character in the alphabet
            char_index = alphabet.index(char)
            # Shift the character by the key and wrap around using modulo
            encrypted_index = (char_index + key) % alphabet_length
            # Get the encrypted character
            encrypted_char = alphabet[encrypted_index]
            # Append to the encrypted message
            encrypted_message += encrypted_char
        else:
            # If the character is not in the alphabet, leave it unchanged
            encrypted_message += char
    
    return encrypted_message

def caesar_cipher_decrypt(encrypted_message, key, alphabet):
    decrypted_message = ""
    alphabet_length = len(alphabet)
    
    for char in encrypted_message:
        if char in alphabet:
            # Find the position of the character in the alphabet
            char_index = alphabet.index(char)
            # Shift the character back by the key and wrap around using modulo
            decrypted_index = (char_index - key) % alphabet_length
            # Get the decrypted character
            decrypted_char = alphabet[decrypted_index]
            # Append to the decrypted message
            decrypted_message += decrypted_char
        else:
            # If the character is not in the alphabet, leave it unchanged
            decrypted_message += char
    
    return decrypted_message

# Example usage:
alphabet = "abcdefghijklmnopqrstuvwxyz"
message = input('Enter message to encrypt (use lower case letters only): ')
key = int(input('Enter the value of the key (n): '))

encrypted_message = caesar_cipher_encrypt(message, key, alphabet)
print("Encrypted message:", encrypted_message)

decrypted_message = caesar_cipher_decrypt(encrypted_message, key, alphabet)
print("Decrypted message:", decrypted_message)