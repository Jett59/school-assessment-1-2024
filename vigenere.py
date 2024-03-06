# The first part of this file is concerned with the relatively easy task of ciphering and deciphering text with a known key.

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


# The rest of the code deciphers text without a key.
        # It uses a form of frequency analysis, where we work out how frequent each letter is in the cipher text and compare this to the known frequencies for the english language.
# While         incredibly simple for the Caesar cipher, it is slightly more complicated for the Vigenere cipher owing to the fact that keys may be multiple characters long.

# REF: https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
alphabetic_frequencies = [0.0812, 0.0149, 0.0271, 0.0432, 0.1202, 0.0230, 0.0203, 0.0592, 0.0731, 0.0010, 0.0069, 0.0398, 0.0261, 0.0695, 0.0768, 0.0182, 0.0011, 0.0602, 0.0628, 0.0910, 0.0288, 0.0111, 0.0209, 0.0017, 0.0211, 0.0007]

def calculate_error(letters: list[str], offset: int):
    letter_occurrences = [0] * 26
    for letter in letters:
        # We subtract the offset since we are working out what offset was applied, not what offset we should apply to undo it.
        # If this results in a negative number, python will automatically wrap it around to the end of the list, achieving the correct behavior.
        letter_occurrences[alphabetic_index(letter) - offset] += 1
    error = 0
    for i in range(26):
        error += (letter_occurrences[i] / len(letters) - alphabetic_frequencies[i]) ** 2
    return error

# Returns the most likely offset, along with the certainty.
# This effectively solves a Caesar cipher.
# The certainty is the difference in error from the best offset to the second best offset, divided by the best error.
def find_optimal_offset(letters: list[str]):
    if len(letters) == 0:
        return 0, 0
    # The error is calculated as the sum of the squares of the differences from the expected frequencies.
    calculated_errors = []
    for offset in range(26):
        calculated_errors.append((offset, calculate_error(letters, offset)))

    calculated_errors.sort(key=lambda x: x[1])
    certainty = (calculated_errors[1][1] - calculated_errors[0][1]) / calculated_errors[0][1]
    return calculated_errors[0][0], certainty

# Returns the key used to cipher the text and the certainty of the result.
def find_key(cipher_text: str, key_length: int):
    # We have to split up the text into the letters which were ciphered with each letter of the key, and find the optimal offsets for each.
    split_text = [''] * key_length
    # Since we have to skip non-alphabetic characters, we can't use a simple counted for loop.
    i = 0
    for character in cipher_text:
        if character.isalpha():
            split_text[i % key_length] += character
            i += 1

    offsets = []
    total_certainty = 0
    for text in split_text:
        offset, certainty = find_optimal_offset(text)
        offsets.append(offset)
        total_certainty += certainty
    certainty = total_certainty / key_length
    key = [to_letter(offset) for offset in offsets]
    return key, certainty

def decipher_without_key(cipher_text: str):
    # We look for the key with the highest certainty, with a length up to the length of the cipher text.
    candidate_keys = [find_key(cipher_text, key_length) for key_length in range(1, len(cipher_text))]
    candidate_keys.sort(key=lambda x: x[1])
    key = ''.join(candidate_keys[-1][0])
    return key, decipher(cipher_text, calculate_key_offsets(key))

# The main loop, which delegates to the appropriate function based on user input.
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
            if len(text) < 1:
                print('Either key or text must be specified.')
                continue
            print('Attempting to automatically determine the key...')
            key, clear_text = decipher_without_key(text)
            print(f'Key: {key}')
            print(clear_text)
        else:
            print(decipher(text, calculate_key_offsets(key)))
    else:
        print('Invalid action')
