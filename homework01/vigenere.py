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
    while len(keyword) < len(plaintext):
        keyword *= 2

    ls = [ord(i) for i in list(plaintext)]
    keys = [ord(j) for j in list(keyword)]

    for i in range(len(ls)):

        if 65 <= keys[i] <= 90:
            keys[i] -= 65
        elif 97 <= keys[i] <= 122:
            keys[i] -= 97

        if 97 <= ls[i] <= 122:
            ls[i] += keys[i]
            if ls[i] > 122:
                ls[i] -= 26
        elif 65 <= ls[i] <= 90:
            ls[i] += keys[i]
            if ls[i] > 90:
                ls[i] -= 26

    ciphertext = "".join(chr(i) for i in ls)

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
    while len(keyword) < len(ciphertext):
        keyword *= 2

    ls = [ord(i) for i in list(ciphertext)]
    keys = [ord(i) for i in list(keyword)]

    for i in range(len(ls)):
        if 65 <= keys[i] <= 90:
            keys[i] -= 65
        elif 97 <= keys[i] <= 122:
            keys[i] -= 97

        if 65 <= ls[i] <= 90:
            ls[i] -= keys[i]
            if ls[i] < 65:
                ls[i] += 26
        elif 97 <= ls[i] <= 122:
            ls[i] -= keys[i]
            if ls[i] < 97:
                ls[i] += 26

    plaintext = "".join(chr(i) for i in ls)
    return plaintext
