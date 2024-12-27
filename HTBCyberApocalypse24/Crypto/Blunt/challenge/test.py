from pwn import log

p = 0xdd6cc28d
A = 0xcfabb6dd
B = 0xc4a21ba9
g = 0x83e21c05

log_1 = log.progress("Testing: ")

for i in range(p//2):
    log_1.status(f"Testing i : {i}")
    new_A = pow(g, i, p)
    if A == new_A:
        print(f"Found a : {i}")
        break
