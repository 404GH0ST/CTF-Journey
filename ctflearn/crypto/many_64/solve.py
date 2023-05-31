import base64

flag_enc = open("flag.enc", "r").read()
while "{" not in flag_enc:
    flag_enc = base64.b64decode(flag_enc.encode()).decode()

print(flag_enc)