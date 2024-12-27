from pwn import *

io = remote("103.185.44.122", 18921)

io.sendlineafter(b"Input: ", b"2")

# Sending sixteen 00 (null bytes) to leak the key
io.sendlineafter(b"hex: ", b"00" * 16)
io.recvuntil(b"Hasil= ")

key = bytes.fromhex(io.recvline().strip().decode())

io.sendlineafter(b"Input: ", b"1")

flag_enc = bytes.fromhex(io.recvline().strip().decode())

flag = xor(flag_enc, key)

log.success(f"Flag: {flag.decode()}")
