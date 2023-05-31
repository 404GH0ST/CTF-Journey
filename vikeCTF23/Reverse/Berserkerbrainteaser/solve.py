import random

ciphertext = "zexqSNE{cVaLuM_xRxBuRs_vE_mTtAe_ToOiN_oEiK}"
alphabet = "abcdefghijklmnopqrstuvwxyz"

flag = ""
known_key = [4]
while flag[:7] != "vikeCTF":
    for guess in range(27):
        plaintext = ""
        key = known_key + [guess for _ in range(len("vikeCTF") - len(known_key))]
        print(key)
        for i, c in enumerate(ciphertext):
            if not c.isalpha():
                plaintext += c
                continue

            offset = alphabet.find(c.lower())
            rotation = key[i % len(key)]

            result = alphabet[(offset - rotation) % len(alphabet)]
            if c.islower():
                plaintext += result
            else:
                plaintext += result.upper()

        if plaintext[:7] == "vikeCTF":
            print(f"Found correct key : {key}")
            flag = plaintext
            known_key = key
        elif plaintext[:6] == "vikeCT":
            print(f"Found key6 : {guess}")
            known_key.append(guess)
        elif plaintext[:5] == "vikeC":
            print(f"Found key5 : {guess}")
            known_key.append(guess)
        elif plaintext[:4] == "vike":
            print(f"Found key4 : {guess}")
            known_key.append(guess)
        elif plaintext[:3] == "vik":
            print(f"Found key3 : {guess}")
            known_key.append(guess)
        elif plaintext[:2] == "vi":
            print(f"Found key2 : {guess}")
            known_key.append(guess)
        elif plaintext[:1] == "v":
            print(plaintext)
            print(f"Found key1 : {guess}")
            known_key.append(guess)
        else:
            plaintext = ""
            key = known_key + [guess for _ in range(len("vikeCTF") - len(known_key))]

def brute(msg, key):
    plaintext = ""
    key = known_key + [guess for _ in range(len("vikeCTF") - len(known_key))]
    print(key)
    for i, c in enumerate(ciphertext):
        if not c.isalpha():
            plaintext += c
            continue

        offset = alphabet.find(c.lower())
        rotation = key[i % len(key)]

        result = alphabet[(offset - rotation) % len(alphabet)]
        if c.islower():
            plaintext += result
        else:
            plaintext += result.upper()