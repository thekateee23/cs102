def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    a_low = ord("a")
    a_up = ord("A")
    alpha_length = ord("z") - ord("a") + 1
    shift = [keyword[i % len(keyword)] for i in range(len(plaintext))]

    for i, symbol in enumerate(plaintext):
        if symbol.isalpha():
            if symbol.isupper():
                ciphertext += chr((ord(symbol) + ord(shift[i])) % alpha_length + a_up)
            elif symbol.islower():
                ciphertext += chr((ord(symbol) + ord(shift[i]) - 2 * a_low) % alpha_length + a_low)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    a_low = ord("a")
    a_up = ord("A")
    alpha_length = ord("z") - ord("a") + 1
    shift = [keyword[i % len(keyword)] for i in range(len(ciphertext))]

    for i, symbol in enumerate(ciphertext):
        if symbol.isalpha():
            if symbol.isupper():
                plaintext += chr((ord(symbol) - ord(shift[i]) - 2 * a_up) % alpha_length + a_up)
            elif symbol.islower():
                plaintext += chr((ord(symbol) - ord(shift[i])) % alpha_length + a_low)
        else:
            plaintext += symbol
    return plaintext
