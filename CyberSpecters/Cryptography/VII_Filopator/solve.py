flag_enc = open("./flag.enc", "r").read().strip()

flag = ""

for c in flag_enc:
    flag += chr(int(ord(c) / 20))

print(flag)
