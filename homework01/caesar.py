from string import punctuation


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for elem in plaintext:
        if 65 <= ord(elem) <= 90:
            ciphertext += chr(((ord(elem) - 65 + shift) % 26) + 65)
        elif 97 <= ord(elem) <= 122:
            ciphertext += chr(((ord(elem) - 97 + shift) % 26) + 97)
        else:
            ciphertext += elem
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    shift %= 26
    plaintext = ""
    for elem in ciphertext:
        if elem == " " or elem.isdigit() or elem in punctuation:
            plaintext += elem
        elif ((ord(elem) - shift) < 97) and ((ord(elem) - shift) > 90):
            plaintext += chr((ord(elem) - shift) + 26)
        elif (ord(elem) - shift) < 65:
            plaintext += chr((ord(elem) - shift) + 26)
        else:
            plaintext += chr(ord(elem) - shift)
    return plaintext
