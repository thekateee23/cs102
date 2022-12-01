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
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha() and ciphertext[i].isupper():
            num = ord(ciphertext[i]) - shift
            if num < ord("A"):
                num = ord("Z") - (ord("A") - num) + 1
                plaintext += chr(num)
            else:
                plaintext += chr(num)
        if ciphertext[i].isalpha() and ciphertext[i].islower():
            num = ord(ciphertext[i]) - shift
            if num < ord("a"):
                num = ord("z") - (ord("a") - num) + 1
                plaintext += chr(num)
            else:
                plaintext += chr(num)
        if not ciphertext[i].isalpha():
            plaintext += ciphertext[i]
    return plaintext