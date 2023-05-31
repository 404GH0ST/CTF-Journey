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
            break
        elif plaintext.startswith("vikeCT"):
            print(f"Found key{len(plaintext)-6} : {guess}")
            known_key.append(guess)
            break
        else:
            plaintext = ""
            key = known_key + [guess for _ in range(len("vikeCTF") - len(known_key))]
