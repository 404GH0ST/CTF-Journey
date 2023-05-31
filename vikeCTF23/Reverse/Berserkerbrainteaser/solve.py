import random

ciphertext = "zexqSNE{cVaLuM_xRxBuRs_vE_mTtAe_ToOiN_oEiK}"
alphabet = "abcdefghijklmnopqrstuvwxyz"

known_flag = "vikeCTF"
key = list()
print("Brute Forcing the correct key")
for i, c in enumerate(ciphertext[:7]):
    for x in range(1,27):
        known_key = key + [x for _ in range(len(known_flag))]
        offset = alphabet.find(c.lower())
        rotation = known_key[i % len(known_key)]
        result = alphabet[(offset - rotation) % len(alphabet)]
        if result == known_flag[i].lower():
            key.append(x)
            break
print(f"Got the correct key : {key}")
plaintext = ""
for i, c in enumerate(ciphertext):
    if not c.isalpha():
        plaintext += c
        continue

    offset = alphabet.find(c.lower())
    print(offset)
    rotation = key[i % len(key)]
    result = alphabet[(offset - rotation) % len(alphabet)]
    if c.islower():
        plaintext += result
    else:
        plaintext += result.upper()
    
print(f"Flag: {plaintext}")
