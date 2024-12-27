from pwn import *
from Crypto.PublicKey import RSA
from sage.all import factor

if len(sys.argv) != 3:
    print(f"usage: python3 {sys.argv[0]} <host> <port>")
    exit()

r = remote(sys.argv[1], sys.argv[2])


for i in range(5):
    r.recvuntil(b"?")
    r.recvline()

    public_key = r.recvuntil(b"-----END PUBLIC KEY-----")
    public_key += r.recvuntil(b"\n")

    public_key_rsa = RSA.importKey(public_key)
    n = public_key_rsa.n
    e = public_key_rsa.e

    log.info(f"Getting factor for n : {n}")
    f = factor(n)
    factor_list = [x for x, y in f]

    r.sendlineafter(b"=", str(factor_list[0]).encode())
    r.sendlineafter(b"=", str(factor_list[1]).encode())

r.interactive()
