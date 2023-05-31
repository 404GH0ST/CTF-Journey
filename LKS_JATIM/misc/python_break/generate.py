
command = input("RCE Command: ")

obfuscated = []

for c in command:
    obfuscated.append(f"chr({ord(c)})+")

print("".join(obfuscated))
