from itertools import cycle
def xor(x,y):
    return bytes(a^y for a in x)

flag = bytes.fromhex('f4e3f091f0dbc2f2d5d493c690d2c393ffc394ceffc293fff5d393c6d5ececffd390cd93d491cd93d3dd')

print("Bruteforcing.....")
for i in range(255):
    pt = xor(flag, i)
    if b"TCP1P" in pt:
        print(f"Key: {i}")
        print(f"Flag: {pt.decode()}")