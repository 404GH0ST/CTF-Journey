import random

FLAG = "REDACTED"
encrypted_text = ""
key = random.randint(1, 500)

for ch in plaintext:
    e = chr(ord(ch) * key)
    encrypted_text += e

print("Key:", ????)
print("Encrypted Text:", encrypted_text)


with open('flag.enc', 'w', encoding='utf-8') as file:
    file.write(encrypted_text)