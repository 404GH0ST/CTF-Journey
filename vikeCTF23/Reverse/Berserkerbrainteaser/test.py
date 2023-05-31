import random
ciphertext = "fcjzMNV{zzfo_vvuf}"

alphabet = "abcdefghijklmnopqrstuvwxyz"

bruh = 1
while bruh == 1:
        flag = ""
        realkey = []
        for i in range(27):
                
                plaintext = ""
                testkey = realkey + [i for _ in range(len("vikeCTF") - len(realkey))]
                for i, c in enumerate(ciphertext):
                        if not c.isalpha():
                                plaintext += c
                                continue

                        offset = alphabet.find(c.lower())
                        rotation = testkey[i % len(testkey)]

                        result = alphabet[(offset - rotation) % len(alphabet)]
                        if c.islower():
                                plaintext += result
                        else:
                                plaintext += result.upper()
                        
                        if plaintext.startswith("v"):
                                realkey.append()
