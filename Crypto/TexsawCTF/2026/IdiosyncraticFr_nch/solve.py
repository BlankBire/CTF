import string

def decrypt(text):
    mapping = {
        'a': 'n', 'b': 'm', 'c': 'l', 'd': 'k', 'e': 'j', 'f': 'i', 'g': 'h', 'h': 'g',
        'i': 'f', 'j': 'q', 'k': 'd', 'l': 'c', 'm': 'b', 'n': 'a', 'o': 'p', 'p': 'y',
        'q': 'x', 'r': 'w', 's': 'v', 't': 'u', 'u': 't', 'v': 's', 'w': 'r', 'x': 'z',
        'y': 'p', 'z': 'o'
    }

    res = ""
    for char in text:
        lower_char = char.lower()
        if lower_char in mapping:
            new_char = mapping[lower_char]
            if char.isupper():
                res += new_char.upper()
            else:
                res += new_char
        else:
            res += char
    return res

if __name__ == "__main__":
    try:
        with open("ciphertext.txt", "r") as f:
            ciphertext = f.read()
            print(decrypt(ciphertext))
    except FileNotFoundError:
        print("Error: ciphertext.txt not found.")

