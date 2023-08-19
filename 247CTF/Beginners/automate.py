from pwn import *

r = remote("3a6024e8ca8a8a3d.247ctf.com",50168)

# r.recvuntil(b"What is the answer to ")
# equation = r.recvline().strip(b"?\r\n").decode()

# r.send(str(eval(equation)).encode('utf-8') + b"\r\n")
for i in range(500):
    r.recvuntil(b"What is the answer to ")
    equation = r.recvline().strip(b"?\r\n").decode()
    info(f"equation: {eval(equation)}")
    r.send(str(eval(equation)).encode('utf-8') + b"\r\n")
print(r.recv(1024))
r.interactive()