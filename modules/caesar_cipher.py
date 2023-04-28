def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += chr((ord(char) - 97 + shift * mode) % 26 + 97)
            else:
                result += chr((ord(char) - 65 + shift * mode) % 26 + 65)
        else:
            result += char
    return result
