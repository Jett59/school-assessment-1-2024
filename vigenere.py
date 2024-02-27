def alphabetic_index(letter: str):
    return ord(letter.upper()) - ord('A')

def to_letter(alphabetic_index: int):
    return chr(alphabetic_index + ord('A'))

def cipher(clear_text: str, key_offsets: str):
    # Since we have to ignore non-alphabetic characters, we can't just use enumerate; we have to keep track of the index manually.
    key_index = 0
    result = ''
    for text_letter in clear_text:
        if text_letter.isalpha():
            result += to_letter((alphabetic_index(text_letter) + key_offsets[key_index]) % 26)
            key_index  = (key_index + 1) % len(key_offsets)
        else:
            result += text_letter
    return result

def decipher(cipher_text: str, key_offsets: str):
    # Deciphering is just subtracting instead of adding the key offsets.
    # We can easily reuse the cipher function with negated key offsets to achieve this, rather than having to write out the same code over again.
    return cipher(cipher_text, [-offset for offset in key_offsets])

def calculate_key_offsets(key):
    return [alphabetic_index(letter) for letter in key]

while True:
    action = input('"cipher" or "decipher"? ')
    if action == "cipher":
        text = input('Enter the text to cipher: ')
        key = input('Enter the key: ')
        if len(key) < 1:
            print('Key must be at least one character long')
            continue
        print(cipher(text, calculate_key_offsets(key)))
    elif action == "decipher":
        text = input('Enter the text to decipher: ')
        key = input('Enter the key: ')
        if len(key) < 1:
            print('Key must be at least one character long')
            continue
        print(decipher(text, calculate_key_offsets(key)))
    else:
        print('Invalid action')
