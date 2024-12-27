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

exe = "./mathematricks"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()

io.sendline(b"1")
io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"> ", b"0")
io.sendlineafter(b"n1: ", b"2147483649")
io.sendlineafter(b"n2: ", b"10")

io.interactive()
