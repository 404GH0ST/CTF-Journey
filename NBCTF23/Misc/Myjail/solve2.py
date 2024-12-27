from pwn import *

r = remote("localhost", 5090)

with open("solve.py", "rb") as f:
    payload = f.read()

print(payload)
r.send(payload)
r.interactive()
