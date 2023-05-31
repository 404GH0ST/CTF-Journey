import random

alphabet = "abcdefghijklmnopqrstuvwxyz"

known_part = "the quick brown fox jumps over the lazy dog"
ciphertext = ""

key = [random.randint(1, len(alphabet)) for _ in range(len(known_part))]
print("key:", *key)

for i, c in enumerate(known_part):
        if not c.isalpha():
                ciphertext += c
                continue

        offset = alphabet.find(c.lower())
        rotation = key[i % len(key)]

        result = alphabet[(offset + rotation) % len(alphabet)]
        if c.islower():
                ciphertext += result
        else:
                ciphertext += result.upper()

print("ciphertext:")
print(ciphertext)

for j in range(len(alphabet)):
        plaintext2 = known_part
        key = [j] * len(ciphertext)

        for i, c in enumerate(ciphertext):
                if not c.isalpha():
                        plaintext2 += c
                        continue

                offset = alphabet.find(c.lower())
                rotation = key[i % len(key)]

                result = alphabet[(offset - rotation) % len(alphabet)]
                if c.islower():
                        plaintext2 += result
                else:
                        plaintext2 += result.upper()

        if plaintext2.startswith(known_part):
                print("key:", *key)
                print("plaintext:")
                print(plaintext2)
                break

