flag_enc = [0x5D, 0x32, 0x70, 0x3D, 0x34, 0x6D, 0x6D, 0x31]

key = [80, 94, 60, 9, 119, 23, 63, 0]
print("".join([chr(x) for x in key]))

for i in range(0, len(flag_enc)):
    print(chr(flag_enc[i] ^ key[i] ^ key[i + 1]))
